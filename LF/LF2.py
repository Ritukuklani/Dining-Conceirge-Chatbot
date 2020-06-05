from __future__ import print_function
import json
import random
import boto3
import urllib3
from botocore.vendored import requests


def get_random_business_id(cuisine_type):
    http = urllib3.PoolManager()
    es_query = "https://search-es-restaurant-domain-fjlnyb4olzxswem7scgg7jm6dy.us-east-1.es.amazonaws.com/restaurants/_search?q={cuisine}&size={size_limit}".format(
        cuisine=cuisine_type,
        size_limit=10
        )
    response = http.request('GET', es_query)
    result = json.loads(response.data.decode('utf-8'))
    print(result)

    random_num_list = list(range(10))
    random.shuffle(random_num_list)
    for random_number in random_num_list:
        if result['hits']['hits'][random_number]['_source']['businessId'] != None:
            businessId = result['hits']['hits'][random_number]['_source']['businessId']

    return businessId # string


#Get restaurant info from DynamoDB based on businessId sent from ElasticSearch

def get_restaurant_info(businessId):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('yelp-restaurants')
    response = table.get_item(
        Key={
            'businessId': businessId
        }
    )
    response_item = response.get("Item")
    restaurant_name = response_item['name']
    restaurant_category = response_item['category']
    restaurant_address = response_item['address']
    restaurant_city = response_item['city']
    restaurant_zipcode = response_item['zipcode']
    restaurant_rating = str(response_item['rating'])
    restaurant_url = str(response_item['url'])
    restaurant_phone = response_item['phone']
    formatted_restaurant_info = restaurant_name+" "+restaurant_phone+'\n'+"Rating: "+restaurant_rating+", "+restaurant_address+", "+restaurant_city+", "+restaurant_zipcode+" "+restaurant_url

    return formatted_restaurant_info # string type



def lambda_handler(event, context):
    # for record in event['Records']:
    #   print ("test")
    #   payload=record["body"]
    #   print(str(payload))
    # print(event)

    # print("Testing CloudWatch: Call LF2 every minute.")
    # # 1. pulls a message from the SQS queue
    # # Create SQS client
    # sqs = boto3.client('sqs')
    # # Get URL for SQS queue
    # response = sqs.get_queue_url(QueueName='Q1')
    # print(response)
    # queue_url = response['QueueUrl']
    # print(queue_url)
    # message = None
    # # Receive a message from SQS queue
    # resp = boto3.client('sqs')
    # print(resp)
    # resp = sqs.receive_message(
    #     QueueUrl=queue_url,
    #     AttributeNames=[
    #         'SentTimestamp'
    #     ],
    #     MaxNumberOfMessages=1,
    #     MessageAttributeNames=[
    #         'All'
    #     ],
    #     VisibilityTimeout=0,
    #     WaitTimeSeconds=0
    # )
    # # try:
    # print(resp)
    # message = resp['Messages'][0]
    # print(message)
    # receipt_handle = message['ReceiptHandle']
    # # Delete received message from queue
    # sqs.delete_message(
    #     QueueUrl=queue_url,
    #     ReceiptHandle=receipt_handle
    # )
    # print('Received and deleted message: %s' % message)
    # # 2. gets a random restaurant recommendation for the cuisine collected through conversation from ElasticSearch
    # print(message['Body'])
    # # all information stored in sqs queue
    # location = message['MessageAttributes']['location']['StringValue']
    # cuisine = message['MessageAttributes']['cuisine_type']['StringValue']
    # dining_date =  message['MessageAttributes']['date']['StringValue']
    # num_people = message['MessageAttributes']['number_of_people']['StringValue']
    # print(location, cuisine, dining_date, num_people)

    # except:
    #     print("SQS queue is now empty")

    message_attributes = event['Records'][0]['messageAttributes']
    print(message_attributes)

    location = message_attributes['location']['stringValue']
    cuisine = message_attributes['cuisine_type']['stringValue']
    dining_date = message_attributes['time']['stringValue']
    num_people = message_attributes['number_of_people']['stringValue']
    phone = message_attributes['phone_number']['stringValue']
    print(location, cuisine, dining_date, num_people, phone)
    
    if cuisine == "indian":
        cuisine = "indpak"
    
    restaurant_info = ""
    for i in range(1, 4):
        restaurantId = get_random_business_id(cuisine)
        restaurant_info += get_restaurant_info(restaurantId) + '\n' + '\n'
        
    if cuisine == "indpak":
        cuisine = "indian"
    
    sendMessage = "Here are the details for the cuisine '{}' you asked for: {}".format(cuisine, restaurant_info)
    sns = boto3.client('sns')
        # send message
    sns.publish(
        PhoneNumber = '+1'+phone,
        Message = sendMessage
    )
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda LF2!')
    }
  