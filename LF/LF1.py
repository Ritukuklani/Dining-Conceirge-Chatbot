import json
import math
import dateutil.parser
import datetime
import time
import os
import logging
import boto3

    
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

client = boto3.client('sqs')

def lambda_handler(event, context):
    # TODO implement
    # return {
    #     'statusCode': 200,
    #     'body': json.dumps('Hello from Lambda!')
    # }
    # a = json.stringify(event)
    # print(a)
    print(event)
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event)
    
def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']
    print(intent_name)
    # Dispatch to your bot's intent handlers
    if intent_name == 'DiningSuggestionsIntent':
        return dining_suggestions_intent(intent_request)
    elif intent_name == 'GreetingIntent':
        return greeting_intent(intent_request)
    elif intent_name == 'ThankYouIntent':
        return thankyou_intent(intent_request)
    raise Exception('Intent with name ' + intent_name + ' not supported')
    
def get_slots(intent_request):
    return intent_request['currentIntent']['slots']


def validate_dining_suggestions(cuisine_type, location, time, number_of_people, phone_number):
    cuisine_types = ['indian', 'italian', 'korean', 'chinese', 'japanese', 'mexican', 'french', 'thai', 'veitnamese', 'caribbean', 'turkish']
    if cuisine_type is not None and cuisine_type.lower() not in cuisine_types:
        return build_validation_result(False,
                                       'cuisine',
                                       'We do not have "{}", would you like a different type of cuisine? The most popular cuisine is Indian'.format(cuisine_type))
    
    location_types = ['manhattan', 'brooklyn', 'queens', 'Sunset Park', 'Edgewater', 'Bensonhurst', 'Jackson Heights', 'Union City', 'Fairview', 'Crown Heights', 'Staten Island', 'Astoria', 'Sunnyside', 'Long Island City']
    if location is not None and location.lower() not in location_types:
        return build_validation_result(False,
                                       'location',
                                       'We do not have suggestions for "{}", would you like to try a different location? The most popular location is Manhattan.  '.format(location))
    
    if time is not None:
        if len(time) != 5:
            # Not a valid time; use a prompt defined on the build-time model.
            return build_validation_result(False, 'time', None)

        hour, minute = time.split(':')
        hour = parse_int(hour)
        minute = parse_int(minute)
        
        if math.isnan(hour) or math.isnan(minute):
            # Not a valid time; use a prompt defined on the build-time model.
            return build_validation_result(False, 'time', None)

        if hour < 10 or hour > 24:
            # Outside of business hours
            return build_validation_result(False, 'time', 'Our business hours are from 10 a m. to 12 p m. Can you specify a time during this range?')
            
    if number_of_people is not None:
        number_of_people = parse_int(number_of_people)
        if number_of_people < 0 or number_of_people > 20:
            return build_validation_result(False, 'numberofpeople', 'Sorry! We accept reservations only upto 20 people')
    
    if phone_number is not None:
        if len(phone_number) != 10:
            return build_validation_result(False, 'phonenumber', 'You have entered an invalid phone number. Please enter a valid phone 10 digit phone number.')

    return build_validation_result(True, None, None)
    

def parse_int(n):
    try:
        return int(n)
    except ValueError:
        return float('nan')


def build_validation_result(is_valid, violated_slot, message_content):
    if message_content is None:
        return {
            "isValid": is_valid,
            "violatedSlot": violated_slot,
        }

    return {
        'isValid': is_valid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content}
    }    


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }


def close(session_attributes, fulfillment_state, message):
    
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }
    
    return response


def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }

def dining_suggestions_intent(intent_request):
    
    cuisine_type = get_slots(intent_request)["cuisine"]
    location = get_slots(intent_request)["location"]
    time = get_slots(intent_request)["time"]
    number_of_people = get_slots(intent_request)["numberofpeople"]
    phone_number = get_slots(intent_request)["phonenumber"]
    
    source = intent_request['invocationSource']
    
    if source == 'DialogCodeHook':
        slots = get_slots(intent_request)

        validation_result = validate_dining_suggestions(cuisine_type, location, time, number_of_people, phone_number)
        if not validation_result['isValid']:
            slots[validation_result['violatedSlot']] = None
            return elicit_slot(intent_request['sessionAttributes'],
                               intent_request['currentIntent']['name'],
                               slots,
                               validation_result['violatedSlot'],
                               validation_result['message'])
        
        output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
        return delegate(output_session_attributes, get_slots(intent_request))
        
    elif source == 'FulfillmentCodeHook':
        
        sqs = boto3.client('sqs')
        
        response = sqs.get_queue_url(QueueName='Q1')
        queue_url = response['QueueUrl']
        print(queue_url)
        
        print(location, cuisine_type, time, number_of_people, phone_number)
        
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageAttributes={
                'location': {
                        'DataType': 'String',
                        'StringValue': location
                    },
                'cuisine_type': {
                        'DataType': 'String',
                        'StringValue': cuisine_type
                    },
                'time': {
                        'DataType': 'String',
                        'StringValue': time
                    },
                'number_of_people': {
                        'DataType': 'String',
                        'StringValue': number_of_people
                    },
                'phone_number': {
                        'DataType': 'String',
                        'StringValue': phone_number
                    }
            },
            MessageBody=(
                'Information about the user inputs to the bot'
            )
        )
        
        print("SQS messageID:"+str(response['MessageId']))
        
        
        return close(intent_request['sessionAttributes'],
                     'Fulfilled',
                     {'contentType': 'PlainText',
                      'content': "You're all set. Expect restaurant suggestions on your +1- {} shortly".format(phone_number)})
        
        # return {
        #     "dialogAction": {
        #         "type": "Close",
        #         "fulfillmentState": "Fulfilled",
        #         "message": {
        #           "contentType": "SSML",
        #           "content": "I didn't get you. Can you please repeat that?"
        #         },
        #     }
        # }



 




def greeting_intent(intent_request):
    
    return {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
              "contentType": "SSML",
              "content": "Hey! I am DineBot.  What can I do for you today? "
            },
        }
    }
    
def thankyou_intent(intent_request):
    
    return {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
              "contentType": "SSML",
              "content": "Nice to talk to you! Thank you and visit again!  "
            },
        }
    }
    

    # MessageSystemAttributes={
    #     'string': {
    #         'StringValue': 'string',
    #         'BinaryValue': b'bytes',
    #         'StringListValues': [
    #             'string',
    #         ],
    #         'BinaryListValues': [
    #             b'bytes',
    #         ],
    #         'DataType': 'string'
    #     }
    # },
    # MessageDeduplicationId='string',
    # MessageGroupId='string'

    