import boto3
from datetime import datetime, timedelta

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PendingTransactions')

def lambda_handler(event, context):
    # Get current date and date one week ago
    today = datetime.utcnow().date()
    one_week_ago = today - timedelta(days=7)
    
    expired_transactions = []

    # Loop through each day from one week ago to today
    current_date = one_week_ago
    while current_date <= today:
        # Convert current_date to string format (assuming ExpiryDate is a string in 'YYYY-MM-DD' format)
        date_str = current_date.strftime('%Y-%m-%d')
        
        # Query for transactions with this ExpiryDate
        response = table.query(
            KeyConditionExpression="ExpiryDate = :date_str AND ExpiryTime <= :current_time",
            ExpressionAttributeValues={
                ":date_str": date_str,
                ":current_time": int(datetime.utcnow().timestamp())
            }
        )

        # Collect expired transactions
        expired_transactions.extend(response.get('Items', []))

        # Move to the next date
        current_date += timedelta(days=1)
    
    # Remove expired transactions
    for transaction in expired_transactions:
        table.delete_item(
            Key={
                'TransactionID': transaction['TransactionID'],
                'ExpiryDate': transaction['ExpiryDate']
            }
        )

    return {'ExpiredTransactions': expired_transactions}
