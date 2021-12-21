# Import the relevant libraries
import json
import boto3

def lambda_handler(event, context):
    # Create/initialise resources 
    sns = boto3.client('sns')
    rek = boto3.client('rekognition')
    table = boto3.resource('dynamodb').Table('rekog-DynamoDB-cpd-s1903348')
    
    #Loops through every file uploaded
    for message in event["Records"]:
        #pull the body out & json load it
        content=(message["body"])
        content=json.loads(content)
        
        #checks if records exist
        #then gets the bucket name and the image name from the records
        if 'Records' in content:
            bucket = content["Records"][0]["s3"]["bucket"]["name"]
            img = content["Records"][0]["s3"]["object"]["key"]
            response = rek.detect_protective_equipment(
                    #Call to rekognition to process the image (img)
                    Image={"S3Object": {"Bucket": bucket, "Name": img}},
                    SummarizationAttributes={
                        "MinConfidence": 85,
                        "RequiredEquipmentTypes": ["FACE_COVER", "HEAD_COVER"]
                    })

            
            # extracting the reply
            # bf= Body Features
            # manipulating the response from rekognition to filter out only information that is needed
            for person in response['Persons']:
                bf = person['BodyParts']
                
                # An empty array to store the data after filtering
                result = {'Features':[]}

                # loops through the response
                # captures the Name (of the body part) and Equipment Detections
                # and stores it
                for detections in bf:
                    name = detections['Name']
                    equipment= detections['EquipmentDetections']

                    for equipment_type in equipment:
                        types = equipment_type["Type"]
                        confidence = equipment_type["Confidence"]
                        covers_body = equipment_type["CoversBodyPart"]["Value"]

                        person_details = {
                            "Confidence": confidence,
                            "Cover Type": types,
                        }
                        covered = covers_body
                    
                    # prepares data for dynamoBD table 
                    # Adds the image (img) name as the key
                    # and the results from the AWS Rekognition analysis to dynamoDB
                    data = {'Body Part': name, 'Details': str(person_details), 'Covered': covered}
                    result['Features'].append(data)
                    
                    # stores the date captured into dynamoDB
                    table.put_item(Item={"img_name": img, 'Image Analysis': result})

                    #An SMS is sent to the phone number listed below
                    sns.publish(PhoneNumber = '+256000000000', Message = str(img))
            
    return {"statusCode": 200}
