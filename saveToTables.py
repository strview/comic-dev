# create aws lambda function called handler
# it will be triggered by sns topic
# it will parse out of the message the series, episode, scene, and filename
# the message looks like this:
# {
#   "series": "series",
#   "episode": "episode",
#   "scene": "scene",
#    "filename": "filename",
#   "url": "url"    
# }
# it will check to see if the series already exists in the series table
# if not, it will add it,         
# it will also add a property to the series table called name which is the series in title case
        
# it will check to see if the episode already exists in the episode table
# if not, it will add it. it will include a foreign key to the series table
# it will check to see if the scene already exists in the scene table
# if not, it will add it. it will include a foreign key to the episode table

import json
import boto3 # pylint: disable=import-error
import os

def handler(event, context):
    message = json.loads(event['Records'][0]['Sns']['Message'])
    print(message)
    (series, episode, scene, filename, url) = (message['series'], message['episode'], message['scene'], message['filename'], message['url'])
    print(series, episode, scene, filename)
    series_table = os.environ['AWS_SERIES_TABLE']
    episode_table = os.environ['AWS_EPISODE_TABLE']
    scene_table = os.environ['AWS_SCENE_TABLE']
    dynamodb = boto3.resource('dynamodb')
    series_table = dynamodb.Table(series_table)
    episode_table = dynamodb.Table(episode_table)
    scene_table = dynamodb.Table(scene_table)
    series_response = series_table.get_item(
        Key={
            'seriesId': series    
        }
    )
    if 'Item' not in series_response:
        series_table.put_item(
            Item={
                'seriesId': series,
                'name': series.title()
            }
        )

    # check to see if the episode already exists in the episode table
    # if not, it will add it. it will include a foreign key to the series table
    episode_response = episode_table.get_item(
        Key={
            'seriesId': series,
            'episodeId': episode
        }
    )
    if 'Item' not in episode_response:
        episode_table.put_item(
            Item={
                'seriesId': series,
                'episodeId': episode,
                'series_name': series.title(),
                'is_published': False
            }
        )

    # check to see if the scene already exists in the scene table
    # if not, it will add it. it will include a foreign key to the episode table
    scene_response = scene_table.get_item(
        Key={
            'sceneId': scene,
            'episodeId_seriesId': f"{episode}_{series}"
        }
    )
    if 'Item' not in scene_response:
        scene_table.put_item(
            Item={
                'sceneId': scene,
                'episodeId_seriesId': f"{episode}_{series}",
                'episode': episode,
                'scene': scene,
                'series_name': series.title(),
                'url': url,
            }
        )
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
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