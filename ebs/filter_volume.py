import boto3

# Cria uma sessão com a AWS
ec2 = boto3.resource('ec2', region_name='us-east-2')

# Filtra os volumes que estão no estado 'available' e 'in-use'
volumes = ec2.volumes.filter(
    Filters=[
        {'Name': 'status',
         'Values': ['available', 'in-use']
         },
    ]
)

# Itera sobre os volumes e imprime seus detalhes
for volume in volumes:
    print(volume.id, volume.state, volume.size, volume.availability_zone)

