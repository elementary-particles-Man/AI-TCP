import json
from urllib import request


class Response:
    def __init__(self, resp):
        self._resp = resp

    def json(self):
        return json.loads(self._resp.read().decode())

    @property
    def status_code(self):
        return self._resp.getcode()

def post(url, data=None, headers=None):
    if isinstance(data, str):
        data = data.encode()
    req = request.Request(url, data=data, headers=headers or {}, method="POST")
    resp = request.urlopen(req)
    return Response(resp)
