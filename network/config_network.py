import boto3
import logging

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Inicializa o recurso EC2
ec2 = boto3.resource('ec2')

def create_vpc(cidr_block):
    try:
        vpc = ec2.create_vpc(CidrBlock=cidr_block)
        vpc.wait_until_available()
        logging.info(f'VPC criada com sucesso: {vpc.id}')
        return vpc
    except Exception as e:
        logging.error(f'Erro ao criar VPC: {e}')

def create_subnet(vpc, cidr_block, availability_zone):
    try:
        subnet = vpc.create_subnet(CidrBlock=cidr_block, AvailabilityZone=availability_zone)
        logging.info(f'Sub-rede criada com sucesso: {subnet.id}')
        return subnet
    except Exception as e:
        logging.error(f'Erro ao criar sub-rede: {e}')

def create_internet_gateway():
    try:
        igw = ec2.create_internet_gateway()
        logging.info(f'Gateway da Internet criado com sucesso: {igw.id}')
        return igw
    except Exception as e:
        logging.error(f'Erro ao criar Gateway da Internet: {e}')

def attach_internet_gateway(vpc, igw):
    try:
        vpc.attach_internet_gateway(InternetGatewayId=igw.id)
        logging.info(f'Gateway da Internet {igw.id} anexado à VPC {vpc.id} com sucesso.')
    except Exception as e:
        logging.error(f'Erro ao anexar Gateway da Internet: {e}')

def create_route_table(vpc):
    try:
        route_table = vpc.create_route_table()
        logging.info(f'Tabela de rotas criada com sucesso: {route_table.id}')
        return route_table
    except Exception as e:
        logging.error(f'Erro ao criar tabela de rotas: {e}')

def create_route(route_table, destination_cidr_block, gateway_id):
    try:
        route_table.create_route(DestinationCidrBlock=destination_cidr_block, GatewayId=gateway_id)
        logging.info(f'Rota criada com sucesso na tabela de rotas {route_table.id}.')
    except Exception as e:
        logging.error(f'Erro ao criar rota: {e}')

def associate_route_table(subnet, route_table):
    try:
        route_table.associate_with_subnet(SubnetId=subnet.id)
        logging.info(f'Tabela de rotas {route_table.id} associada à sub-rede {subnet.id} com sucesso.')
    except Exception as e:
        logging.error(f'Erro ao associar tabela de rotas: {e}')

# Exemplo de uso
if __name__ == "__main__":
    vpc_cidr_block = '10.0.0.0/16'
    subnet_cidr_block = '10.0.1.0/24'
    availability_zone = 'us-east-1a'
    destination_cidr_block = '0.0.0.0/0'

    vpc = create_vpc(vpc_cidr_block)
    subnet = create_subnet(vpc, subnet_cidr_block, availability_zone)
    igw = create_internet_gateway()
    attach_internet_gateway(vpc, igw)
    route_table = create_route_table(vpc)
    create_route(route_table, destination_cidr_block, igw.id)
    associate_route_table(subnet, route_table)
