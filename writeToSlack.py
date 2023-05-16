# lambda function
# reads from the sns topic singleSceneToPublish
# for each message in the topic it will create a string from the message
# and send it to the webhook "https://hooks.slack.com/services/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"
# this incoming topic will look like this:
# {
#   "series": "series",
#   "episode": "episode",
#   "scene": "scene",
#   "url": "url",
#   "added_data": current date time
# }
# the message sent to slack will look like this:
# f'New scene added to {series}. This is Scene {scene} from Episode {episode}. Click here to view: {url}. Date: {added_date}'

import json
import boto3
import os
import datetime
import requests

def handler(event, context):
    # TODO implement
    print(event)
    message = json.loads(event['Records'][0]["Sns"]["Message"])
    series = message['series']
    episode = message['episode']
    scene = message['scene']
    url = message['url']
    added_date = message['added_date']
    print(f"series: {series}, episode: {episode}, scene: {scene}, url: {url}, added_date: {added_date}")
    webhook_url = os.environ['AWS_SLACK_WEBHOOK_URL']
    message = f'New scene added to {series}. This is Scene {scene} from Episode {episode}. Click here to view: {url}. Date: {added_date}'
    slack_data = {'text': message}
    response = requests.post(
        webhook_url, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )
    print(response)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }