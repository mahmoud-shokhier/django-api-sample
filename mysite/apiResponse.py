
def prepareResponse(meta=[], data=[], status=True, message='', errors=[]):
    response = {
        'meta' :meta,
        'data': data ,
        'status': status ,
        'message':message ,
        'errors':errors
    }
    return response