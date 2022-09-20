import requests
from pytz import timezone
from datetime import datetime
from dateutil.tz import tzlocal
import boto3


def lambda_handler(event, context):

    response = requests.get("https://monitoringapi.solaredge.com/site/SITE_ID/overview.json?api_key=REPLACE_WITH_SOLAREDGE_API_KEY")

    message=""
    try:
        lastUpdateTimeStr = response.json()["overview"]["lastUpdateTime"]
        message = message + "Solaredge account last updated: "+lastUpdateTimeStr+".\n"
        now = datetime.now(tzlocal())
        lastUpdateTime = datetime.fromisoformat(lastUpdateTimeStr)
        sinceLastUpdate = now.timestamp()-lastUpdateTime.timestamp()
        minsSinceLastUpdate = int(sinceLastUpdate/60)
        message = message + "Mins since last update: " +str(minsSinceLastUpdate)+".\n"
    except Exception:
        message = "Error retrieving last updated time.\n"
        send_mail(message)

    if (minsSinceLastUpdate > 60):
        message += "Error: Not updated in under 60 minutes."
        send_mail(message)
    else:
        message += "Updated in under 60 minutes."

    body = {
        "message": message,
        "rsp": response.text
    }

    return {"statusCode": 200, "body": message}

def send_mail(body):
    
    ses = boto3.client('ses')
    body += "\n\nGenerated from AWS Lambda."

    ses.send_email(
	    Source = 'FROM@EMAIL.COM',
	    Destination = {
		    'ToAddresses': [
			    'TO@EMAIL.COM'
		    ]
	    },
	    Message = {
		    'Subject': {
			    'Data': 'Solaredge Connection Monitoring',
			    'Charset': 'UTF-8'
		    },
		    'Body': {
			    'Text':{
				    'Data': body,
				    'Charset': 'UTF-8'
			    }
		    }
	    }
    )