__version__ = '0.3.0'

from functools import wraps
from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey

class InteractionType:
    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3
    APPLICATION_COMMAND_AUTOCOMPLETE = 4

class InteractionResponseType:
    PONG = 1
    CHANNEL_MESSAGE_WITH_SOURCE = 4
    DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE = 5
    DEFERRED_UPDATE_MESSAGE = 6
    UPDATE_MESSAGE =  7  
    APPLICATION_COMMAND_AUTOCOMPLETE_RESULT = 8 

class InteractionResponseFlags:
    EPHEMERAL = 1 << 6

def verify_key(raw_body: bytes, signature: str, timestamp: str, client_public_key: str) -> bool:
    message = timestamp.encode() + raw_body
    try:
        vk = VerifyKey(bytes.fromhex(client_public_key))
        vk.verify(message, bytes.fromhex(signature))
        return True
    except Exception as ex:
        print(ex)
    return False

def verify_key_decorator(client_public_key):
    import json
    from django.http import HttpResponse
    
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            signature = request.headers['X-Signature-Ed25519']
            timestamp = request.headers['X-Signature-Timestamp']
            jsonpayload = json.loads(request.body)
            if signature is None or timestamp is None or not verify_key(request.body, signature, timestamp, client_public_key):
                return 'Bad request signature', 401
            if jsonpayload and jsonpayload['type'] == InteractionType.PING:
                return HttpResponse(json.dumps({
                    'type': InteractionResponseType.PONG
                }))
            return func(request, *args, **kwargs)
        return wrapper
    return decorator
