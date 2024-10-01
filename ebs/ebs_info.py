import boto3

# Cria um cliente EC2
ec2 = boto3.resource('ec2', region_name='us-east-2')

volumes = ec2.volumes.all()

try:
    for volume in volumes:
        print(f"Volume ID: {volume.id}, State: {volume.state}, Size: {volume.size} GiB")
except Exception as e:
    print(e)




