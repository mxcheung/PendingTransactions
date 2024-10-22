import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PendingTransactions')

def lambda_handler(event, context):
    transaction_id = event['TransactionID']
    
    # Remove transaction
    response = table.delete_item(
        Key={
            'TransactionID': transaction_id
        }
    )

    return {'TransactionID': transaction_id, 'Status': 'Completed'}
