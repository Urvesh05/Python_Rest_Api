
import json
import logging
import uuid
import boto3

dynamodb = boto3.resource('dynamodb')
dynamodbTbale= 'python_serverless'
table = dynamodb.Table(dynamodbTbale)


# Save data from Database
def postData(event, context):
    data = json.loads(event['body'])
    if 'name' not in data:
        logging.error('Validation failed')
        raise Exception('cannot create items!.')

    item = {
        'id': str(uuid.uuid1()),
        'name':data['name'],
        'lname':data['lname']
    }
    table.put_item(Item=item)

    response = {
        "statusCode":200,
        "body":json.dumps(item)
    }
    return response


# Get Data from Database
def getData(event, context):
    print(event,"-------------")
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'])
    }

    return response


# Delete Data from database
def deleteData(event, context):
   
    table.delete_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    # create a response
    response = {
        "statusCode": 200,
        'body': 'Deleted item' 
    }

    return response


# Update data from databse
def updateData(event, context):
    data = json.loads(event['body'])
    
    result = table.update_item(
        Key={
            'id': event['pathParameters']['id']
        },
        ExpressionAttributeNames={
          '#N': 'lname',
        },
        ExpressionAttributeValues={
          ':lname': data['lname'],
          
        },
        UpdateExpression='SET #N = :lname',
                         
        ReturnValues='ALL_NEW',
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Attributes'])
                           
    }

    return response