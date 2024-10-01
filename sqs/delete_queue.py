import boto3

# Cria um recurso SQS
sqs = boto3.resource('sqs')

# Obtém a fila pelo nome
queue = sqs.get_queue_by_name(QueueName='NOME_DA_FILA')

# Deleta a fila
response = queue.delete()

print('Fila deletada:', response)
