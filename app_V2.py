from liveLambda_v2 import LiveLambdaV2

app = LiveLambdaV2()

@app.route("/user/name/is/rynm", "GET")
def getUsers():
  pass

@app.route("/user/name/is/rynm/<id>", "GET")
def getUserById():
  pass

@app.route("/", "GET")
def getUserById():
  pass

@app.route("/<a>", ["GET", "POST", "PUT"])
def f():
  pass

@app.route("user", "PUT")
def f2():
  pass


from dummy_event import dummy_event
app.run(dummy_event, {})
