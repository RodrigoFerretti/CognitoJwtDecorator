# CognitoJwtDecorator

This code is intended to be used as a decorator for a flask route to authenticate itself before executing the rest of the method. It blocks the execution of the route method in case you dont provide a valid access token in request header with some custom responses.

To authenticate, you need to pass in the access token generated from AWS cognito pool in the 'Authorization' header.

The decorator takes 2 arguments, one is a string containing cognito groups separated by commas or spaces(spaces optional, example: "admin, read, write"), and the other is the Cognito pool Id that generated the access key token to be validated. 

Example:

```python
# save this as app.py
from flask import Flask

from CognitoJwtDecorator.CognitoDecorator import token_required

app = Flask(__name__)

@token_required('admin, read', 'cognito_pool_id_example')
@app.route("/")
def hello():
    return "Hello, World!"
```

The 4 possible responses for this example would be:

```json
{
    "statusCode": 403,
    "body": {
        "ErrorMessage": "Invalid Access Token"
    }
}





{
    "statusCode": 403,
    "body": {
        "ErrorMessage": "The groups you belong to are not allowed on this route"
    }
}



{
    "statusCode": 403,
    "body": {
        "ErrorMessage": "Access Token has expired"
    }
}




{
    "statusCode": 200,
    "body": "Hello, World!"
}
```

