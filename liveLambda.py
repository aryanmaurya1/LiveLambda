class LiveLambda:
  def __init__(self):
    self.__action_dict = dict({ "POST" : {}, "GET" : {}, "PUT" : {},"DELETE" : {} ,"ANY" : {}, "PATCH" : {} })
    self.__database_config = {}
    self.__app_config = {}
    self.__connection = None
    self.__cursor = None
    self.__event = None

  def get_action_dict(self):
    return self.__action_dict
  
  def get_database_config(self):
    return self.__database_config

  def get_app_config(self):
    return self.__app_config
  
  def set_database_config(self, config):
    self.__database_config = config

  def get_cursor(self):
    if self.__database_config["engine"] == "mysql":
      import pymysql
      db_url = self.__database_config["url"]
      username = self.__database_config["username"]
      password = self.__database_config["password"]
      db_name = self.__database_config["database"]
      self.__connection = pymysql.connect(host=db_url, user=username, password=password, database=db_name)
      self.__cursor = self.__connection.cursor()
      return self.__cursor

  def commit_close_connection(self):
    self.__cursor.close()
    self.__connection.commit()

  def get_method(self):
    return self.__event["requestContext"]["http"]["method"]
  
  def get_action(self):
    return self.__event["body"]["action"]

  def get_handler_dict(self, method, action):
    return self.__action_dict[method][action]

  def add_action(self, action, method , controller, db_required = False):
    try:
      check = self.__action_dict[method][action]
      if check:
        msg = f"Route : {action}, Method: {method} is already registered."
        raise Exception(msg)
    except KeyError:
      self.__action_dict[method][action] = dict({"controller" : controller, "db_required" : db_required})


  def run(self, event, context):
    self.__event = event
    body = {}
    if "data" in event["body"].keys():
      body =  event["body"]["data"]
    request = {"headers" : event["headers"],"requestContext" : event["requestContext"], "body" : body}
    try:
      request["queryStringParameters"] = event["queryStringParameters"]
    except KeyError:
      pass
    response = {}
    method = self.get_method()
    action = self.get_action()
    handler_dict = self.get_handler_dict(method, action)
    if handler_dict["db_required"]:
      response = handler_dict["controller"](request, response, self.get_cursor())
    else:
      response = handler_dict["controller"](request, response)
    self.commit_close_connection()
    return response