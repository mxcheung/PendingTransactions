import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PendingTransactions')

def lambda_handler(event, context):
    current_time = int(datetime.utcnow().timestamp())

    # Scan for transactions that have expired
    response = table.scan(
        FilterExpression="ExpiryTime <= :current_time",
        ExpressionAttributeValues={":current_time": current_time}
    )

    expired_transactions = response.get('Items', [])

    # Remove expired transactions
    for transaction in expired_transactions:
        table.delete_item(
            Key={
                'TransactionID': transaction['TransactionID']
            }
        )

    return {'ExpiredTransactions': expired_transactions}
