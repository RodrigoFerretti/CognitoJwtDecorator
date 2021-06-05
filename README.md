# CognitoJwtDecorator

This code is intended to be used as a decorator for a flask route to authenticate itself before executing the rest of the method. 

It takes 2 arguments, one is a string containing cognito groups separated by commas or spaces(optional), for example: "admin, read, write", and the other is the cognito pool id that generated the access key token to be validated. 

Example:

```python
# save this as app.py
from flask import Flask

from CognitoJwtDecorator.CognitoDecorator import token_required

app = Flask(__name__)

@token_required('admin', 'cognito_pool_id_example')
@app.route("/")
def hello():
    return "Hello, World!"
```
