import boto3

s3 = boto3.resource(service_name='s3', region_name='us-east-2')

for obj in s3.Bucket('NOME DA BUCKET').objects.all():
    print(obj.key)

