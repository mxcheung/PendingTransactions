To refactor the solution without using DynamoDB TTL, 
Lambda 3 will periodically poll the PendingTransactions table to check for expired transactions. 
We will modify the design such that Lambda 3 identifies transactions that have expired based on the current timestamp and removes them if they have expired.

Here’s the updated solution:

# Lambda Functions Overview
Lambda 1: Insert New Pending Transaction

Inserts a new transaction into the DynamoDB table with an explicit expiration timestamp (not using TTL).
# Lambda 2: Remove Transaction on Completion

Removes a transaction once it is completed.
# Lambda 3: Check for Expired Transactions

Polls the DynamoDB table periodically to find and remove transactions that have expired. This Lambda will be triggered via a scheduled event (CloudWatch Events or EventBridge).
