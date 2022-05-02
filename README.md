discord-interactions-django
---
A fork of discord-ineractions-python
![PyPI - License](https://img.shields.io/pypi/l/discord-interactions)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/discord-interactions)

Types and helper functions for Discord Interactions webhooks.

# Installation - COMING SOON

Available via [pypi](https://pypi.org/project/discord-interactions/):

```
pip install discord-interactions-django
```

# Usage

Use the `InteractionType` and `InteractionResponseType` enums to process and respond to webhooks.

Use `verify_key` to check a request signature:

```py
if verify_key(request.data, signature, timestamp, 'my_client_public_key'):
    print('Signature is valid')
else:
    print('Signature is invalid')
```

Use `verify_key_decorator` to protect a view function in a Django app:

```py
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from discord_interactions_django import verify_key_decorator, InteractionType, InteractionResponseType

DISCORD_APPLICATION_PUBLIC_KEY = os.getenv('DISCORD_APPLICATION_PUBLIC_KEY')

@csrf_exempt
@require_http_methods(['POST'])
@verify_key_decorator(DISCORD_APPLICATION_PUBLIC_KEY)
def webhook(request):
    if json.loads[request.body]['type'] == InteractionType.APPLICATION_COMMAND:
        return HttpResponse(json.dumps({
            'type': InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
            'data': {
                'content': 'Hello world'
            }
        }))
```

# Exports

This module exports the following:

### InteractionType

An enum of interaction types that can be POSTed to your webhook endpoint.

### InteractionResponseType

An enum of response types you may provide in reply to Discord's webhook.

### InteractionResponseFlags

An enum of flags you can set on your response data.

### verify_key(raw_body: str, signature: str, timestamp: str, client_public_key: str) -> bool:

Verify a signed payload POSTed to your webhook endpoint.

### verify_key_decorator(client_public_key: str)

Django decorator that will verify request signatures and handle PING/PONG requests.
