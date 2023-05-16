# this is a lamba function tied to an http endpoint
# the incoming data will be in the format:
# {
#   "series": "series", 
#   "episode": "episode",
# }
# the function will parse the data and look the episode in dynamodb based on the series and episode
# the table has hash AttributeName of episodeId and a range AttributeName of seriesId 
# the function will check a property called is_published. If it is true, it will not run the rest of the function
# the function will then search the scene table for all scenes that match the series and episode
# the function will then loop through the scenes and for each item it will write a message to the sqs queue.
# each message will be added to the queue with a delay of 24 hours
# the message will be in the format:
# {
#   "series": "series",
#   "episode": "episode",
#   "scene": "scene",
#   "url": "url",
#   "added_data": current date time
# }

import json
import boto3
import os
import datetime

def handler(event, context):
    # TODO implement
    print(event)
    series = event['body']['series']
    episode = event['body']['episode']
    # series_table = os.environ['AWS_SERIES_TABLE']
    episode_table = os.environ['AWS_EPISODE_TABLE']
    scene_table = os.environ['AWS_SCENE_TABLE']
    queue_url = os.environ['AWS_SCENES_TO_PUBLISH_QUEUE_URL']
    dynamodb = boto3.resource('dynamodb')
    # series_table = dynamodb.Table(series_table)
    episode_table = dynamodb.Table(episode_table)
    scene_table = dynamodb.Table(scene_table)
    # series_response = series_table.get_item(
    #     Key={
    #         'seriesId': series    
    #     }
    # )
    # if 'Item' not in series_response:
    #     return {
    #         'statusCode': 404,
    #         'body': json.dumps('Series not found')
    #     }
    episode_response = episode_table.get_item(
        Key={
            'seriesId': series,
            'episodeId': episode
        }
    )
    if 'Item' not in episode_response:
        return {
            'statusCode': 404,
            'body': json.dumps('Episode not found')
        }
    if episode_response['Item']['is_published']:
        return {
            'statusCode': 200,
            'body': json.dumps('Episode already published')
        }
    # scene_response = scene_table.query(
    #     KeyConditionExpression='seriesId = :seriesId and episodeId = :episodeId',
    #     ExpressionAttributeValues={
    #         ':seriesId': series,
    #         ':episodeId': episode
    #     }
    # )
    # rewrite the above query to use a scan instead of a query
    # use the attribute name episodeId_seriesId to filter  
    # the value for episodeId_seriesId will be <episodeId>_<seriesId>
    scene_response = scene_table.scan(
        FilterExpression='episodeId_seriesId = :episodeId_seriesId',
        ExpressionAttributeValues={
            ':episodeId_seriesId': episode + '_' + series
        }
    )
    sqs = boto3.client('sqs')
    # there is a max delay of 15 minutes for sqs
    SPACING_IN_SECS  = 10
    delay_seconds = 0
    for item in scene_response['Items']:
        message = {
            'series': series,
            'episode': episode,
            'scene': item['sceneId'],
            'url': item['url'],
            'added_date': str(datetime.datetime.now())
        }
        print(message)
        sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(message),
            DelaySeconds=delay_seconds
        )
        delay_seconds += SPACING_IN_SECS
    # episode_table.update_item(
    #     Key={
    #         'seriesId': series,
    #         'episodeId': episode
    #     },
    #     UpdateExpression='SET is_published = :is_published',
    #     ExpressionAttributeValues={
    #         ':is_published': True
    #     }
    # )
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }



