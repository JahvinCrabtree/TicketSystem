# AWS Ticket System
A application that takes IT supprot tickets from teams and uses AWS SQS to then manage the tickets into seperate queues to improve an IT Support services efficiency and reliability.

## Setup
### Prerequisites

Installing the following libraries into your python environment.
This is done using `pip` install.
  - Flask
  - boto3


### Step 1 - Creating the teams channel to capture requests.

1.  Clicking the + button on the teams tab in MS teams, and then select the Create team button.
2.  Select From scratch --> Public, then give your new team a name and description, and click Create.
3.  Create a new channel in the team by clicking the ellipsis button, then Add channel.
4.  Give the channel a name and finally select the Standard access.


### Step 2. Go to [https://ngrok.com/](https://ngrok.com/) and create an account. 


1.  Follow the installation steps.
2.  In the `Deploy your app online` section, select the second tab `Static Domain`.
3.  Click the link to claim your free static domain, and save the command presented, it should look like this: `ngrok http --domain=your-domain-name.ngrok-free.app 80`
4.  When you've set it up and started running it you want to select your domain it'll be next to the `Forwarding` it'll look something like the following image.

![image](https://github.com/JahvinCrabtree/TicketSystem/assets/108539156/cfa97e42-2fbe-4b75-a330-8745c0c641a2)

5. You'll need the link that it's forwarding.


### Step 3 - Creating the outgoing webhook.

1.  Now you have your teams channel and ngrok, click the ellipsis beside the new channel.
2.  Then click the the manage team button from the dropdown.
3.  On the new page that is opened select the apps button at the top of the page. 
4.  There will be a button to `Create an outgoing webhook` select this.
5.  Name the webhook, and in the `Callback URL` insert the link from ngrok and give the webhook a relevant description.

### Step 4 - Moving over to AWS 

1.  Naviagate to the AWS IAM Console
2.  Go to `User Groups` and create a new group with a name relevant to the service TicketGroup etc.
3.  Add a permission policy to this group named `AmazonSQSFullAccess` or a custom policy that suits the needs as long as it has access to the SQS. - These should be saved in a secure place.
4.  After creating the group select the group and press `Create user` and assign them to the group.
5.  On the new users account, on the `Security credentials` tab you want to create `Access keys` - this will create a access key and a secret access key which will be used to access the queues we'll make next.
6.  Next navigate to the SQS service, and click the `Create Queue` button
7.  Create 3 Queues for the tickets to be sent into with the default queue settings

### Step 5 - Imlementing Access Keys and Changing Queue Names

1.  You want to add your access keys to the application
2.  And add your QueueURLs to the application - This can be seen in the following image.
   
![image](https://github.com/JahvinCrabtree/TicketSystem/assets/108539156/9f7bd376-2abf-440c-b629-14c7bf7d4e75)


## Deployment

1. Make sure the application is running using the flask command `flask run`
2. Run the ngrok domain using the command `ngrok http --domain=your-domain-name.ngrok-free.app 5000`

## Process

3.  Submit a ticket through MS teams

![image](https://github.com/JahvinCrabtree/TicketSystem/assets/108539156/eda0d2d7-b6dc-40d5-91e1-ec984e63cba4)

4.  If the it hits a validity check, retry with the correct format.
5.  If correct view terminal to check if the request has gone through.

![image](https://github.com/JahvinCrabtree/TicketSystem/assets/108539156/0c02790e-1bd1-4b50-9d0b-a8ae3c38660c)

6.  If the submission was successful move over to the releveant SQS queue.
7.  Press the `Send and receeive message` button
8.  Press the `Poll for messages` button to poll the queue to view the message in the queue.

