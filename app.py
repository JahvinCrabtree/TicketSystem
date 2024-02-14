import re
from flask import Flask, jsonify, request
import json
import os
from dotenv import load_dotenv
load_dotenv()
import boto3

aws_region = 'us-east-1'

sqs_client = boto3.client(
    'sqs',
    region_name=aws_region,
    aws_access_key_id=os.environ["ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["SECRET_ACCESS_KEY"]
)

sqs_high_queue_url = 'https://sqs.us-east-1.amazonaws.com/211125347201/HighQueue'
sqs_mid_queue_url = 'https://sqs.us-east-1.amazonaws.com/211125347201/MidQueue'
sqs_low_queue_url = 'https://sqs.us-east-1.amazonaws.com/211125347201/LowQueue'

app = Flask(__name__)

def is_valid_title(title):
    return bool(title) and len(title.split()) <= 10

def is_valid_priority(priority):
    return bool(priority) and priority.lower() in ["high", "medium", "low"] 

def is_valid_description(description):
    return bool(description) and re.fullmatch(r'[\s\S]*', description)

def validate_ticket_data(title, priority, description):
    validation_results = {
        "title": is_valid_title(title),
        "priority": is_valid_priority(priority),
        "description": is_valid_description(description),
    }

    validation_results["title"] = validation_results["title"] and bool(title and title.strip())
    validation_results["priority"] = validation_results["priority"] and bool(priority and priority.strip())
    validation_results["description"] = validation_results["description"] and bool(description and description.strip())

    return validation_results

@app.route("/", methods=["POST"])
def hook():
    data = json.loads(request.data)

    response_message = {
        "type": "message",
        "text": """Input missing - please refer to this template \n
        Title: Example Title
        Priority: High, Medium or Low.
        Description: A description for the problem. """
    }

    if "text" in data:
        text_content = data["text"]

        # Use regular expressions to extract information
        title_match = re.search(r'Title: (.+)', text_content)
        title = title_match.group(1) if title_match else None

        priority_match = re.search(r'Priority: (\w+)', text_content, re.IGNORECASE)
        priority = priority_match.group(1).strip().lower() if priority_match else None

        description_match = re.search(r'Description: (.+)', text_content, re.DOTALL)
        description = description_match.group(1) if description_match else None

        # Validate each piece of data individually
        validation_results = validate_ticket_data(title, priority, description)

        # Check validation results and respond accordingly
        
        if all(validation_results.values()):
            if priority == "high":
                sqs_queue_url = sqs_high_queue_url
            elif priority == "medium":
                sqs_queue_url = sqs_mid_queue_url
            else:
                sqs_queue_url = sqs_low_queue_url
            
            try:
                sqs_client.send_message(
                    QueueUrl=sqs_queue_url,
                    MessageBody=json.dumps({"title": title, "priority": priority, "description": description})
                )
                response_message = {
                    "type": "message",
                    "text": f"The ticket has been received.<br>Title: {title}<br>Priority: {priority}<br>Description: {description}"
                }
            except Exception as e:
                print(f"Error sending message to SQS: {e}")               

    return jsonify(response_message)

if __name__ == "__main__":
    app.run()
