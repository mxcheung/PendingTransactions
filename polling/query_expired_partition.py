import boto3
from datetime import datetime, timedelta

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PendingTransactions')

def lambda_handler(event, context):
    # Get the timestamp for one week ago
    one_week_ago = int((datetime.utcnow() - timedelta(weeks=1)).timestamp())

    # Query the GSI to find transactions that are older than one week
    response = table.query(
        IndexName='date-time-index',
        KeyConditionExpression="ExpiryTime <= :one_week_ago",
        ExpressionAttributeValues={":one_week_ago": one_week_ago}
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
