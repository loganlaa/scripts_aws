import boto3

# Cria um recurso SQS
sqs = boto3.resource('sqs')

# Obtém todas as filas
queues = sqs.queues.all()

# Lista para armazenar os nomes das filas
queue_names = []

# Itera sobre todas as filas e obtém seus nomes
for queue in queues:
    queue_names.append(queue.url.split('/')[-1])

# Imprime os nomes das filas
for name in queue_names:
    print("Nome da fila:", name)
