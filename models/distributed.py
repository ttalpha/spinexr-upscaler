import os
import pandas as pd
import random
import torch
import time
import torch.nn as nn
import warnings
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

TRAIN_ROOT = 'dataset/train'

image_dirs = os.listdir(TRAIN_ROOT)
train_image_files = [os.path.join(TRAIN_ROOT, fname) for fname in os.listdir(TRAIN_ROOT)]

train_size = int(len(train_image_files) * c.TRAIN_PORTION)
train_image_files, val_image_files = train_image_files[:train_size], train_image_files[train_size:]

train_history = {'g_loss': [], 'd_loss': []}
val_history = {'g_loss': [], 'd_loss': [], 'ssim': [], 'psnr': []}

def setup(rank, world_size):
  os.environ['MASTER_ADDR'] = c.MASTER_ADDR  # Set master node address
  os.environ['MASTER_PORT'] = c.MASTER_PORT  # Choose an open port
  dist.init_process_group("nccl", rank=rank, world_size=world_size)
  torch.cuda.set_device(rank)

def cleanup():
  dist.destroy_process_group()

def train(rank, world_size):
  setup(rank, world_size)

  generator = Generator(scale_factor=c.SCALE_FACTOR).to(rank)
  discriminator = Discriminator().to(rank)
  vgg = vgg19(weights=VGG19_Weights.DEFAULT).to(rank).features[:c.VGG_FEATURES_EXTRACTED]

  generator = DDP(generator, device_ids=[rank], broadcast_buffers=False)
  discriminator = DDP(discriminator, device_ids=[rank], broadcast_buffers=False)

  bce_loss = nn.BCEWithLogitsLoss()
  criterion = SNSRGANLoss(vgg, device=rank)
  ssim = StructuralSimilarityIndexMeasure(data_range=2.0)
  psnr = PeakSignalNoiseRatio(data_range=2.0)

  optimizer_g = torch.optim.Adam(generator.parameters(), lr=c.LEARNING_RATE)
  optimizer_d = torch.optim.Adam(discriminator.parameters(), lr=c.LEARNING_RATE)

  best_ssim = 0

  train_dataset = XrayDataset(train_image_files, c.PATCH_SIZE, hr_transform, lr_transform)
  val_dataset = XrayDataset(val_image_files, c.PATCH_SIZE, hr_transform, lr_transform)
  train_sampler = DistributedSampler(train_dataset, num_replicas=world_size, rank=rank, shuffle=True)
  val_sampler = DistributedSampler(val_dataset, num_replicas=world_size, rank=rank, shuffle=False)

  train_loader = DataLoader(train_dataset, batch_size=c.BATCH_SIZE, shuffle=False, num_workers=c.NUM_WORKERS, pin_memory=True, sampler=train_sampler)
  val_loader = DataLoader(val_dataset, batch_size=c.BATCH_SIZE, shuffle=False, num_workers=c.NUM_WORKERS, pin_memory=True, sampler=val_sampler)

  del train_dataset
  del val_dataset

  for epoch in range(c.EPOCHS):
    print(f"Epoch [{epoch + 1}/{c.EPOCHS}]")
    epoch_start_time = time.time()

    train_sampler.set_epoch(epoch)

    generator.train()
    discriminator.train()

    with tqdm(total=len(train_loader), desc=f"Train Epoch {epoch + 1}/{c.EPOCHS}", unit="batch") as train_pbar:
      with torch.autograd.set_detect_anomaly(True):
        for lr_images, hr_images in train_loader:
          lr_images, hr_images = lr_images.to(rank), hr_images.to(rank)

          optimizer_d.zero_grad()
          fake_hr = generator(lr_images)
          real_labels = torch.ones(hr_images.size(0), 1).to(rank)
          fake_labels = torch.zeros(hr_images.size(0), 1).to(rank)

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
          g_loss = criterion(fake_hr, hr_images, d_fake)
          g_loss.backward()
          optimizer_g.step()

          train_pbar.set_postfix({
              'D Loss': f"{d_loss.item():.4f}",
              'G Loss': f"{g_loss.item():.4f}",
          })
          train_pbar.update(1)

    # Validation
    generator.eval()
    discriminator.eval()
    val_d_loss = val_g_loss = val_ssim = val_psnr = 0
    num_val_batches = len(val_loader)

    with torch.no_grad():
      with tqdm(total=num_val_batches, desc=f"Validation Epoch {epoch + 1}/{c.EPOCHS}", unit="batch") as val_pbar:
        for lr_images, hr_images in val_loader:
          lr_images, hr_images = lr_images.to(rank), hr_images.to(rank)
          fake_hr = generator(lr_images)

          real_labels = torch.ones(hr_images.size(0), 1).to(rank)
          fake_labels = torch.zeros(hr_images.size(0), 1).to(rank)

          d_real = discriminator(hr_images)
          d_fake = discriminator(fake_hr)
          real_loss = bce_loss(d_real, real_labels)
          fake_loss = bce_loss(d_fake, fake_labels)
          d_loss = real_loss + fake_loss

          g_loss = criterion(fake_hr, hr_images, d_fake)  # Move here before accumulating

          val_d_loss += d_loss.item() / num_val_batches
          val_g_loss += g_loss.item() / num_val_batches
          val_ssim += ssim(fake_hr, hr_images).item() / num_val_batches
          val_psnr += psnr(fake_hr, hr_images).item() / num_val_batches

          val_pbar.set_postfix({
            'D Loss': f"{val_d_loss:.4f}",
            'G Loss': f"{val_g_loss:.4f}",
            'SSIM': f'{val_ssim:.4f}',
            'PSNR': f'{val_psnr:.4f}'
          })
          val_pbar.update(1)

    save_image(fake_hr, f'epoch-{epoch}-output.png')
    # Save best model
    if val_ssim > best_ssim:
      best_ssim = val_ssim
      torch.save(generator.state_dict(), 'pretrained/generator.pt')
      torch.save(discriminator.state_dict(), 'pretrained/discriminator.pt')
      torch.save(optimizer_g.state_dict(), 'pretrained/optimizer_g.pt')
      torch.save(optimizer_d.state_dict(), 'pretrained/optimizer_d.pt')

    print(f"Completed in {time.time() - epoch_start_time:.2f} seconds.")

  cleanup()

if __name__ == "__main__":
  world_size = torch.cuda.device_count()
  print('World size:', world_size)
  torch.multiprocessing.spawn(train, args=(world_size,), nprocs=world_size)
  train_history_df = pd.DataFrame(train_history)
  val_history_df = pd.DataFrame(val_history)
  train_history_df.to_csv('train_history.csv')
  val_history_df.to_csv('val_history.csv')