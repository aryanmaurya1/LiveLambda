from liveLambda_v2 import LiveLambdaV2

app = LiveLambdaV2()

localTesting = True
lambdaTesting = False

@app.route("/", "GET")
def f1():
  return {"key" : str(app.request), "route" : "GET /"}

@app.route("/", "POST")
def f2():
  return {"key" : str(app.request), "route" : "POST /"}

@app.route("/user", "POST")
def f3():
  return {"key" : str(app.request), "route" : "POST /user"}

@app.route("/user", "GET")
def f4():
  return {"key" : str(app.request), "route" : "GET /user"}

@app.route("/user/{id}", "POST")
def f4(id):
  return {"key" : str(app.request), "route" : "POST /user/" + str(id)}

@app.route("/user/{id}", "GET")
def f5(id):
  return {"key" : str(app.request), "route" : "GET /user/" + str(id)}

from dummy_event import Dummy_event, dummy_event_template

def lambda_handler(event, context):
  response = app.run(event, context)
  print(response)
  return response

if localTesting:
  lambda_handler(dummy_event_template, {})