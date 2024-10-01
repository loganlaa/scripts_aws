import boto3

# Cria uma sessão com a AWS
ec2 = boto3.resource('ec2')

# Filtra as instâncias que estão no estado 'running'
running_instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
)

# Itera sobre as instâncias e imprime os seus atributos
for instance in running_instances:
    print(instance.id, instance.state, instance.private_dns_name, instance.public_dns_name)
