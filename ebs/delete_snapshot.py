import sys

import boto3

ec2 = boto3.resource('ec2')

def delete_snapshot(snapshot_id):
    try:
        snapshot = ec2.Snapshot(snapshot_id)  # Instancia um objeto snapshot
        snapshot.delete()  # Deleta o snapshot
        print(f'Snapshot deleted: {snapshot_id}')
    except Exception as e:
        print(f'Erro ao deletar snapshot {snapshot_id}: {e}')

def main():
    snapshot_ids = ['snap-0123456789abcdef0', 'snap-0987654321abcdef0']

    '''
    # Obtém todos os snapshots (você pode filtrar conforme necessário)
    snapshots = ec2.snapshots.filter(OwnerIds=['self'])
    '''

    '''
    # Cria uma lista de IDs de snapshots
    snapshot_ids = [snapshot.id for snapshot in snapshots]
    list(map(delete_snapshot, snapshot_ids))
    '''

    for snapshot_id in snapshot_ids:  # list(map(delete_snapshot, snapshot_ids))  aplica a função delete_snapshot a cada item na lista snapshot_ids.
        delete_snapshot(snapshot_id)

if __name__ == "__main__":
    main()