import boto3

# Cria um recurso SQS
sqs = boto3.resource('sqs')

# Obtém a fila pelo nome
queue = sqs.get_queue_by_name(QueueName='test')

# Lista para armazenar todas as mensagens
all_messages = []

while True:
    # Recebe mensagens da fila
    messages = queue.receive_messages(
        MaxNumberOfMessages=10,  # Número máximo de mensagens a serem recebidas por vez
        WaitTimeSeconds=10  # Tempo de espera para receber a mensagem
    )

    # Verifica se há mensagens recebidas
    if not messages:
        break

    for message in messages:
        # Adiciona a mensagem à lista
        all_messages.append(message.body)

        # Exclui a mensagem da fila após o processamento
        message.delete()

# Imprime todas as mensagens
for msg in all_messages:
    print("Mensagem:", msg)



"""
Dá para criar um objeto Message usando a URL da fila e o receipt_handle da mensagem.

if messages:
    # Obtém a primeira mensagem
    message = messages[0]
    
    # Cria um objeto Message usando a URL da fila e o receipt handle
    message_obj = sqs.Message(queue_url, message.receipt_handle)
    
    # Imprime o corpo da mensagem
    print("Mensagem recebida:", message_obj.body)
    
    # Exclui a mensagem
    message_obj.delete()
    print("Mensagem excluída.")
else:
    print("Nenhuma mensagem recebida.")
"""