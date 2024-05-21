import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME'] 
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    for record in event['Records']:
        message = json.loads(record['body'])
        # Extract values from SQS message
        message_text = message['Message'] 
        timestamp = message['Timestamp']
        
        # Send values to table
        table.put_item(
            Item={
                'message': message_text,
                'timestamp': timestamp
            }
        )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Values processed successfully')
    }