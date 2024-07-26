import boto3
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
table_name = 'ClientesTest'
table = dynamodb.create_table(
    TableName=table_name,
    KeySchema=[
        {
            'AttributeName': 'ClienteID',
            'KeyType': 'HASH' 
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'ClienteID',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)
table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
print(f"Tabla '{table_name}' creada con éxito.")
