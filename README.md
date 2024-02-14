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
3.  Add a permission policy to this group named `AmazonSQSFullAccess` or a custom policy that suits the needs as long as it has access to the SQS.
4.  After creating the group select the group and press `Create user` and assign them to the group.
5.  On the new users account, on the `Security credentials` tab you want to create `Access keys` - this will create a access key and a secret access key which will be used to access the queues we'll make next.