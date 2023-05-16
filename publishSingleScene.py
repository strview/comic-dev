#lambda function
# reads from the sqs ScenesToPublish
# for each message in the queue
# it will forward the queue message to the sns topic singleSceneToPublish
# it will delete the message from the queue

import json
import boto3
import os

def handler(event, context):
    # TODO implement
    print(event)
    sns = boto3.client('sns')
    sqs = boto3.client('sqs')
    queue_url = os.environ['AWS_SCENES_TO_PUBLISH_QUEUE_URL']
    topic_arn = os.environ['AWS_SINGLE_SCENE_TO_PUBLISH_TOPIC']
    # response = sqs.receive_message(
    #     QueueUrl=queue_url,
    #     MaxNumberOfMessages=1,
    #     VisibilityTimeout=0,
    #     WaitTimeSeconds=0
    # )
    print(event)
    if 'Records' not in event:
        print("No messages in queue")
        print("response's datatype",type(event))
        return {
            'statusCode': 200,
            'body': json.dumps('No messages in queue')
        }
    message = event['Records'][0]
    print("I'm in the publishSingleScene lambda function. ", "message: ", message)
    sns.publish(
        TopicArn=topic_arn,
        Message=message['body']
    )
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=message['receiptHandle']
    )
    return {
        'statusCode': 200,
        'body': json.dumps('publishSingleScene lambda function ran successfully')
    }