import boto3
import pandas as pd

# Configuración de DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

# Nombre de la tabla en DynamoDB
table_name = 'ClientesTest'
table = dynamodb.Table(table_name)

# Leer datos del archivo CSV
df = pd.read_csv('datos_base_clientes.csv')

# Función para transformar y serializar datos para DynamoDB
def serialize_data(row):
    item = {}
    for key, value in row.items():
        if pd.isna(value):
            continue
        if key == 'documento':
            item[key] = str(value)  # Asegúrate de que ClienteID está presente y es una cadena
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

# Función para subir datos a DynamoDB
def upload_data_to_dynamodb(table, df):
    with table.batch_writer() as batch:
        for index, row in df.iterrows():
            item = serialize_data(row)
            if 'documento' in item:
                batch.put_item(Item=item)
            else:
                print(f"Fila {index} omitida: falta ClienteID")

# Eliminar filas duplicadas basadas en 'ClienteID'
df = df.drop_duplicates(subset=['documento'])

# Ejecutar la función para subir datos
upload_data_to_dynamodb(table, df)
