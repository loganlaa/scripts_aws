import boto3


def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name='us-east-2')
    instance_ids = ['i-0abcd1234efgh5678', 'i-0wxyz1234ijkl5678']  # Substitua pelos IDs das suas instâncias
    ec2.start_instances(InstanceIds=instance_ids)
    print(f'Instâncias {instance_ids} iniciadas')
