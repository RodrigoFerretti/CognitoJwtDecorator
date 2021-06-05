from functools import wraps

from src.Validators import *


# Decorator for Cognito token authentication #
def token_required(groups_string, user_pool_id):
    def token_validator(f):
        @wraps(f)
        def token_requirement(*args, **kwargs):
            token_data = dict()

            token_error = validate_token(token_data, user_pool_id)
            if token_error is not None:
                return token_error

            token_error = validate_token_groups(token_data, groups_string)
            if token_error is not None:
                return token_error

            token_error = validate_token_expiration(token_data, user_pool_id)
            if token_error is not None:
                return token_error

            return f(*args, **kwargs)

        # Returning decorator method #
        return token_requirement

    # Returning decorator #
    return token_validator
