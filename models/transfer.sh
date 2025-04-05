IP=$1
PORT=$2
# rsync --inplace -azP -e "ssh -p $PORT -T -c aes128-gcm@openssh.com -o Compression=no -o StrictHostKeyChecking=no -L 8080:localhost:8080" ./datasets/test_png/ root@$IP:~/test_png
# rsync --inplace -azP -e "ssh -p $PORT -T -c aes128-gcm@openssh.com -o Compression=no -o StrictHostKeyChecking=no -L 8080:localhost:8080" ./datasets/test_png_x4/ root@$IP:~/test_png_x4
# rsync --inplace -azP -e "ssh -p $PORT -T -c aes128-gcm@openssh.com -o Compression=no -o StrictHostKeyChecking=no -L 8080:localhost:8080" ./metrics.py root@$IP:~/
rsync --inplace -azP -e "ssh -p $PORT -T -c aes128-gcm@openssh.com -o Compression=no -o StrictHostKeyChecking=no -L 8080:localhost:8080" ./weights/g_x4_v3.pth root@$IP:~/weights
# rsync --inplace -azP -e "ssh -p $PORT -T -c aes128-gcm@openssh.com -o Compression=no -o StrictHostKeyChecking=no -L 8080:localhost:8080" ./infer.sh root@$IP:~/
# rsync --inplace -azP -e "ssh -p $PORT -T -c aes128-gcm@openssh.com -o Compression=no -o StrictHostKeyChecking=no -L 8080:localhost:8080" ./options/ft_x4_paired.yml root@$IP:~/options
# rsync -azP -e "ssh -p $PORT -T -c aes128-gcm@openssh.com -o Compression=no -o StrictHostKeyChecking=no -L 8080:localhost:8080" ./experiments/ root@$IP:~/experiments
# rsync -azP -e "ssh -p $PORT -T -c aes128-gcm@openssh.com -o Compression=no -o StrictHostKeyChecking=no -L 8080:localhost:8080" ./degrade_png.py root@$IP:~
# rsync -azP -e "ssh -p $PORT -T -c aes128-gcm@openssh.com -o Compression=no -o StrictHostKeyChecking=no -L 8080:localhost:8080" ./realesrgan/ root@$IP:~/realesrgan/
# rsync -azP -e "ssh -p $PORT -T -c aes128-gcm@openssh.com -o Compression=no -o StrictHostKeyChecking=no -L 8080:localhost:8080" ./inference_realesrgan.py root@$IP:~
# rsync -azP -e "ssh -p $PORT -T -c aes128-gcm@openssh.com -o Compression=no -o StrictHostKeyChecking=no -L 8080:localhost:8080" ./requirements.txt root@$IP:~/realesrgan/
