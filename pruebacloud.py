import boto3
import pandas as pd

# Configuración de DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

# Nombre de la tabla en DynamoDB
table_name = 'ClientesTest'
table = dynamodb.Table(table_name)

# Leer datos del archivo CSV
df = pd.read_csv('datos_base_clientes.csv')

# Imprimir los nombres de las columnas para verificar
print("Columnas del DataFrame:", df.columns)

# Función para transformar y serializar datos para DynamoDB
def serialize_data(row):
    item = {}
    for key, value in row.items():
        if pd.isna(value):
            continue
        # Asegúrate de que ClienteID o el nombre correcto de la clave primaria esté presente
        if key == 'ClienteID':  # Cambia 'ClienteID' por el nombre correcto si es diferente
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

# Función para subir datos a DynamoDB
def upload_data_to_dynamodb(table, df):
    with table.batch_writer() as batch:
        for index, row in df.iterrows():
            item = serialize_data(row)
            if 'ClienteID' in item:
                batch.put_item(Item=item)
            else:
                print(f"Fila {index} omitida: falta ClienteID")

# Verificar si la columna 'ClienteID' existe y eliminar duplicados
if 'ClienteID' in df.columns:
    df = df.drop_duplicates(subset=['ClienteID'])
else:
    print("La columna 'ClienteID' no existe en el DataFrame")
    print("Columnas del DataFrame:", df.columns)

# Ejecutar la función para subir datos
upload_data_to_dynamodb(table, df)
