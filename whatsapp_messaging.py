import boto3
import datetime
import time
import feedparser
from twilio.rest import Client

# ddb client
ddb = boto3.client("dynamodb")
table = 'aws-whatsnew-table'
key = 'whatsnew'
attribute = 'timest'
# news url
aws_whats_new_url = 'https://aws.amazon.com/new/feed/'
# sid and auth token from twilio
twilio_sid = '<YOUR TWILIO SID>'
auth_token = '<YOUR AUTH TOKEN>'
twilio_number = '<YOUR TWILIO NUMBER>'
contact_directory = {'<CONTACT NAME>': '<CONTACT NUMBER>'}


# get the RSS feed through feedparser
def get_rss(url):
    return feedparser.parse(url)


# get the latest notification
def get_latest():
    last_timest = ddb.scan(TableName=table)
    last_timest = last_timest['Items'][0]['timest']['S']
    print('Latest ddb timest: {}'.format(last_timest))
    return last_timest


# update the latest notification
def update_latest(timest):
    ddb.update_item(
        TableName=table,
        Key={
            "rss": {"S": key}
        },
        UpdateExpression="SET #9feb0 = :9feb0",
        ExpressionAttributeNames={"#9feb0": attribute},
        ExpressionAttributeValues={":9feb0": {"S": timest}}
    )
    print('Updated ddb {}: {}'.format(attribute, timest))
    return


# twilio client send whatsapp notification
def send_message(title, link):
    # numbers and messages
    whatsapp_client = Client(twilio_sid, auth_token)
    now = datetime.datetime.now()
    message = 'AWS News {}: {} ({})'.format(now.year, title, link)

    for key, value in contact_directory.items():
        msg_subscribers = whatsapp_client.messages.create(
            body=message,
            from_='whatsapp:{}'.format(twilio_number),
            to='whatsapp:{}'.format(value),
        )
        print('Sent to: {} (id: {})'.format(value, msg_subscribers.sid))
    return


def aws_news(event=None, context=None):
    news = get_rss(aws_whats_new_url)
    print('Feed: {}'.format(aws_whats_new_url))

    # verify last new and actual
    now_timest = str(int(time.mktime(news['entries'][0]['published_parsed'])))
    last_timest = get_latest()
    print('Now ddb timest: {}'.format(now_timest))
    if now_timest == last_timest:
        print("No news")
        return
    else:
        # get the article meta data and send notification
        title = str(news['entries'][0]['title'])
        link = str(news['entries'][0]['link'])
        print(title)
        send_message(title, link)
        update_latest(now_timest)


if __name__ == "__main__":
    aws_news()
