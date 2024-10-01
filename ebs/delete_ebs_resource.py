import boto3

# Cria uma sessão com a AWS
ec2 = boto3.resource('ec2', region_name='us-east-2')

# Filtra os volumes que estão no estado 'in-use' ou 'available'
volumes = ec2.volumes.filter(
    Filters=[
        {'Name': 'status', 'Values': ['in-use', 'available']}
    ]
)

volume_ids_to_detach = []
volume_ids_to_delete = []

for volume in volumes:
    if volume.attachments:
        volume_ids_to_detach.append(volume.id)
        # Desanexar o volume
        volume.detach_from_instance()  # Faz a desassociacao do EBS da Instancia
        print(f"Detaching volume: {volume.id}")
    else:
        volume_ids_to_delete.append(volume.id)

# Esperar até que os volumes estejam desanexados
for volume_id in volume_ids_to_detach:
    volume = ec2.Volume(volume_id)
    volume.wait_until_available()
    print(f"Volume {volume_id} is now available")
    volume_ids_to_delete.append(volume_id)

# Excluir os volumes
for volume_id in volume_ids_to_delete:
    volume = ec2.Volume(volume_id)
    if volume.state == 'available':
        volume.delete()
        print(f"Deleted volume: {volume_id}")
    else:
        print(f"Volume {volume_id} is not in a deletable state: {volume.state}")

if not volume_ids_to_delete:
    print("No volumes to delete.")

"""
volume.detach_from_instance(
                                InstanceId='i-12345',
                                Device='/dev/sda',
                                Force=True,
                            )
"""