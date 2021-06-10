from LiveLambda import LiveLambda
app = LiveLambda()

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


def lambda_handler(event, context):
  response = app.run(event, context)
  return response
