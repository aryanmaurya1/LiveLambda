domain_name = ""
domain_prefix = ""

dummy_event_template = {
    "version": "2.0",
    "routeKey": "GET /user/48578547",
    "rawPath": "/testing/user/2",
    "rawQueryString": "",
    "headers": {
      "accept": "*/*",
      "content-length": "31",
      "content-type": "application/json",
      "host": "api.writups.tech",
      "user-agent": "Dummy Event",
      "x-amzn-trace-id": "Root=1-60a4c716-1c1a3cf77daa2a9473d2fdd8",
      "x-forwarded-for": "1.23.143.231",
      "x-forwarded-port": "443",
      "x-forwarded-proto": "https"
    },
    "requestContext": {
      "accountId": "734310663973",
      "apiId": "wldde2k9s8",
      "domainName": "api.writups.tech",
      "domainPrefix": "api",
      "http": {
        "method": "GET",
        "path": "/testing/user/2",
        "protocol": "HTTP/1.1",
        "sourceIp": "1.23.143.231",
        "userAgent": "insomnia/2021.1.0"
      },
      "requestId": "fkQLeiZ1BcwEJ4Q=",
      "routeKey": "GET /user/{id}",
      "stage": "testing",
      "time": "19/May/2021:08:06:46 +0000",
      "timeEpoch": 1621411606142
    },
    "pathParameters": {
      "id": "2"
    },
    "body": "{\"name\":\"John\",\"surname\":\"Doe\"}",
    "isBase64Encoded": False,
}

class Test():
  def __init__(self):
    self.path = ""
    self.method = "GET"
    self.pathParameters = None
    self.queryStringParameters = None

class DummyEvent():
  def __init__(self, app):
    self.version = "2.0"
    self.stage = "default"
    self.base = ""
    self.tests = []

  def generate_test_request(test):
    pass