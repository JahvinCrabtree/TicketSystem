# AWS Ticket System Report. 

The task – to automate the routing and classification of IT Support tickets, leveraging AWS services to manage ticket queues.  

## The Problem 

Managing IT Support tickets is an essential part of maintaining IT Services. However, issues can arise when a system is centralized, and all tickets are sent to a single place can lead to a priority blindness or a first in first out situation where the team is flooded with tickets that they must manually filter through and work with. This could lead to a variety of issues that could include missing important tickets and having an increased time to fix tickets in general. This in turn will lead to a dissatisfaction and an overall unproductive, inefficient work environment.   

## The Approach 

The task can be broken down into individual problems as follows;  

  - Extracting the important information from the ticket, what the problem is, the priority and the description.  

  - Capturing this information from the webhook. 

  - Separating the tickets based on priority. 

  - Automatically moving tickets into the relevant queue. 

The approach for handling these tasks was to move the ticketing system to a communication channel, for this I found MS Teams to be a good fit, this is due to being able to implement outgoing webhooks this can be used to capture data using a flask application to then move the data into an SQS queue. This can later be scaled even further moving the tickets into S3 buckets and directing tickets to channels to be sorted.  

## The Solution 

### Capturing the input.  

By implementing an approach like this the tickets can be validated to make sure they meet a standard input to be managed easier. This is implemented in the backend doing various validation checks to make sure tickets are formatted correctly and don’t contain any system breaking inputs.  This approach is particularly useful for descriptions as some problem descriptions can span across multiple lines and initially the application would ignore the extra lines.  The application responds to the webhook with the correct input format if one of the validation checks fails so that the user can then redo the ticket correctly.  

The flask application has try and catch statements within it so if there is a problem with capturing the users input it can be diagnosed through the applications terminal. So that it can be troubleshooted if it's an input error, or a status issue.  Furthermore, the validation checks used are also used to separate the tickets based on the priority. This is using a system based on high, medium or low priority and can be scaled to meet different needs regarding ticket types or priorities but given the requirements having 3 priorities covered the use case.  

### Flask and Ngrok 

Flask is used to handle the API calls and as mentioned handle the priority and validation checks and then forwarding the message to the AWS SQS queues using the boto3 library. This is deployed alongside Ngrok which is what we use to forward the traffic to the application.  

### SQS Queues 

Once we have captured a valid input from the MS Teams webhook, the tickets are then moved to the correct queues, if it’s a high priority ticket it will go to a high queue and likewise for the other ticket priorities. This was the chosen approach for future expansions of the system, an SQS queue can be used alongside over AWSs features such as Lambda to automatically push the messages to different boards so that they can get dealt with; such as moving the high priority tickets directly into a slack channel to be handled as soon as possible.  

## The Challenges. 

Some of the challenges that were faced when developing this solution included correctly capturing the messages from teams, this was due to a few issues where the application wouldn’t pick up the descriptions from across multiple lines, and a few other validations checks to keep the messages easy to read and manageable. This was achieved using some regex commands and string manipulation to tidy it up using .trim and various string functions to maintain readability.  

NGrok local host, when setting up the ngrok proxy initially it wasn’t working do ngrok assuming the port the application is working off is 8080, this wasn’t a difficult fix but did require some time to investigate where it was going wrong. The solution for this was when deploying ngrok it gives you “ngrok http http://localhost:8080” for the static domain you just change the port to necessary port in this applications case it is 5000. Finding an application that would allow me to use the local application with the internet to capture the data.  
