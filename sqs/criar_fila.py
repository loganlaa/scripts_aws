import boto3

sqs = boto3.resource('sqs')

# CRIAR  FILA
queue = sqs.create_queue(QueueName='test', Attributes={
    'DelaySeconds': '5',  # Tempo, em segundos, durante o qual o SQS entrega de todas as mensagens na fila está atrasada. (inteiro de 0 a 900 (15 minutos)). Padrão: 0.
    'MaximumMessageSize': '262.144',  # O limite de quantos bytes uma mensagem pode conter. (inteiro de 1.024 bytes (1 KiB) a 262.144 bytes (256 KiB). Padrão: 262.144 (256 KiB).
    'MessageRetentionPeriod': '345.600',  # Tempo, em segundos, que o SQS retém uma mensagem. (inteiro de 60 a 1.209.600 segundos (14 dias). Padrão: 345.600 (4 dias).
    #'Policy':, #A política da fila
    'ReceiveMessageWaitTimeSeconds': '5',  # Tempo, em segundos, pelos quais uma ação aguarda para que uma mensagem chegue (número inteiro de 0 a 20). Padrão: 0
    'VisibilityTimeout': '30',  #   TIMER para enviar o feedback de processamento da mensagem (número inteiro de 0 a 43.200 (12 horas). Padrão: 30)
    'FifoQueue': 'true',  # Indica que a fila é FIFO
})

# SE FILA JÁ EXISTENTE:
existent_queue = sqs.get_queue_by_name(QueueName='test')

# LISTAR TODAS AS FILAS EXISTENTES
for queue in sqs.queues.all():
    print(queue.url)

'''Para obter o nome de uma fila, você deve usar seu ARN, que está disponível no atributo da fila. 
   queue.attributes['QueueArn'].split(':')[-1]'''

# CRIAR MENSAGEM (Adiciona ao final da fila)
response = queue.send_message(MessageBody='Hello World')
response.get('Messages', [])
response.get('MD5OfMessageBody', [])



# Obtém a URL da fila
queue_url = queue.url

# Obtém algum atributo da fila
queue.attributes.get('VisibilityTimeout')

"""
As mensagens também podem ser enviadas em lotes. Por exemplo, enviar as duas mensagens em uma única solicitação:
"""
response = queue.send_messages(Entries=[
    {
        'Id': '1',
        'MessageBody': 'world'
    },
    {
        'Id': '2',
        'MessageBody': 'boto3',
        'MessageAttributes': {
            'Author': {
                'StringValue': 'Daniel',
                'DataType': 'String'
            }
        }
    }
])

# Print out any failures
print(response.get('Failed'))