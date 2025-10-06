import json
import boto3
import os
import random
from urllib.parse import unquote_plus

# Define your region
AWS_REGION = "eu-central-1"

# --- Initialize AWS clients with explicit region --- #
rekognition_client = boto3.client('rekognition', region_name=AWS_REGION)
sms_client = boto3.client('pinpoint-sms-voice-v2', region_name=AWS_REGION)

# --- Configuration --- #
SENDER_ID = 'KOALASPOTTR' 
RECIPIENT_PHONE = os.environ.get('RECIPIENT_PHONE') 

# --- Helper functions --- #
def generate_koala_joke():
    """Generates a random koala-themed joke with emoticons."""
    jokes = [
        "Why do koalas make great supervisors? Because they're experts in koala-ty control! 🐨✔️",
        "What's a koala's favorite drink? A Koka-Koala! 🥤🐨",
        "How do you know when a baby koala is happy? It jumps for joey! 🤗",
        "Why aren't koalas considered real bears? They don't meet the koala-fications! 📝😂",
        "What do you call a lazy koala? A pouch potato! 🥔😴",
        "How do koalas stay in shape? They do bear-obics! 🤸‍♂️🐨",
        "What happened when the koala tripped in a restaurant? He got embearassed! 😳",
        "Why did the manager hire the marsupial? Because he was koala-fied for the job! 👨‍💼👍",
        "What's a koala's favorite car? A Furr-ari! 🚗💨",
        "Where do all the famous koalas live? In Hollywood, Koala-fornia! 🌟🎬"
    ]
    return random.choice(jokes)

def extract_capitalized_name_from_bucket(bucket_name):
    """Extracts and capitalizes the first and last name from a bucket name."""
    # Expected format: "firstname-lastname-koala-bucket"
    try:
        parts = bucket_name.split('-')
        first_name = parts[0].capitalize()
        last_name = parts[1].capitalize()
        return f"{first_name} {last_name}"
    except IndexError:
        # Fallback if the bucket name doesn't match the expected format.
        return "Workshop User"

# --- Core Logic --- #
def lambda_handler(event, context):
    # 1. PERCEIVE: Get the uploaded image details from the S3 trigger event.
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    
    # URL decode the object key to handle special characters (spaces, +, @, etc.)
    object_key = unquote_plus(event['Records'][0]['s3']['object']['key'])
    
    # Dynamically get the user's name from the bucket name.
    USER_NAME = extract_capitalized_name_from_bucket(bucket_name)
    
    print(f"New image detected: {object_key} in bucket {bucket_name}")

    try:
        # 2. THINK: Use Rekognition to analyze the image.
        response = rekognition_client.detect_labels(
            Image={'S3Object': {'Bucket': bucket_name, 'Name': object_key}},
            MaxLabels=10,
            MinConfidence=70
        )
        
        # Extract label names for easy checking
        labels = [label['Name'] for label in response['Labels']]
        print(f"Rekognition detected labels: {labels}")

        # Core Agent Logic: Is it a Koala?
        if 'Koala' in labels:
            # 3. ACT (Happy Path): Send a success SMS.
            print("It's a Koala! Sending a happy SMS.")
            message = (f"🎉 {USER_NAME}, SUCCESS! "
                      f"You sent me a Koala! I love this picture. "
                      f"You have made me a very happy agent. 🐨❤️ "
                      f"- Your Koala Agent")
        else:
            # 3. ACT (Rejection Path): Send a rejection SMS with a koala joke.
            print("Not a Koala. Sending a polite rejection with a joke.")
            
            joke = generate_koala_joke()
            
            message = (f"🤔 Hi {USER_NAME}, "
                      f"Thank you for the upload, but that is not a Koala. "
                      f"I only want Koalas! Please try again. "
                      f"Here's a joke to cheer you up: {joke} "
                      f"- Your (Still Hopeful) Koala Agent")

        # Send the SMS using AWS End User Messaging
        sms_response = sms_client.send_text_message(
            DestinationPhoneNumber=RECIPIENT_PHONE,
            OriginationIdentity=SENDER_ID,
            MessageBody=message,
            MessageType='TRANSACTIONAL'
        )
        
        print(f"SMS sent successfully. Message ID: {sms_response['MessageId']}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {'statusCode': 500, 'body': json.dumps(str(e))}

    return {'statusCode': 200, 'body': json.dumps('Agent has completed its task.')}
    
