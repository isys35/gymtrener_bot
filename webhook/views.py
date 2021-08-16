from rest_framework import status
from rest_framework.response import Response


async def webhook(request):
    if request.method == 'POST':
        return Response("Hello, async Django!")
    else:
        return Response({'code': 405}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
