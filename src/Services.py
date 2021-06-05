import json
import requests


# Method retrieve redis cache keys list #
def get_cognito_pool_public_keys(url_cognito_pool):
    response = requests.request('GET', url_cognito_pool, timeout=5)
    keys_list = json.loads(response.text)['keys']
    return keys_list


def get_url_cognito_pool(cognito_pool_id):
    return f'https://cognito-idp.us-east-2.amazonaws.com/{cognito_pool_id}/.well-known/jwks.json'