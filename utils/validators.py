from typing import Union
from models import GenericAPIRepsonse


def validate_response(fn):
    def wrapper(*args, **kwargs):
        # assuming we would be getting status_code, message and data
        try:
            result = fn(*args, **kwargs)
            if (
                isinstance(result, Union[dict, GenericAPIRepsonse])
                and result.status_code == 200
            ):
                return result.data
            else:
                print("Unrecognised type found")
                return result.message
        except Exception as e:
            # log the exception
            print(f"Unexpected error in {fn.__name__}: {str(e)}")
            return {}

    return wrapper
