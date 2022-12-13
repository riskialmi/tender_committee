from fastapi.responses import JSONResponse

def exception_handler_negative_case(status_code, msg, data):
    return JSONResponse(
        status_code=status_code,
        content={'is_success': False,
                 'data': data,
                 "message": msg},
    )

def response_success(data, msg=None):
    return {'is_success': True,
            'data': data,
            "message": msg
            }