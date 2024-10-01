import boto3
import config

# Cria um cliente EC2
ec2 = boto3.client('ec2')

# Script que será executado na inicialização
user_data_script = '''#!/bin/bash
echo "Hello, World!" > /var/www/html/index.html
'''

# Lança uma nova instância EC2
response = ec2.run_instances(
    ImageId=config.AMAZON_LINUX_AMI,  # Substitua pelo ID da AMI desejada
    InstanceType=config.INSTANCE_TYPE,  # Tipo da instância
    MinCount=1,
    MaxCount=1,
    KeyName=config.KEYPAIR,  # Subs    titua pelo nome da sua KeyPair
    NetworkInterfaces=[{
            'SubnetId': config.SUBNET,  # Substitua pelo ID da sua sub-rede
            'DeviceIndex': 0,
            'AssociatePublicIpAddress': True,
            'Groups': [config.SECURITY_GROUP]
        }],
    UserData=user_data_script,
    TagSpecifications=[{
            'ResourceType': 'instance',
            'Tags': [{
                'Key': 'Name',
                'Value': 'boto3_instance'  # Substitua pelo nome desejado
            }]
        }]
)

print(response)


'''O parâmetro UserData no Boto3 permite que você forneça um script que será executado automaticamente quando a 
instância EC2 for iniciada pela primeira vez. Isso é útil para configurar a instância, instalar software, ou realizar 
outras tarefas de inicialização.'''