#!/bin/bash
cd notificationenv/lib/python3.7/site-packages
zip -r9 ${OLDPWD}/function.zip .
cd $OLDPWD
zip -g function.zip whatsapp_messaging.py
aws lambda update-function-code --function-name whatsapp-awsnews --zip-file fileb://function.zip