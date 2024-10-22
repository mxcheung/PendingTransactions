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




# Scheduling Lambda 3
You can use CloudWatch Events or EventBridge to trigger Lambda 3 at a desired interval (e.g., every 5 minutes, every hour). Here’s how you can schedule it:

CloudWatch Console:

Go to Events > Rules > Create rule.
Choose Event Source as "Schedule" and set the interval.
Set Target to Lambda 3.
Infrastructure as Code (optional): If you're using AWS CDK or SAM, you can define a scheduled event to trigger Lambda 3.

# Considerations:
## Performance: Scanning DynamoDB can be costly, especially if your table grows large. You might want to consider indexing or partitioning strategies if the table becomes large over time.
Rate Limiting: Ensure your Lambda 3 is not invoked too frequently to avoid excessive cost or throttling.
