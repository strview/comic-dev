# lambda function
# triggered by the sns topic singleSceneToPublish
# the sns message will be in the event parameter
# we will take the first record from the event
# and navigate down to the Message key
# the message will be a stringified json object
# we will parse the stringified json object
# we will update the dynomoDB table for that scene
# we will set is_published to true
# we will set the published_date to the current date time

import json
import boto3
import os
import datetime

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
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['AWS_SCENE_TABLE']) 
    response = table.update_item(
        Key={
            'sceneId': scene,
            'episodeId_seriesId': f"{episode}_{series}"
        },
        UpdateExpression="set is_published=:p, published_date=:d",
        ExpressionAttributeValues={
            ':p': True,
            ':d': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        ReturnValues="UPDATED_NEW"
    )
    
    print("UpdateItem succeeded:")
    print(json.dumps(response, indent=4, cls=DecimalEncoder))
    return {
        'statusCode': 200,
        'body': json.dumps('postPublishCleanup.py executed successfully!')
    }