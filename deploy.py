import boto3
import json
from datetime import datetime
from app import app

#### Reading Config file

config_file = open("./config.json", 'r')
config_data = config_file.read()
config_data = json.loads(config_data)
config_file.close()

#### Global Configuration ###

file_path = config_data["file_path"]
lambda_role_arn = config_data["lambda_role_arn"]
function_name = config_data["function_name"]
handler_function = config_data["handler_function"]
api_name = config_data["api_name"]



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
binary_data = file.read()
file.close()

deployed_function = lambda_client.create_function(FunctionName=function_name, Runtime='python3.8', Role=lambda_role_arn, Handler=handler_function, Code={'ZipFile' : binary_data}, Publish=True, PackageType='Zip')
lambda_function_arn = deployed_function["FunctionArn"]

print(f"[{step}] : Lambda Creation Done.")
print(f"Lambda function ARN : {lambda_function_arn}")

#### Ataching Resource Based Permissions to lambda
step = step + 1
print(f"[{step}] : Attaching Resource Based Permission.")
statement_id = str(datetime.now().timestamp())
statement_id = statement_id.replace(".", "-")
lambda_client.add_permission(FunctionName=function_name, Principal="apigateway.amazonaws.com", Action="lambda:InvokeFunction",StatementId=statement_id)
print(f"[{step}] : Attached Resource Based Permission.")
print(f"Statement Id : {statement_id}")


#### AWS API Gateway Part
step  = step + 1
print(f"[{step}] : Generating Route Key List")
route_key_list = app.generate_route_keys()
print(f"[{step}] : Generation of Route Key List done.")
print(route_key_list)
step = step + 1

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
