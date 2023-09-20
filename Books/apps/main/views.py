from rest_framework.response import Response
from rest_framework.views import APIView


class HomePage(APIView):
    def get(self, request):
        if not request.user.is_anonymous:
            content = {'message': f'Hello, {request.user.email}!'}
        else:
            content = {'message': 'Welcome!'}
        return Response(content)
