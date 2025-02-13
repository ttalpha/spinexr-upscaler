PORT=$1
IP=$2
rsync -avz --inplace models.py root@$IP:/workspace
rsync -avz --inplace loss.py root@$IP:/workspace
rsync -avz --inplace transforms.py root@$IP:/workspace
rsync -avz --inplace test.py root@$IP:/workspace
rsync -avz --inplace dataset.py root@$IP:/workspace
rsync -avz --inplace train.py root@$IP:/workspace
