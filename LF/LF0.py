import boto3
import json


def lambda_handler(event, context):
    print(event)
    client = boto3.client('lex-runtime')
    inputTexttext = event['message']
    print(inputTexttext)
    response = client.post_text(
        botName='DiningChatBot',
        botAlias='$LATEST',
        userId='string',
        inputText=inputTexttext
    )
    # respose = response.replace("'",'"')
    print(type(response))
    r1 = response["message"]
    print(r1)
    r1_j = json.dumps(r1)
    print(r1_j)
    r2 = json.dumps(response)
    print(type(r2))
    # r3 = r2.message
    print(r2)
    # messg=json.stringify(r)
    # #response = '{%s}' % ', '.join(['"%s": "%s"' % (k, v) for k, v in response.items()])

    # #response = {"ResponseMetadata": {"RequestId": "4cf07927-ad7b-41b9-84c1-011ab45e4f5a", "HTTPStatusCode": 200, "HTTPHeaders": {"content-type": "application/json", "date": "Fri, 13 Mar 2020 14:41:45 GMT", "x-amzn-requestid": "4cf07927-ad7b-41b9-84c1-011ab45e4f5a", "content-length": "315", "connection": "keep-alive"}, "RetryAttempts": 0}, "intentName": "GreetingIntent", "slots": {}, "sessionAttributes": {}, "message": "Hey! I am DineBot.  What can I do for you today? ", "messageFormat": "SSML", "dialogState": "Fulfilled", "sessionId": "2020-03-13T14:36:43.644Z-qAGxHIQU"}

    # # print(inputTexttext)
    # # print(r)
    # print(messg)
    # stringify=json.stringify(response)
    # print(stringify)
    # r=(response["message"])
    # r1=json.dumps(r)
    # print(type(r1))
    # print(response["message"])
    # r3 = r2.message
    # print(r3)
    return r1_j
