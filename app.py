from liveLambda_v2 import LiveLambdaV2

app = LiveLambdaV2()

@app.route("/", "GET")
def f1():
  pass

@app.route("/", "POST")
def f2():
  pass

@app.route("/user", "POST")
def f3():
  pass

@app.route("/user", "GET")
def f4():
  pass


@app.route("/user/{id}", "POST")
def f4():
  pass

@app.route("/user/{id}", "GET")
def f5():
  pass

from dummy_event import dummy_event

def lambda_handler(event, context):
  testing = False
  if testing:
    event = dummy_event
  app.run(event, context)