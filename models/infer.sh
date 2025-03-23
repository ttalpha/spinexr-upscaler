pip install -r requirements.txt &&
wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth -P weights && (
  python inference_realesrgan.py -n RealESRGAN_x4plus -i datasets/test_jpeg_x4 -o results/base &
  python inference_realesrgan.py -n RealESRGAN_x4plus -i datasets/test_jpeg_x4 -o results/ftx4 -mp experiments/ft_SpineXR_x4_paired/models/net_g_6000.pth &
  python inference_realesrgan.py -s 2 -n RealESRGAN_x2plus -i datasets/test_jpeg_x2 -o results/ftx2 -mp experiments/ft_SpineXR_x2_paired/models/net_g_6000.pth
) &&
pip install torchmetrics &&
python metrics.py