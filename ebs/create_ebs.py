# CLIENT

import boto3

# Cria um cliente EC2
ec2 = boto3.client('ec2')

# Cria um volume EBS
volume = ec2.create_volume(
    AvailabilityZone='us-west-2a',  # Substitua pela zona de disponibilidade desejada
    Size=8,  # Tamanho do volume em GiB
    VolumeType='gp2',  # Tipo do volume

)

# Espera até que o volume esteja disponível
volume.wait_until_available()

# Anexa o volume à instância
volume.attach_to_instance(
    InstanceId='',  # ID da instância
    Device='/dev/sdf'  # Nome do dispositivo
)

print(f"Volume {volume.id} created and attached to instance i-1234567890abcdef0")


# RESOURCE

import boto3

# Cria uma sessão com a AWS
ec2 = boto3.resource('ec2', region_name='us-west-2')

# Cria um volume EBS
volume = ec2.create_volume(
    AvailabilityZone='us-west-2a',  # Substitua pela zona de disponibilidade desejada
    Size=8,  # Tamanho do volume em GiB
    VolumeType='gp2'  # Tipo do volume
)

# Espera até que o volume esteja disponível
volume.wait_until_available()

# Anexa o volume à instância
instance_id = 'i-1234567890abcdef0'  # ID da instância
device_name = '/dev/sdf'  # Nome do dispositivo

volume.attach_to_instance(
    InstanceId=instance_id,
    Device=device_name
)

print(f"Volume {volume.id} created and attached to instance {instance_id}")



"""
# COM RESOURCE

# Configura a opção Delete on Termination ( na EC2, após associar o volume )
ec2.Instance(instance_id).modify_attribute(
    BlockDeviceMappings=[
        {
            'DeviceName': device_name,
            'Ebs': {
                'DeleteOnTermination': True
            }
        }
    ]
)
"""

