from liveLambda_v2 import LiveLambdaV2

app = LiveLambdaV2()

localTesting = False
lambdaTesting = False

@app.route("/", "GET")
def f1():
  return {"key" : str(app.request)}

@app.route("/", "POST")
def f2():
  return {"key" : str(app.request)}

@app.route("/user", "POST")
def f3():
  return {"key" : str(app.request)}

@app.route("/user", "GET")
def f4():
  return {"key" : str(app.request)}

@app.route("/user/{id}", "POST")
def f4(id):
  return {"key" : str(app.request)}

@app.route("/user/{id}", "GET")
def f5(id):
  return {"key" : str(app.request)}

from dummy_event import dummy_event

def lambda_handler(event, context):
  use_dummy_event = True
  if lambdaTesting:
    event = dummy_event
  response = app.run(event, context)
  return response

if localTesting:
  lambda_handler(dummy_event, {})