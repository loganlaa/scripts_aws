import boto3

sqs = boto3.resource('sqs')

def create_queue(queue_name):
    queue = sqs.create_queue(QueueName=queue_name, Attributes={
        'DelaySeconds': '10',
        'MessageRetentionPeriod': '86400',  # 1 dia
    })
    return queue

def send_message(queue, messages):
    for message in messages:
        queue.send_message(MessageBody=message)

def receive_message(queue):
    while True:  # configurado para continuar recebendo mensagens até que a fila esteja vazia.
        queue_messages = queue.receive_messages(
            MaxNumberOfMessages=10,
            WaitTimeSeconds=10,
        )
        if not queue_messages:
            break
        for message in queue_messages:
            print(message.body)
            message.delete()

def delete_queue(queue):
    queue.delete()

if __name__ == '__main__':

    queue_name = input('Queue Name: ')
    messages = ['Olá, Mundo', 'Testando','AWS é top']

    queue = create_queue(queue_name)
    print("Fila Criada: ", queue.url.split('/')[-1])

    send_message(queue, messages)
    print("Mensagens Enviadas")

    receive_message(queue)
    delete_queue(queue)
    print("Fila Deletada: ", queue.url.split('/')[-1])