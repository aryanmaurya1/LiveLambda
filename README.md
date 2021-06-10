# LiveLambda
A libray for building backends using AWS Lambda.

## Make Your Servers Serverless 🤓

### Instructions
* `LiveLambda.py` and you ``<source_file>`` should be in same directory.
* Import ``LiveLambda`` class from ``LiveLambda.py`` file.
### Example

```
from LiveLambda import LiveLambda

app = LiveLambda()

# Route with a single method attached to it.

@app.route("/", "GET")
def getIndex():
  return {"page" : str(app.request), "route" : "GET /"}

@app.route("/", "POST")
def postIndex():
  return {"page" : str(app.request), "route" : "POST /"}

# Route with url parameters.

@app.route("/user/{id}", "POST")
def routeWithParam(id):
  return {"page" : str(app.request), "route" : "POST /user/{id}"}


# Route with multiple methods attached to it.

@app.route("/dynamic", ["GET", "POST", "PUT", "PATCH", "DELETE"])
def routeWithMultipleMethods():
  return {"key" : str(app.request), "route" : "GET /user"}

# Your source file must containe a method which lambda runtime will invoke.
# Name of function must be same in deployment config file.

def lambda_handler(event, context):
  response = app.run(event, context)
  return response

```

## Deployment

### Instructions
* Your source code must contain a ``config.json`` file which will contains deployment configuration and 'arn' of the role used by the AWS lambda to push the logs at AWS cloudwatch.

* Make a single `.zip` file containing` LiveLambda.py`, `<your_source_code>.py`, and `all_libraries_you_use(files and folders)` .
### Sample ``config.json``
```
{
  "file_path": "<path_to_zip_file>",
  "lambda_role_arn": "<arn>",
  "function_name": "<lambda_function_name>",
  "handler_function": "<source_file>.<starting_function_name>",
  "api_name": "<cloudwatch_api_name>"
}
```
* your ``config.json`` and ``deploy.py`` should be in same folder.
* Run ``deploy.py`` file. 

You will see messages on the terminal indicating the status of each stage. If all goes successful API base URL will be printed on terminal after completion of last stage.
