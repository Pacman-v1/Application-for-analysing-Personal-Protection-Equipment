<!-- ABOUT THE PROJECT -->
## About The Project

<img src="img/AWS Flowchart.jpg">

This application is designed implemented to analyse an image and detect Personal Protection Equipment (PPE) using AWS Rekognition (AI services).

Here's how:
* Resource creation using Boto3
* Image upload to S3 and Lambda trigger from SQS
* PPE Detection with Rekognition
* Database Updates and SMS Notification

Of course, its also important to discuass the security accesses used that will be discussed later on.

<p align="right">(<a href="#top">back to top</a>)</p>

### Built with

* S3
* SQS
* SMS Message
* Rekognition
* DynamoDB
* Lambda


<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## 1. Resource creation with Boto3

The S3 bucket and SQS queue are created using the python cocde in the createS3Bucket file. The code sets the bucket_name and once successfullly created a statement indicating the bucket was successfully created is returned

## 2. Image upload to S3 and Lambda trigger from SQS

The Python application (Boto3) uploads images one after the other at 10 secs interval to the S3 bucket taking in three attributes
* file_pat is the file to be uploaded
* bucket is the name of the bucket to upload 
* image_name is the S3 object(image) name
*
  ```sh
  for equipment_type in equipment:
                        types = equipment_type["Type"]
                        confidence = equipment_type["Confidence"]
                        covers_body = equipment_type["CoversBodyPart"]["Value"]

                        person_details = {
                            "Confidence": confidence,
                            "Cover Type": types,
                        }
                        covered = covers_body
  ```

## 3. PPE Detection with Rekognition

The Lambda function code in Python (Boto3) extracts the relevant details such as image name etc. from the SQS message. The image details are then sent by the Lambda code to the AWS Rekognition service for detecting ‘face cover’ and ‘head cover’.

```sh
  for equipment_type in equipment:
                        types = equipment_type["Type"]
                        confidence = equipment_type["Confidence"]
                        covers_body = equipment_type["CoversBodyPart"]["Value"]

                        person_details = {
                            "Confidence": confidence,
                            "Cover Type": types,
                        }
                        covered = covers_body
  ```

## 4. Database Updates and SMS Notification

The DynamoDB database has a single table with only a single partition (primary) key as the image name. From the Rekognition response (part 3 above), the Lambda function extracts relevant information and save true/false for the presence/absence of a face cover and a head cover together with the confidence level in the DynamoDB table.

For responses indicating absence of a face mask, the Lambda function immediately notifies a given telephone number using SMS.
```sh
  sns.publish(PhoneNumber = '+256000000000', Message = str(img))
  ```

<p align="right">(<a href="#top">back to top</a>)</p>
