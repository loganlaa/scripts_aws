import boto3
import config

# Cria um cliente EC2
ec2 = boto3.resource('ec2')

instances = ec2.create_instances(
    ImageId=config.AMAZON_LINUX_AMI,  # Substitua pelo ID da AMI desejada
    InstanceType=config.INSTANCE_TYPE,  # Tipo da instância
    MinCount=3,
    MaxCount=3,
    KeyName=config.KEYPAIR,  # Substitua pelo nome da sua KeyPair
    NetworkInterfaces=[{
        'SubnetId': config.SUBNET,  # Substitua pelo ID da sua sub-rede
        'DeviceIndex': 0,
        'AssociatePublicIpAddress': True,
        'Groups': [config.SECURITY_GROUP]
    }],
    # UserData=user_data_script,
    TagSpecifications=[{
        'ResourceType': 'instance',
        'Tags': [{
            'Key': 'Name',
            'Value': 'boto3_instance'  # Substitua pelo nome desejado
        }]
    }]
)

# Exibe o ID da instância criada
for instance in instances:
    print(f'Instância criada com ID: {instance.id}')

# instances é uma lista de recursos ec2

# Parar a instancias
for instance in instances:
     instance.stop()

# Iniciar instancias
for instance in instances:
    instance.start()

# Terminar instancias
for instance in instances:
    instance.terminate(
        Hibernate=False,
        Force=True,
        DryRun=False
    )





