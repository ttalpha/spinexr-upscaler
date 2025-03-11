# code to upload everything onto a remote server
IP=$1
PORT=$2
rsync -azP -e "ssh -p $PORT -T -c aes128-gcm@openssh.com -o Compression=no -o StrictHostKeyChecking=no" ./ root@$IP:/workspace/esrgan/
