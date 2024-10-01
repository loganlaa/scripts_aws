import boto3

# Cria um recurso SQS
sqs = boto3.resource('sqs')

# Obtém a fila pelo nome
queue = sqs.get_queue_by_name(QueueName='NOME_DA_FILA')

# Recebe mensagens da fila
messages = queue.receive_messages(
    MaxNumberOfMessages=1,  # Número máximo de mensagens a serem recebidas
    WaitTimeSeconds=10  # Tempo de espera para receber a mensagem
)

# Verifica se há mensagens recebidas
if messages:
    for message in messages:
        print("Mensagem recebida: ", message.body)

        # Obtém o receipt handle da mensagem
        receipt_handle = message.receipt_handle
        print("Receipt Handle: ", receipt_handle)

        # Exclui a mensagem da fila após o processamento
        message.delete()
        print("Mensagem excluída.")
else:
    print("Nenhuma mensagem recebida.")
