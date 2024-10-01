import boto3


def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name='us-east-2')
    instance_ids = ['i-0abcd1234efgh5678', 'i-0wxyz1234ijkl5678']  # Substitua pelos IDs das suas instâncias
    ec2.stop_instances(InstanceIds=instance_ids)
    print(f'Instâncias {instance_ids} paradas')


# parar as instâncias sem realizar outras operações

'''ec2.instances.filter com instance.stop(): Use quando você precisa aplicar filtros complexos e realizar operações adicionais em cada instância.
ec2.stop_instances(): Use quando você souber os IDs das instâncias de antemão e quiser parar todas de uma vez de maneira eficiente.'''
