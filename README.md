# solaredge-conmonitor

This aws lambda project monitors solar power generation using the solaredge api at a particular time during the day and ensures that the system has been updated within the past hour. If not, an email is sent.\
You will need AWS SAM installed and configured.

## Modifications

Roles: Create a role (e.g. LambdaSESRole) with  the following inside it: \
1)AWSLambdaBasicExecutionRole\
2)Your own policy (e.g. LambdaSESPolicy) with email sending priviledges.
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ses:SendEmail",
                "ses:SendRawEmail"
            ],
            "Resource": "*"
        }
    ]
}
```

In template.yaml, replace the LambdaSESRole with yours & change the rate to whatever schedule you wish. You will also need to make sure the timezone (TZ) matches the timezone your solaredge account is set to (usually the timezone where the panels are located)\
In app.py, replace the solaredge site id & api key in the url along with the from and to email addresses and make sure SES has verified the emails you wish to use.

### Deploy the sample application


sam build\
sam deploy --guided

If not deploying from an administrative account, then your aws user will need to be part of a code deployment group which has a policy (e.g. ServerlessDeploymentPolicy) with teh following permissions:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "iam:GetRole",
                "iam:CreateRole",
                "iam:DeleteRolePolicy",
                "iam:PassRole",
                "iam:PutRolePolicy",
                "iam:DeleteRole",
                "iam:AttachRolePolicy",
                "iam:DetachRolePolicy"
            ],
            "Resource": "*"
        }
    ]
}
```
