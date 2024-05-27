import json
import boto3
import os

client = boto3.client('dynamodb')
dynamodb = boto3.resource("dynamodb")
table_name = os.environ['TABLE_NAME'] 
table = dynamodb.Table(table_name)

sns_client = boto3.client('sns')
sns_topic_arn = os.environ['SNS_TOPIC_ARN']

def publish_to_sns(message, operation):
    sns_client.publish(
        TopicArn=sns_topic_arn,
        Message=message,
        MessageAttributes={
            'operation': {
                'DataType': 'String',
                'StringValue': operation
            }
        },
        Subject='DynamoDB Operation'
    )

def lambda_handler(event, context):
    print(event)
    body = {}
    statusCode = 200
    headers = {
        "Content-Type": "application/json"
    }

    try:
        route_key = event['routeKey']
        
        if route_key == "DELETE /items/{id}":
            # Delete item based on id 
            table.delete_item(Key={'id': event['pathParameters']['id']})
            body = 'Deleted item ' + event['pathParameters']['id']
            publish_to_sns(body, 'delete')

        elif route_key == "GET /items/{id}":
            # Retrieve item by ID and include the new attributes in the response
            response = table.get_item(Key={'id': event['pathParameters']['id']})
            if 'Item' in response:
                item = response['Item']
                body = {
                    'id': item['id'],
                    'name': item.get('name', ''),
                    'email': item.get('email', ''),
                    'filename': item.get('filename', '')
                }
                publish_to_sns(f'Retrieved item {event["pathParameters"]["id"]}', 'get')
            else:
                statusCode = 404
                body = f"Item with id {event['pathParameters']['id']} not found."

        elif route_key == "GET /items":
            # Check if query parameters are present
            query_params = event.get('queryStringParameters', {})
            if query_params and 'id' in query_params:
                # Construct the query parameters for DynamoDB
                query_kwargs = {
                    'KeyConditionExpression': 'id = :id',
                    'ExpressionAttributeValues': {
                        ':id': query_params['id']
                    }
                }
                response = table.query(**query_kwargs)
                items = response.get('Items', [])
                body = items
                publish_to_sns('Retrieved items based on query', 'get')
            else:
                # Scan the table and include the new attributes for each item in the response
                response = table.scan()
                items = response.get('Items', [])
                body = [
                    {'id': item['id'],
                     'name': item.get('name', ''),
                     'email': item.get('email', ''),
                     'filename': item.get('filename', '')
                    } for item in items
                ]
                publish_to_sns('Retrieved all items', 'get')

        elif route_key == "PUT /items":
            # Parse the request body and put the item with new attributes into the DynamoDB table
            requestJSON = json.loads(event['body'])
            table.put_item(
                Item={
                    'id': requestJSON['id'],
                    'name': requestJSON.get('name', ''),
                    'email': requestJSON.get('email', ''),
                    'filename': requestJSON.get('filename', '')
                })
            body = 'Put item ' + requestJSON['id']
            publish_to_sns(body, 'put')

    except KeyError as e:
        statusCode = 400
        body = f'Error processing request: {str(e)}'

    # Convert response body to JSON and return response
    res = {
        "statusCode": statusCode,
        "headers": headers,
        "body": json.dumps(body)
    }
    return res