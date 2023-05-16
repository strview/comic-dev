# create aws lambda function called parseFileName
# it will be triggered by s3 bucket creation event
# it will parse the file name which will be in the format <series>-<episode>-<scene>.png
# it will create a json file with the following format and send that json as a message to sns topic.
# {
#   "series": "series",
#   "episode": "episode",
#   "scene": "scene",
#    "filename": "filename",
# }

import json
import boto3
import os

def parseFileName(event, context):
    # TODO implement
    ## use the AWS_PARSED_NAME_TOPIC environment variable to get the SNS topic ARN
    ## it is locatd in servreless.yml file
    topic_arn = os.environ['AWS_PARSED_NAME_TOPIC']


    print(event)
    sns = boto3.client('sns')
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key'] 
    url = "https://" + bucket + ".s3.amazonaws.com/" + key

    series, episode, scene = key.split('-')
    series = series.split('/')[1]
    message = {
        'series': series,
        'episode': episode,
        'scene': scene.split('.')[0],
        'filename': key,
        'url': url
    }
    print(message)
    response = sns.publish(
        TopicArn=topic_arn,
        Message=json.dumps(message)
    )
    print(response)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }