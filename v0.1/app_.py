import json
import liveLambda

app = liveLambda.LiveLambda();


endpoint = "database-lambda.cjqf0qtlraak.ap-south-1.rds.amazonaws.com"
db = {"engine" : "mysql", "username" : "admin", "password" : "stackprolambdadb", "database" : "lambda", "url" : endpoint}

app.set_database_config(db)


def f1(request, response, cursor=None):
  response["body"] = {"function" : "f1", "method" : "GET"}
  return response

def f2(request, response, cursor=None):
  return {"function" : "f2", "method" : "POST"}
  

def f3(request, response, cursor=None):
  return {"function" : "f3", "method" : "PUT"}
  

# app.add_route(action, method, controller, db_required)
app.add_action("/", "GET", f1, db_required=True)
app.add_action("/", "POST", f2, db_required=True)
app.add_action("/", "PUT", f3, db_required=True)

print(app.get_action_dict())


def lambda_handler(event, context):
  return json.dumps(app.run(event, context))