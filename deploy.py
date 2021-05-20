from logging import Handler
import boto3
import base64
from app import app

#### Constants ###

file_path = "./liveLambda.zip"
lambda_role_arn = 'arn:aws:iam::734310663973:role/lambda_role'
function_name = "made_in_India_v2"
handler_function = 'app.lambda_handler'

#### Constants End Here ###


#### Globals for auto population ###

lambda_function_arn = ""

#### Globals for auto population ###


# AWS Lambda Deployment Part 

lambda_client = boto3.client('lambda')
file = open(file_path, 'rb')
file = file.read()
deployed_function = lambda_client.create_function(FunctionName=function_name, Runtime='python3.8', Role=lambda_role_arn, Handler=handler_function, Code={'ZipFile' : file}, Publish=True, PackageType='Zip')
lambda_function_arn = deployed_function["FunctionArn"]
