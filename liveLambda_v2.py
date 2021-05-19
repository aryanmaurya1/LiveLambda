import json

class Request:
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
  def __init__(self):
    self.__route_dict = { "POST" : {}, "GET" : {}, "PUT" : {},"DELETE" : {} ,"ANY" : {}, "PATCH" : {} }
    self.__app_config = {}
    self.__event = None
    self.request = {}
    self.response = {}
  
  def register_route(self, route, methods, handler):
    # print(route," " * (50 - len(str(route))), methods, " " * (40 - len(str(methods))) ,handler)
    for method in methods:
      self.__route_dict[method][route] = handler


  def route(self, route, method):
    isMethodList = type(method) == type([])
    if not isMethodList:
      # If there is a single method, then converting it into list of method.
      method = [method]

    def wrapper(handler):
      self.register_route(route=route, methods=method, handler=handler)
    return wrapper

  def run(self, event, context):

    self.request = Request()
    self.response = Response()

    # Setup request object 
    self.request.request_context = event["requestContext"]
    self.request.headers = event["headers"]
    self.request.body = json.loads(event["body"]) if "body" in event.keys() else {}
    self.request.pathParameters = event["pathParameters"] if "pathParameters" in event.keys() else None
    self.request.queryStringParameters = event["queryStringParameters"] if "queryStringParameters" in event.keys() else None
    self.request.mics = {"version" : event["version"], "routeKey" : event["routeKey"], "rawPath" : event["rawPath"], "rawQueryString" : event["rawQueryString"], "isBase64Encoded" : event["isBase64Encoded"]} 

    # Call appropriate handler
    method, route = event["routeKey"].split()
