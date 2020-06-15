# Survey and User Feedback sample Webex Teams Bot 

This sample code implements a Webex Teams Bot which can send out surveys to obtain user feedback from multiple users
organized in "Channels".   
The surveys are received by the end users as Adaptive Cards with buttons. They can be free form or multiple choice questions  
Once users submit their answers, the bot administration component (Django application) provides reports for the survey
results.  


## Contacts
* Marcel Neidinger (mneiding@cisco.com)
* Gerardo Chaves (gchaves@cisco.com)
* Max Acquatella (macquate@cisco.com)

## Solution Components
*  Cisco Webex Teams
*  Python 3
*  Django
*  Docker

## Installation/Configuration

To install and run this sample code , it is assumed that you are familiar with the Python 3 language, 
(https://www.python.org/about/) the PIP package manager (https://www.w3schools.com/python/python_pip.asp) 
and the Django framework (https://www.djangoproject.com/).  
You need to have Python 3.7 or later with it's corresponding PIP tools installed on your test environment. 
The Django libraries are "imported" by the code when testing locally and also built by Docker when packaging the sample
for running in a set of containers. 


### Generate Webex Teams Bot and and obtaining access token

This sample is meant to be used with a Webex Teams Bot. 

If you don't already have a Cisco Webex account, go ahead and register for one.  They are free.  
You'll need to start by adding your bot to the Cisco Webex website.

[https://developer.webex.com/my-apps](https://developer.webex.com/my-apps)

1. Click on "Create a New App" 
2. Click on "Create a Bot"
3. Fill out all the details about your bot. You might want to give it a Name and UserName that reflects how you intend to use it so 
end users can recognize it easily such as "ACMESurveyBot" or something else that is unique to your organization. 
4. Click "Add Bot" and make sure to copy your bot access token! You will need this later.

Here is a more complete guide on creating and using bots:  
https://developer.webex.com/docs/bots  

This Blog gives you more step by step instructions:    
https://developer.webex.com/blog/from-zero-to-webex-teams-chatbot-in-15-minutes


## Development testing installation on local machine with SQLLite, no container and ngrok for webhook address

Follow these steps to setup your environment to run in debug mode locally using SQLLite for the database and ngrok 
for the webhook address: 

1. Install virtual env:  
```python3 -m venv .env```   

2. Install requirements:  
```pip install -r requirements.txt```  

3. Set the database to debug mode:  
Edit file **evy_light/settings.py** to hard-code the DEBUG setting to True.  
The file in the repository shows the following:  
```DEBUG = int(os.environ.get('DJANGO_DEBUG', default=0))```  
Change that temporarily to:  
```DEBUG = True```
This will use the SQLLite libraries to generate a local **db.sqlite3** file and use the SQLLite DB engine instead of 
Postgres which is what the sample uses when running in a container. 

4. Enable local sqllite database
Issue the following coomand in the command line:  
```python3 manage.py migrate```

5. Set the access token as an environment variable
```export WEBEX_ACCESS_TOKEN="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"```  
NOTE: no spaces between the = sign and the inputs, enclose the token in ""

6. Register the bot's webhook
First make sure that step 2 above is satisfied so that the webhooksimple library is installed.  
Then, if you are running locally behind a firewall and do not have an external URL with HTTPS that maps to your  
server, you can use the ngrok tool (https://ngrok.com/). Once you have it installed on your local machine where  
you will running the Django application, issue the following command to establish a tunnel:  
```ngrok http 8080```  
NOTE: the port must correspond to the port use when enabling manage.py run server 8080  
Now copy the https forwarding address that the tool generates and use it to edit the "target_url:" field  
int the **hooks.yml** file:  
```
hooks:
    - name: "attachment actions hook"
      resource: "attachmentActions"
      event: "created"
      target_url: "<ngrok provided url HERE>/webhooks/attachmentActions"
```  
Next, make a copy of the **vars.yml.tpl** template file named **vars.yml** to add the Webex Teams Bot authorization token 
so that the webhooksimple library can register the webhooks.
NOTE: The webhooksimple library and it's documentation can be found at https://github.com/ciscoSE/webhooksimple  
Place the authorization token within quotes instead of the <add access token here> as shown below.
Also provide the same ngrok URL as above, but just the base URL:  
```
adapter:
    name: WebexTeamsWebhookManager
    authentication:
      access_token: "XXXXXXXXXXXXXXXXXX"
    parameters:
  
  # Add your variables from here on
remote_prefix: "<ngrok provided url HERE>"
```  
Now you can issue the command to register the webhooks:  
```
python3 -m webhooksimple setup
```



## Production installation with Postgres and Docker container hosted with external URL for webhook


Edit the **hooks.yml** file as described in development installation instructions above to add the URL of where the 
containerized Django application will be running (external HTTPS URL using CA issued certificate)  in the target_url:
field (remote_prefix)

Make a copy of the **vars.yml.tpl** template file named **vars.yml** and edit it as described in development installation instructions above to add the Webex Teams Bot access token 
in the access_token: field and the external URL of where the sample is running in the container in the remote_prefix: field

Copy the **docker-compose.yml.tpl** file to **docker-compose.yml** and fill out the corresponding Postgres
and Django environment variables to use. 

Use included **Dokerfile** to build and run the container

## Usage

To run the script locally use: 
```python3 manage.py runserver 8080```

To run in a the docker container, use the appropriate ``docker run`` command 

Once you have the Django application running, be it locally in development testing mode or in production using the container
, open the /receiver page with a web browser.  

Sample URL to open with a browser when running locally:  
http://127.0.0.1:8080/receiver

You are initially shown the "User Management" tab which is a good starting point to create "Receivers" that will be the  
target of surveys that are organized in "Channels". 

Below is a description of the operations you can perform on each "Tab" you see on the main page on the upper right, or under  
a "hamburger menu" if you screen size cannot fit the full names of the tabs

### User Management

Here you create "Channels", create "Receivers" and associate them with each other.
A Channel is a grouping of receivers that is used to send out the surveys. 
A receiver is Webex Teams end user that will receive the survey in the form of a message from the Bot with a card that 
has all the questions that form part of the particular survey.  


### Create QuestionSet

This is where you create a question set to send out to a "channel".  
NOTE: The order in which the questions are created is not used to order the questions in the card. 

For multiple choice questions, you must write the question using followed by the choices as comma separated strings
within parenthesis. Example:
"how are you doing today? (bad, average, good, great)" 

### List QuestionSets

This is where you send out the surveys using the "Send" button next to each survey and come back to 
check on the answers by clicking on the "View Report" button for each one. 

Once you are in the "View Report" page, you are given the option to download the data to a .CSV file using the
"Download Data" button. 


## Data Management

At the moment there are no web pages in the application to manage surve or user data beyond initial creation. 

In order to delete all QuestionSets/Surveys, you must reset the Database manually as if you were re-installing the sample  
application, but that will remove all Recipient, Channel and QuestionSet data.

You can also manipulate the database using another tool, but care must be taken to follow the rules defined in  
**entities/models.py** to keep DB integrity. 

If you are done running tests, you might also want to remove any webhooks associated to the bot for this application  
using using the webhooksimple commands from the library. 


## API

The sample application has a REST based API at /api/v0/ which is not fully documented, but simple enough  
so that you can use the various commands to do things like exporting QuestionSets to modify and create new ones  
and add further functionality. 

You can browse through the available calls by pointing your browser to:  
http://127.0.0.1:8080/api/v0/  
(in case of running locally)  

# Screenshots

![/IMAGES/Receivers.png](/IMAGES/Receivers.png)

![/IMAGES/AddToChannel.png](/IMAGES/AddToChannel.png)

![/IMAGES/CreateQuestionSet.png](/IMAGES/CreateQuestionSet.png)

![/IMAGES/ListQuestionSets.png](/IMAGES/ListQuestionSets.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.






