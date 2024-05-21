import boto3
import json

sns = boto3.client('sns')
sqs = boto3.client('sqs')

def create_sns_topic(topic_name):
    response = sns.create_topic(
        Name=topic_name,
        Tags=[
            {
                'Key': 'name',
                'Value': 'nlaws'
            }
        ]
    )
    return response['TopicArn']

def create_sqs_queue(queue_name):
    response = sqs.create_queue(
        QueueName=queue_name,
        Attributes={
            'VisibilityTimeout': '30'
        },
        tags={
            'Key': 'name',
            'Value': 'nlaws'
        }
    )
    return response['QueueUrl'], queue_name

def subscribe_queue_to_topic(topic_arn, queue_arn):
    sns.subscribe(
        TopicArn=topic_arn,
        Protocol='sqs',
        Endpoint=queue_arn
    )

def get_sqs_arn(queue_url):
    response = sqs.get_queue_attributes(
        QueueUrl=queue_url,
        AttributeNames=['QueueArn']
    )
    return response['Attributes']['QueueArn']

if __name__ == '__main__':
    topic_name = input("Enter your desired SNS Topic Name: ")
    get_queue_name = input("Enter your desired SQS Queue Name for GET operations: ")
    delete_queue_name = input("Enter your desired SQS Queue Name for DELETE operations: ")
    put_queue_name = input("Enter your desired SQS Queue Name for PUT operations: ")

    # Create SNS topic
    sns_topic_arn = create_sns_topic(topic_name)

    # Create SQS queues for each operation
    get_queue_url, get_queue_name = create_sqs_queue(get_queue_name)
    delete_queue_url, delete_queue_name = create_sqs_queue(delete_queue_name)
    put_queue_url, put_queue_name = create_sqs_queue(put_queue_name)

    # Get ARN for each queue
    getqueue_arn = get_sqs_arn(get_queue_url)
    deletequeue_arn = get_sqs_arn(delete_queue_url)
    putqueue_arn = get_sqs_arn(put_queue_url)

    # Subscribe SQS queues to SNS topic with filter policies
    subscribe_queue_to_topic(sns_topic_arn, getqueue_arn)
    subscribe_queue_to_topic(sns_topic_arn, deletequeue_arn)
    subscribe_queue_to_topic(sns_topic_arn, putqueue_arn)

    # Set up filter policies for SQS subscriptions
    filter_policy_get = {
        'operation': ['get']
    }
    filter_policy_delete = {
        'operation': ['delete']
    }
    filter_policy_put = {
        'operation': ['put']
    }

    # Set filter policies for each subscription
    sns.set_subscription_attributes(
        SubscriptionArn=sns.list_subscriptions_by_topic(TopicArn=sns_topic_arn)['Subscriptions'][0]['SubscriptionArn'],
        AttributeName='FilterPolicy',
        AttributeValue=json.dumps(filter_policy_get)
    )
    sns.set_subscription_attributes(
        SubscriptionArn=sns.list_subscriptions_by_topic(TopicArn=sns_topic_arn)['Subscriptions'][1]['SubscriptionArn'],
        AttributeName='FilterPolicy',
        AttributeValue=json.dumps(filter_policy_delete)
    )
    sns.set_subscription_attributes(
        SubscriptionArn=sns.list_subscriptions_by_topic(TopicArn=sns_topic_arn)['Subscriptions'][2]['SubscriptionArn'],
        AttributeName='FilterPolicy',
        AttributeValue=json.dumps(filter_policy_put)
    )

    output = {
        "sns_topic_arn": sns_topic_arn,
        "get_queue_url": get_queue_url,
        "delete_queue_url": delete_queue_url,
        "put_queue_url": put_queue_url
    }
    print(json.dumps(output))
