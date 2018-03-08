#!/usr/bin/python
# -*- coding: utf-8 -*-

import boto3
import botocore
import json

BUCKET_NAME = 'user.policies'
KEY = 'user_policies.json'

s3 = boto3.resource('s3')
count = 0

try:
    s3.Bucket(BUCKET_NAME).download_file(KEY, 'user_policies.json')
except botocore.exceptions.ClientError, e:
    if e.response['Error']['Code'] == '404':
        print 'The object does not exist.'
    else:
        raise Exception('An error occurred.')

with open('user_policies.json') as json_data:
    jdata = json.load(json_data)
    for data in jdata['data']['users']['items']:
        for further in data['policies']['items']:
            if 'FullAccess' in further.values()[0]:
                count += 1

store = {'count': count}

try:
    with open('count.json', 'w') as outfile:
        json.dump(store, outfile)
except IOError:
    print 'Unable to create file'

try:
    with open('count.json', 'rb') as upload:
        s3.Bucket(BUCKET_NAME).put_object(Key='count.json', Body=upload)
except FileNotFoundError:
    print 'Wrong file or file path'

			
