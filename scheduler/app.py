import json
import boto3
import os
import datetime

current_time = datetime.now()

def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    table = _get_table()
    data = _get_server_data(table)
    for server in data:
        update_server(server)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
        }),
    }

def _get_table():
    dynamodb = boto3.resource('dynamodb')
    database_name = os.environ['DATABASE_NAME']
    return dynamodb.Table(database_name)

def _get_server_data(table):
    return table.scan(ProjectionExpression='Id,Schedule,Server_State')['Items']

def update_server(server):
    if not 'Schedule' in server:
        return

    # Get start and stop time of server
    start_time_str: str = server['Schedule']['M']['Start-Time']['S']
    start_time: datetime.time = datetime.strptime(start_time_str, "%H:%M").time()
    stop_time_str: str = server['Schedule']['M']['Stop-Time']['S']
    stop_time: datetime.time = datetime.strptime(stop_time_str, "%H:%M").time()

    # Value will be true if the stop time is later in the day than the start time
    # This will help determine if the server should be on if the time of day is between the start and stop times
    stop_after_start: bool = stop_time > start_time

    # True if the server should be online at the current time
    should_be_online: bool = None
    if stop_after_start:
        # If current time is between start and stop times
        should_be_online = (current_time > start_time and current_time < stop_time)
    else:
        # If current time is either after start time or before stop time
        # Since stop time must be before start time, this is the same as checking if the start time is not between stop and start times
        should_be_online = (current_time > start_time or current_time < stop_time)

    # Is server currently online (according to the server state in the database)
    server_online = is_server_online(server)

    if (should_be_online and not server_online):
        start_server(server)
    elif (server_online and not should_be_online):
        stop_server(server)
    
def start_server(server):
    # TODO: Make call to lambda function
    pass

def stop_server(server):
    # TODO: Make call to lambda function
    pass

def is_server_online(server):
    # TODO: Check state of server and
    False
