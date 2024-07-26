import boto3

dynamodb = boto3.client('dynamodb', region_name='us-west-2')
response = dynamodb.describe_table(TableName='ClientesTest')
print(response['Table']['KeySchema'])
