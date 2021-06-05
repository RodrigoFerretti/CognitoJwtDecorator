import json
from flask import Response


def build_flask_response(status_code, body):
    return Response(response=json.dumps(body, sort_keys=True, default=str),
                    status=status_code, content_type='application/json')
