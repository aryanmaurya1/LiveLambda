import json

class Request:
  # Base class for a request object. Every request object comming from API gateway is transformed internally into 
  # LiveLambdaV2's internal request object. 
  # REQUEST (API GATEWAY) --> REQUEST (LiveLambda)
  
  def __init__(self):
      self.request_context = {}
      self.headers = {}
      self.body = {}
      self.pathParameters = None
      self.queryStringParameters = None
      self.mics = {}

  def __repr__(self):
      line = "Request Context: "+ str(self.request_context) + "\n" + "Request Headers: " + str(self.headers) + "\n"
      line = line + "Body: " + str(self.body) + "\n" + "Path Parameters: " + str(self.pathParameters) + "\n"
      line = line + "Query Params: " + str(self.queryStringParameters) + "\n" + "Mics: " + str(self.mics) + "\n"
      return line

class Response:
  def __init__(self):
      self.body = {}
      self.headers = {}
  def get_dict(self):
    return {"body" : self.body, "header": self.headers}

class LiveLambdaV2:
  # Main class which handles the flow from registering handler functions to calling them on correct routes.
  # Evey LiveLambdaV2 webapp must contain atleast one object of this class.

  def __init__(self):
    self.__route_dict = { "POST" : {}, "GET" : {}, "PUT" : {},"DELETE" : {} ,"ANY" : {}, "PATCH" : {} }
    self.__app_config = {}
    self.__event = None
    self.request = {}
    self.response = {}
  
  def register_route(self, route, methods, handler):
    # Internal method, should not be used directly. Instead use @app.route() decorator to register handler functions.
    # Here 'app' refers to a LiveLambdaV2 Object.
    # @route:string -> Endpoint  for which to register handler. 
    # @methods:list -> List of methods for which hanlder should be registered to a given route.
    # @handler:function -> Handler function to register.
    
    for method in methods:
      self.__route_dict[method][route] = handler


  def route(self, route, method):
    # This is a decorator, usage is similar like route decorator in flask.
    # usage : @app.route(route='/{id}', method=['GET'])
    #         def home(id):
    #           pass
    # Here 'app' is a LiveLambda object.
    # @route:string -> Endpoint  for which to register handler. 
    # @method:list/string ->  List of methods for which hanlder should be registered to a given route.

    isMethodList = type(method) == type([])
    if not isMethodList:
      # If there is a single method, then converting it into list of method.
      method = [method]

    def wrapper(handler):
      self.register_route(route=route, methods=method, handler=handler)
      return handler
    return wrapper

  def generate_route_keys(self):
    # Returns a list of all routes registered with an particular LiveLambdaV2 object.

    full_paths = []
    for method in self.__route_dict.keys():
      for route in self.__route_dict[method]:
        p = method + " " + route
        full_paths.append(p)
    return full_paths


  def get_param_name(self, route):
    # Internal method, should not be used directly.
    # run method internally uses it to find out the name of url parameter in a registered route.

    start = None
    end = None
    for i in range(len(route)):
      if route[i] == "{":
        start = i
      if route[i] == "}":
        end = i
        break
    return route[start+1 : end]

  def run(self, event, context):
    # This method takes an event and context object provided by the AWS Lambda handler function and calls 
    # appropriate handler internally and returns the proper response.
    # event:dict -> Event dictionary which lambda_handler function (first function which AWS Lambda runtime calls) 
    #     received as an argument.
    # context:object -> Context Object which lambda_handler function (first function which AWS Lambda runtime calls) 
    #     received as an argument.

    self.request = Request()
    self.response = Response()

    # Setup request object 
    self.request.request_context = event["requestContext"]
    self.request.headers = event["headers"]

    if "body" in event.keys():
      self.request.body = json.loads(event["body"])
    else:
      self.request.body =  {}

    if "pathParameters" in event.keys():
      self.request.pathParameters = event["pathParameters"]
    else:
      self.request.pathParameters = {}

    if "queryStringParameters" in event.keys():
      self.request.queryStringParameters = event["queryStringParameters"]
    else:
      self.request.queryStringParameters = {}

    self.request.mics = {"version" : event["version"], "routeKey" : event["routeKey"], "rawPath" : event["rawPath"], "rawQueryString" : event["rawQueryString"], "isBase64Encoded" : event["isBase64Encoded"]} 

    # Call appropriate handler
    method, route = event["routeKey"].split()
    handler = self.__route_dict[method][route]
    if "pathParameters" in event.keys():
      param_name = self.get_param_name(route)
      response = handler(event["pathParameters"][param_name])
    else:
      response = handler()

    return response