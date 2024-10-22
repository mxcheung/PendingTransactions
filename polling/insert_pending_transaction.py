import boto3
from datetime import datetime, timedelta
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PendingTransactions')

def lambda_handler(event, context):
    transaction_id = str(uuid.uuid4())
    expiry_time = int((datetime.utcnow() + timedelta(hours=1)).timestamp())  # Set expiry to 1 hour

    # Insert record with expiry time
    table.put_item(
        Item={
            'TransactionID': transaction_id,
            'ExpiryTime': expiry_time,
            'TransactionData': event['TransactionData']  # Assumes transaction data passed in event
        }
    )

    return {'TransactionID': transaction_id, 'Status': 'Pending', 'ExpiryTime': expiry_time}
