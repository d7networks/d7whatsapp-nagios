#!/usr/bin/env python3
# coding=utf-8

# ** Remember to replace D7_TOKEN

import argparse
import sys
import json
import urllib.request

GW_URL = "https://api.d7networks.com/whatsapp/v2/send"

# Can be generated from https://app.d7networks.com/developer/applications'
D7TOKEN = "D7_TOKEN"

parser = argparse.ArgumentParser()
parser.add_argument('--source_address', help='Sender ID (Source Mobile Number) registered with Meta')
parser.add_argument('--to', help='SMS receiver mobile number, eg: 9715090xx')
parser.add_argument('--template_id', help='template_id of meta approved template', required=True)
parser.add_argument('--type', help='Notification Type', required=True)
parser.add_argument('--host',  help='Host Name', required=True)
parser.add_argument('--address', help='Host address', required=True)
parser.add_argument('--state',  help='Host state', required=True)
parser.add_argument('--date',  help='Date & time',required=True)
parser.add_argument('--info',  help='Additional info', required=True)

if __name__ == '__main__':
    args = parser.parse_args()
    
    if not (args.to and args.source_address and args.template_id and args.type and args.host and args.address and args.state and args.date and args.info ):
        print("All the arguments are required to send WhatsApp messages")
        sys.exit(1)
    
    to = args.to.strip('\'').replace(' ', '')
    # .split(',')
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + D7TOKEN
    }

    messages = [
        {
            "originator": args.source_address,
            "content": {
                "message_type": "TEMPLATE",
                "template": {
                    "template_id": args.template_id,
                    "language": "en_GB",
                    "body_parameter_values": {
                        "1": args.type,
                        "2": args.host,
                        "3": args.address,
                        "4": args.state,
                        "5": args.date,
                        "6": args.info
                    }
                }
            },
            "recipients": [{"recipient": to, "recipient_type": "individual"}]
        }
    ]

    json_data = json.dumps({
        "messages": messages
    })
    
    req = urllib.request.Request(GW_URL, data=json_data.encode('utf-8'), headers=headers)
    try:
        response = urllib.request.urlopen(req, timeout=10)
    except urllib.error.HTTPError as e:
        print(f"Failed to WhatsApp message, reason: {e.reason}, code: {e.code}")
        response_data = e.read().decode('utf-8')
        print("Error details:", response_data)
    else:
        response_data = response.read().decode('utf-8')
        print(response_data)

