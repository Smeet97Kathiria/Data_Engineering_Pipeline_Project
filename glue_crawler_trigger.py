import json
import sys 

import boto3 

client = boto3.client('glue')



def lambda_handler(event, context):
	print(event)
	
	file_name = event['Records'][0]['s3']['object']['key'].split("/")[1]
	
	if file_name == "csv":
		client.start_crawler( Name='csv_crawler' )
	else:
		client.start_crawler( Name='json_crawler' )
		
		
		

		
		