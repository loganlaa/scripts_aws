import boto3

# Cria um recurso SQS
sqs = boto3.resource('sqs')

# Cria a fila SQS FIFO com todos os parâmetros possíveis
queue = sqs.create_queue(
    QueueName='test.fifo',  # Nome da fila deve terminar com .fifo para filas FIFO
    Attributes={
        'DelaySeconds': '5',  # Tempo de atraso na entrega das mensagens (0 a 900 segundos)
        'MaximumMessageSize': '262144',  # Tamanho máximo da mensagem em bytes (1.024 a 262.144 bytes)
        'MessageRetentionPeriod': '345600',  # Tempo de retenção da mensagem em segundos (60 a 1.209.600 segundos)
        'ReceiveMessageWaitTimeSeconds': '5',  # Tempo de espera para receber mensagens (0 a 20 segundos)
        'VisibilityTimeout': '30',  # Tempo limite de visibilidade em segundos (0 a 43.200 segundos)
        'FifoQueue': 'true',  # Indica que a fila é FIFO
        'ContentBasedDeduplication': 'true',  # Eliminação de duplicação baseada em conteúdo
        'DeduplicationScope': 'messageGroup',  # Escopo de eliminação de duplicação (messageGroup ou queue)
        'FifoThroughputLimit': 'perMessageGroupId',  # Limite de transferência FIFO (perQueue ou perMessageGroupId)
        'RedrivePolicy': '{"deadLetterTargetArn":"arn:aws:sqs:REGION:ACCOUNT-ID:DEAD_LETTER_QUEUE","maxReceiveCount":"5"}'  # Política de redirecionamento para fila de dead-letter
    }
)

print("Fila criada:", queue.url)
