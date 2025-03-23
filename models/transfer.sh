IP=$1
PORT=$2
# rsync --inplace -azP -e "ssh -p $PORT -T -c aes128-gcm@openssh.com -o Compression=no -o StrictHostKeyChecking=no -L 8080:localhost:8080" ./datasets/train_png/ root@$IP:~/datasets
# rsync --inplace -azP -e "ssh -p $PORT -T -c aes128-gcm@openssh.com -o Compression=no -o StrictHostKeyChecking=no -L 8080:localhost:8080" ./options/ft_x4_paired.yml root@$IP:~/options
# rsync -azP -e "ssh -p $PORT -T -c aes128-gcm@openssh.com -o Compression=no -o StrictHostKeyChecking=no -L 8080:localhost:8080" ./experiments/ root@$IP:~/experiments
# rsync -azP -e "ssh -p $PORT -T -c aes128-gcm@openssh.com -o Compression=no -o StrictHostKeyChecking=no -L 8080:localhost:8080" ./degrade_png.py root@$IP:~
rsync -azP -e "ssh -p $PORT -T -c aes128-gcm@openssh.com -o Compression=no -o StrictHostKeyChecking=no -L 8080:localhost:8080" ./realesrgan/ root@$IP:~/realesrgan/