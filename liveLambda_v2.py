import json

request = {}
response = {}

class Route_level:
  def __init__(self):
    self.type = None
    self.handler_dict = { "POST" : {}, "GET" : {}, "PUT" : {},"DELETE" : {} ,"ANY" : {}, "PATCH" : {} }
    self.current_level_str_value = None
    self.sub_route_level = None

  def __repr__(self):
    return "{ TYPE: " + str(self.type) + " " + str(self.handler_dict) + " " + self.current_level_str_value + " SUB_LEVEL: "+ str(self.sub_route_level) + " }"


class Request:
  def __init__(self):
      self.request_context = {}
      self.headers = {}
      self.body = {}

class LiveLambdaV2:
  def __init__(self):
    """
      __route_dict = { method: {node}} 
    """
    # Redesign route dict starting from the base path 
    self.__route_dict = dict({})
    self.__app_config = {}
    self.__event = None
  
  def register_route(self, route_list, methods, handler):
    print(route_list," " * (50 - len(str(route_list))), methods, " " * (40 - len(str(methods))) ,handler)
    # This method registers a route in __route_dict
    # if len(route_list) == 1:
    #   route_level = Route_level()
    #   route_level.type = "path" 
    #   for method in methods:
    #     route_level.handler_dict[method] = handler
    #   route_level.current_level_str_value = "/"

    #   self.__route_dict[route_list[0]] = route_level
  
    # print("Route Dict", self.__route_dict)

  def route(self, route, method):
    route_list = []
    if not route == "/":
      # removing trailing "/" if present
      if route[-1] == "/":
        route = route[:-1]

      # removing leading "/" if present
      if route[0] == "/":
        route = route[1:]

      route_list = route.split("/")

      # again adding ["/"] as starting path in route_list
      route_list = ["/"] + route_list
    else:
      # Handling root path separately 
      route_list = ["/"]

    isMethodList = type(method) == type([])
    if not isMethodList:
      # If there is a single method, then converting it into list of method.
      method = [method]

    def wrapper(handler):
      # populate route dict using a recursive function 
      self.register_route(route_list=route_list, methods=method, handler=handler)

    return wrapper

  def run(self):
    for x in self.__route_dict.keys():
      print(x, self.__route_dict[x])
      print("-" * 20)