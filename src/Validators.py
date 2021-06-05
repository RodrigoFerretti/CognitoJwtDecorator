import os
import jwt
from flask import request

from src.Adapters import *
from src.Services import *
from src.FlaskResponseBuilder import *


def validate_token(token_data, user_pool_id):
    try:
        # JWT decoding #
        token = request.environ['HTTP_AUTHORIZATION'].replace("Bearer ", "")
        token_header_b64 = token.split('.')[0]
        token_header_b64 += "=" * ((4 - len(token_header_b64) % 4) % 4)
        token_header = json.loads(base64.b64decode(token_header_b64).decode("utf-8"))
        token_payload = jwt.decode(token, verify=False)

        # Assembling static pool iss URL for token validation #
        url_cognito_pool = get_url_cognito_pool(user_pool_id)

        # Retrieving JWT iss URL for comparison #
        url_jwt_payload = token_payload['iss'] + '/.well-known/jwks.json'

        # Asserting token URL comparison for security reasons #
        assert url_cognito_pool == url_jwt_payload

        token_data['token'] = token
        token_data['token_header'] = token_header
        token_data['token_payload'] = token_payload

    except Exception as e:
        del e
        return build_flask_response(403, {"ErrorMessage": "Invalid Access Token"})


def validate_token_groups(token_data, groups_string):
    # Validating if user belongs to a Cognito group #
    groups = groups_string.strip(',').replace(' ', '')
    token_validated = validate_user_in_groups(token_data['token_payload'].get('cognito:groups'), groups)

    # Returning 403 for not-authorized #
    if not token_validated:
        return build_flask_response(403, {"ErrorMessage": "The groups you belong to are not allowed on this route"})


def validate_token_expiration(token_data, user_pool_id):
    try:
        # Retrieving Cognito pool keys #
        keys_list = get_cognito_pool_public_keys(get_url_cognito_pool(user_pool_id))

        # Retrieving correct key #
        right_key = next(key for key in keys_list if key['kid'] == token_data['token_header']['kid'])

        # Converting JWK to PEM #
        pem_key = jwk_to_pem(right_key)

        # Retrieving JWT decoding algorithm #
        alg = right_key['alg']

        # Decoding JWT #
        jwt.decode(jwt=token_data['token'], key=pem_key, algorithms=alg)
    except Exception as e:
        del e
        return build_flask_response(403, {"ErrorMessage": "Access Token has expired"})


# Method validates if user associated groups is authorized on a specific route #
def validate_user_in_groups(user_groups, decorator_groups):
    if user_groups is None:
        return True if decorator_groups == '' else False
    return next((True for group in user_groups if group in decorator_groups), False)
