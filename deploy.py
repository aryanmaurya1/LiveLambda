import boto3
import base64

# AWS Lambda Deployment Part 

lambda_client = boto3.client('lambda')
file = open('./liveLambda.zip', 'rb')
file = file.read()

lambda_role_arn = 'arn:aws:iam::734310663973:role/lambda_role'
lambdaClient = lambda_client.create_function(FunctionName='made_in_India', Runtime='python3.8', Role=lambda_role_arn, Handler='app.lambda_handler', Code={'ZipFile' : file}, Publish=True, PackageType='Zip')

