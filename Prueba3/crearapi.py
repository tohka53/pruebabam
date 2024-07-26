from flask import Flask, jsonify
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)


dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
table = dynamodb.Table('ClientesTest')

@app.route('/cliente/<ClienteID>', methods=['GET'])
def get_cliente(ClienteID):
    try:
        response = table.get_item(Key={'ClienteID': ClienteID})
        item = response.get('Item')
        if item:
            return jsonify(item)
        else:
            return jsonify({'error': 'Cliente no encontrado'}), 404
    except ClientError as e:
        return jsonify({'error': e.response['Error']['Message']}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
