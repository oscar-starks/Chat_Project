from asgiref.sync import sync_to_async

from accounts.socket_auth import decodeJWTForSocket


class TokenAuthMiddleware:
    """
    this middleware populates the scope['user'] with the credentials of the authenticated user
    when the authentication is successful else scop['user'] will be None
    """

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        headers_dict = {key.decode(): value.decode() for key, value in scope["headers"]}

        try:
            if "token" in headers_dict:
                token = headers_dict["token"]
                user = await sync_to_async(decodeJWTForSocket)(token)

                if not user:
                    scope["user"] = None
                else:
                    scope["user"] = user

            else:
                scope["user"] = None

        except:
            scope["user"] = None

        return await self.inner(scope, receive, send)
