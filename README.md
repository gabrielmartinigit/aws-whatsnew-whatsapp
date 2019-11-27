# AWS Whats New WhatsApp notifications
Are you tired to try to be updated about AWS? Would you like to be notified every time AWS launches a new feature or service? This simple app reads the AWS Whats New RSS and send you a notification via WhatsApp about the latest entry.

_pre requisites:_
* Twilio account
* AWS CLI
* AWS account with the following access:
    * AWS CloudFormation
    * Amazon Lambda
    * Amazon CloudWatch
    * Amazon DynamoDB

## Testing local
Run the following commands:
```
    virtualenv notificationsenv
    source notificationsenv/bin/activate
    pip install -r requirements.txt
    python whatsapp_messaging.py
```

## Deploying to AWS

## License summary
This sample code is made available under the MIT-0 license. See the LICENSE file.
