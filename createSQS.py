import boto3

client = boto3.resource('sqs')

response = client.create_queue( QueueName='queue-name', Attributes = {
    'DelaySeconds': '60',
    'MessageRetentionPeriod': '1209600'
})
print(response)


