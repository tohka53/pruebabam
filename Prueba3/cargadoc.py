import boto3
import pandas as pd

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
table_name = 'ClientesTest'
table = dynamodb.Table(table_name)
df = pd.read_csv('datos_base_clientes.csv')
print("Columnas del DataFrame:", df.columns)

def serialize_data(row):
    item = {}
    for key, value in row.items():
        if pd.isna(value):
            continue
        if key == 'ClienteID':  
            item[key] = str(value)
        else:
            if isinstance(value, str):
                item[key] = value
            elif isinstance(value, (int, float)):
                item[key] = str(value)
            elif isinstance(value, (list, dict)):
                item[key] = value
            else:
                item[key] = str(value)
    return item
def upload_data_to_dynamodb(table, df):
    with table.batch_writer() as batch:
        for index, row in df.iterrows():
            item = serialize_data(row)
            if 'ClienteID' in item:
                batch.put_item(Item=item)
            else:
                print(f"Fila {index} omitida: falta ClienteID")
if 'ClienteID' in df.columns:
    df = df.drop_duplicates(subset=['ClienteID'])
else:
    print("La columna 'ClienteID' no existe en el DataFrame")
    print("Columnas del DataFrame:", df.columns)
upload_data_to_dynamodb(table, df)
