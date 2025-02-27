import os
import pandas as pd
import random
import torch
import time
import torch.nn as nn
import warnings
from distance_transform import DistanceTransformLoss
import constants as c
import torch.distributed as dist

from tqdm import tqdm
from torch.utils.data import DataLoader, DistributedSampler
from loss import SNSRGANLoss
from dataset import XrayDataset
from torchvision.models import vgg19, VGG19_Weights
from models import Generator, Discriminator
from transforms import lr_transform, hr_transform
from torchvision.utils import save_image
from torchmetrics.image.ssim import StructuralSimilarityIndexMeasure
from torchmetrics.image.psnr import PeakSignalNoiseRatio
from torch.nn.parallel import DistributedDataParallel as DDP

warnings.filterwarnings('ignore')

random.seed(c.SEED)
torch.manual_seed(c.SEED)
torch.cuda.manual_seed(c.SEED)
torch.cuda.manual_seed_all(c.SEED)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

def setup():
	torch.cuda.set_device(int(os.environ["LOCAL_RANK"]))
	dist.init_process_group("nccl")

def cleanup():
	dist.destroy_process_group()

def main():
	setup()
	TRAIN_ROOT = 'images/train_jpeg'
	train_image_files = [os.path.join(TRAIN_ROOT, fname) for fname in os.listdir(TRAIN_ROOT)]

	train_size = int(len(train_image_files) * c.TRAIN_PORTION)
	train_image_files, val_image_files = train_image_files[:train_size], train_image_files[train_size:]

	train_history = {'g_loss': [], 'd_loss': []}
	val_history = {'ssim': [], 'psnr': []}
	gpu_id = int(os.environ['LOCAL_RANK'])
	is_main_process = gpu_id == 0

	generator = Generator(scale_factor=c.SCALE_FACTOR).to(gpu_id)
	discriminator = Discriminator().to(gpu_id)
	vgg = vgg19(weights=VGG19_Weights.DEFAULT).to(gpu_id).features[:c.VGG_FEATURES_EXTRACTED]

	generator = DDP(generator, device_ids=[gpu_id], broadcast_buffers=False)
	discriminator = DDP(discriminator, device_ids=[gpu_id], broadcast_buffers=False)
	bce_loss = nn.BCELoss()
	dtl = DistanceTransformLoss(n=c.SHARPNESS)
	criterion = SNSRGANLoss(vgg, dtl, device=gpu_id)
	ssim = StructuralSimilarityIndexMeasure(data_range=1.0).to(gpu_id)
	psnr = PeakSignalNoiseRatio(data_range=1.0).to(gpu_id)

	best_ssim = 0

	train_dataset = XrayDataset(train_image_files, c.PATCH_SIZE, hr_transform, lr_transform, is_val=False)
	val_dataset = XrayDataset(val_image_files, c.PATCH_SIZE, hr_transform, lr_transform, is_val=True)
	train_sampler = DistributedSampler(train_dataset, num_replicas=world_size, rank=gpu_id, shuffle=True)
	val_sampler = DistributedSampler(val_dataset, num_replicas=world_size, rank=gpu_id, shuffle=False)

	train_loader = DataLoader(train_dataset, batch_size=c.BATCH_SIZE, shuffle=False, num_workers=c.NUM_WORKERS, pin_memory=True, sampler=train_sampler)
	val_loader = DataLoader(val_dataset, batch_size=c.BATCH_SIZE, shuffle=False, num_workers=c.NUM_WORKERS, pin_memory=True, sampler=val_sampler)

	optimizer_g = torch.optim.Adam(generator.parameters(), lr=c.GEN_LR)
	optimizer_d = torch.optim.Adam(discriminator.parameters(), lr=c.DISC_LR)
	g_lr_scheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer_g, gamma=0.8)
	d_lr_scheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer_d, gamma=0.8)

	del train_dataset
	del val_dataset

	for epoch in range(c.EPOCHS):
		if is_main_process:
			print(f"Epoch [{epoch + 1}/{c.EPOCHS}]")
			epoch_start_time = time.time()

		train_sampler.set_epoch(epoch)

		generator.train()
		discriminator.train()
		train_pbar = tqdm(total=len(train_loader), desc=f"Train Epoch {epoch + 1}/{c.EPOCHS}", unit="batch") if is_main_process else None

		total_d_loss = torch.tensor(0.0, device=gpu_id)
		total_g_loss = torch.tensor(0.0, device=gpu_id)

		for lr_images, hr_images in train_loader:
			lr_images, hr_images = lr_images.to(gpu_id), hr_images.to(gpu_id)

			optimizer_d.zero_grad()
			fake_hr = generator(lr_images)
			real_labels = torch.ones(hr_images.size(0), 1).to(gpu_id)
			fake_labels = torch.zeros(hr_images.size(0), 1).to(gpu_id)

			# Compute discriminator losses
			d_real = discriminator(hr_images)
			d_fake = discriminator(fake_hr.detach())
			real_loss = bce_loss(d_real, real_labels)
			fake_loss = bce_loss(d_fake, fake_labels)
			d_loss = real_loss + fake_loss
			d_loss.backward()
			optimizer_d.step()

			# Train Generator
			optimizer_g.zero_grad()
			d_fake = discriminator(fake_hr)  # Recompute for generator loss
			g_loss = 1e-3 * bce_loss(d_fake, real_labels) + criterion(fake_hr, hr_images)
			g_loss.backward()
			optimizer_g.step()

			# Accumulate losses for averaging across GPUs
			total_d_loss += d_loss.detach()
			total_g_loss += g_loss.detach()

			if is_main_process:
				train_pbar.set_postfix({
					'D Loss': f"{d_loss.item():.4f}",
					'G Loss': f"{g_loss.item():.4f}",
					'D LR': f'{d_lr_scheduler.get_last_lr()[0]:.4f}',
					'G LR': f'{g_lr_scheduler.get_last_lr()[0]:.4f}',
				})
				train_pbar.update(1)

		if is_main_process:
			train_pbar.close()
			g_lr_scheduler.step()
			d_lr_scheduler.step()

		# Synchronize and compute average loss across GPUs
		dist.barrier()
		dist.all_reduce(total_d_loss, op=dist.ReduceOp.SUM)
		dist.all_reduce(total_g_loss, op=dist.ReduceOp.SUM)
		num_train_batches = len(train_loader)
		total_d_loss /= num_train_batches * dist.get_world_size()
		total_g_loss /= num_train_batches * dist.get_world_size()
		saved = False

		# Validation
		generator.eval()
		discriminator.eval()
		val_ssim = torch.tensor(0.0, device=gpu_id)
		val_psnr = torch.tensor(0.0, device=gpu_id)

		num_val_batches = len(val_loader)

		with torch.no_grad():
			for lr_images, hr_images in val_loader:
				lr_images, hr_images = lr_images.to(gpu_id), hr_images.to(gpu_id)
				fake_hr = generator(lr_images)
				if not saved:
					os.makedirs('samples', exist_ok=True)
					save_image(fake_hr, f'samples/epoch-{epoch}-output.png') # save sample images to see progress
					saved = True
				val_ssim += ssim(fake_hr, hr_images).detach()
				val_psnr += psnr(fake_hr, hr_images).detach()

		# Synchronize and compute average metrics across GPUs
		dist.barrier()
		dist.all_reduce(val_ssim, op=dist.ReduceOp.SUM)
		dist.all_reduce(val_psnr, op=dist.ReduceOp.SUM)

		val_ssim /= num_val_batches * dist.get_world_size()
		val_psnr /= num_val_batches * dist.get_world_size()

		# Save best model (only on main process)
		if is_main_process:
			print(f'SSIM: {val_ssim:.4f}, PSNR: {val_psnr:.4f}')
			train_history['g_loss'].append(total_g_loss.item())
			train_history['d_loss'].append(total_d_loss.item())
			val_history['ssim'].append(val_ssim.item())
			val_history['psnr'].append(val_psnr.item())
			if val_ssim.item() > best_ssim:
				best_ssim = val_ssim.item()
				os.makedirs('models', exist_ok=True)
				torch.save(generator.state_dict(), 'models/generator.pt')
				torch.save(discriminator.state_dict(), 'models/discriminator.pt')
				torch.save(optimizer_g.state_dict(), 'models/optimizer_g.pt')
				torch.save(optimizer_d.state_dict(), 'models/optimizer_d.pt')

			print(f"Completed in {time.time() - epoch_start_time:.2f} seconds.")


	train_history_df = pd.DataFrame(train_history)
	val_history_df = pd.DataFrame(val_history)
	os.makedirs('progress', exist_ok=True)
	train_history_df.to_csv('progress/train_history.csv', index=False)
	val_history_df.to_csv('progress/val_history.csv', index=False)
	cleanup()

if __name__ == "__main__":
	world_size = torch.cuda.device_count()
	main()