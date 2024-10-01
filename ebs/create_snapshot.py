import boto3
from datetime import datetime

# Inicializa o recurso EC2
ec2 = boto3.resource('ec2')


def create_snapshot(volume_id, description):
    try:
        volume = ec2.Volume(volume_id)
        snapshot = volume.create_snapshot(Description=description,
                                          VolumeId='',
                                          #TagSpecifications=[{'': ''}]
                                          )

        print(f'Snapshot criado com sucesso: {snapshot.id}')
        return snapshot
    except Exception as e:
        print(f'Erro ao criar snapshot para o volume {volume_id}: {e}')


def main():
    # IDs dos volumes EBS para os quais você deseja criar snapshots
    volume_ids = ['', '']  # [volume.id for volume in volumes]

    # Descrição do snapshot
    description = f'Snapshot criado em {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'

    for volume_id in volume_ids:
        create_snapshot(volume_id, description)


if __name__ == "__main__":
    main()
