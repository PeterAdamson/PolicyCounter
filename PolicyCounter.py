#!/usr/bin/python
# -*- coding: utf-8 -*-
#author Peter Adamson
#This script downloads a json file containing user policies from an s3 bucket,
#then counts the number of policies containing the termn "FullAccess",
#and then uploads that count in another json file to the same s3 bucket

import boto3
import botocore
import json

seen = []

BUCKET_NAME = 'user.policies'
KEY = 'user_policies.json'

s3 = boto3.resource('s3')
count = 0

try:
	s3.Bucket(BUCKET_NAME).download_file(KEY, 'user_policies.json')
except botocore.exceptions.ClientError as e:
	if e.response['Error']['Code'] == '404':
		print('The object does not exist.')
	else:
		raise Exception('An error occurred.')

with open('user_policies.json') as json_data:
	jdata = json.load(json_data)
	for data in jdata['data']['users']['items']:
		for further in data['policies']['items']:
			if 'FullAccess' in list(further.values())[0] and list(further.values())[0] not in seen:
				count += 1
				seen.append(list(further.values())[0])

store = {'count': count}

try:
	with open('count.json', 'w') as outfile:
		json.dump(store, outfile)
except IOError:
	print('Unable to create file')

try:
	with open('count.json', 'rb') as upload:
	s3.Bucket(BUCKET_NAME).put_object(Key='count.json', Body=upload)
except FileNotFoundError:
	print('Wrong file or file path')
