from logging import Handler
import boto3
import base64
from app import app

#### Constants ###

file_path = "./liveLambda.zip"
lambda_role_arn = 'arn:aws:iam::734310663973:role/lambda_role'
function_name = "writups_central_api_v2"
handler_function = 'app.lambda_handler'
api_name = "final_deployment"



#### Globals for auto population ###

lambda_function_arn = ""
api_id = ""
api_endpoint = ""
integration_ids = []


#### AWS Lambda Deployment Part 

print("Starting Deployment ...")
step = 1
print(f"[{step}] : Creating Lambda")

lambda_client = boto3.client('lambda')
file = open(file_path, 'rb')
file = file.read()
deployed_function = lambda_client.create_function(FunctionName=function_name, Runtime='python3.8', Role=lambda_role_arn, Handler=handler_function, Code={'ZipFile' : file}, Publish=True, PackageType='Zip')
lambda_function_arn = deployed_function["FunctionArn"]

print(f"[{step}] : Lambda Creation Done.")
print(f"Lambda function ARN : {lambda_function_arn}")


#### AWS API Gateway Part
step  = step + 1
print(f"[{step}] : Generating Route Key List")
route_key_list = app.generate_route_keys()
print(f"[{step}] : Generation of Route Key List done.")
print(route_key_list)
step = step + 1

role_arn = "arn:aws:iam::734310663973:role/api_gateway_role"
api_gateway_client = boto3.client('apigatewayv2')

print(f"[{step}] : Creating Base API.")
# Creating base API using first entry in route_list
base_api_response = api_gateway_client.create_api(Name=api_name, ProtocolType="HTTP", Target=lambda_function_arn, RouteKey=route_key_list[0])
api_id = base_api_response["ApiId"]
api_endpoint = base_api_response["ApiEndpoint"]
print(f"[{step}] : Creation of Base API Done.")
print(f"API ID : {api_id}")

step = step + 1

route_key_list = route_key_list[1:]

for route_key in route_key_list:
  print(f"[{step}] : Making Integration for [ {route_key} ]")
  method, path = route_key.split()
  integration_response =  api_gateway_client.create_integration(ApiId=api_id, IntegrationMethod=method, IntegrationType="AWS_PROXY", IntegrationUri=lambda_function_arn, PayloadFormatVersion="2.0")
  integration_id = integration_response["IntegrationId"]
  target = "integrations/" + str(integration_id)
  integration_ids.append(integration_id)
  api_gateway_client.create_route(ApiId=api_id, RouteKey=route_key, Target=target)
  print(f"[{step}] : Making Integration for [ {route_key} ] done.")
  print(f"[{step}] : Integration Id for [ {route_key} ] -> {integration_id}")
  step = step + 1

print("Deployment Done Successfully.")
print(f"\n\nAPI ENDPOINT : {api_endpoint}")