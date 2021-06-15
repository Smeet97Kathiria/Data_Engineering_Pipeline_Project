from __future__ import print_function

import json
import sys
from os import path
import subprocess
from pprint import pprint
import urllib3

def hello(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

def s3_trigger_pipeline(event, context):
       
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    
    records_s3 = event['Records'][0]['s3']
    bucket_name = records_s3['bucket']['name']
    filename = records_s3['object']['key']

    data_path = 's3://' + path.join(bucket_name, filename)
    
    endpoint = 'http://a2544b01175fd4db887a223c628ff400-744194304.us-west-2.elb.amazonaws.com:8080/api/experimental/dags/data_pipeline_emr/dag_runs'
    
    data = json.dumps({'conf': {'s3_location': data_path }})



    print(f"\n\nPython version: {sys.version}\n\n")
    
    print("Sending http POST request...")

    
    subprocess.run(['curl', '-X', 'POST', endpoint, '-H', "Authorization: 'token dGVzdF91c2VyOnRIMXNJc0FQQHNzdzByZA=='", '--insecure', '-d', data])
    


    return response
    