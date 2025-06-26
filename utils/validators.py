from typing import Union
from models import GenericAPIRepsonse


def validate_response(fn):
    def wrapper(*args, **kwargs):
        # assuming we would be getting status_code, message and data
        expected_types = Union[dict, GenericAPIRepsonse, str]
        try:
            result = fn(*args, **kwargs)
            if not isinstance(result, Union[dict, GenericAPIRepsonse, str]):
                return {
                    "Error": f"Unrecognised type found in {result}, expected: {expected_types}, found: {type(result)}"
                }
            if result.status_code == 200:
                return result.data
            else:
                err = f"{result.message if result.message else result}"
                print(err)
                return err
        except Exception as e:
            # log the exception
            print(f"Unexpected error in {fn.__name__}: {str(e)}")
            return {}

    return wrapper
