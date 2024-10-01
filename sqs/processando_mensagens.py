import boto3

sqs = boto3.resource('sqs')

queue = sqs.get_queue_by_name(QueueName='test')

# As mensagens são processadas em lotes:
for message in queue.receive_messages(MessageAttributeNames=['Author']):  # O parâmetro MessageAttributeNames=['Author'] especifica que queremos receber o atributo de mensagem personalizado chamado “Author”.
    # Get the custom author message attribute if it was set
    author_text = ''
    if message.message_attributes is not None:
        author_name = message.message_attributes.get('Author').get('StringValue')
        if author_name:
            author_text = ' ({0})'.format(author_name)

    # Print out the body and author (if set)
    print('Hello, {0}!{1}'.format(message.body, author_text))

    # Let the queue know that the message is processed
    message.delete()

"""
receive_message é usado para recuperar uma mensagem da fila.
A resposta contém um campo Messages, que é uma lista de mensagens. 
Cada mensagem tem um ReceiptHandle, que você pode usar para deletar a mensagem posteriormente
"""