import boto3


def send_sms_to_sns_topic(message):
    sns_client = boto3.client("sns", region_name='us-east-1')

    response = sns_client.publish(
        PhoneNumber='+905333053492',
        Message=message
    )
    print(response)
