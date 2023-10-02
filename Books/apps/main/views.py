from django.utils.translation import gettext
from rest_framework.response import Response
from rest_framework.views import APIView


class HomePage(APIView):
    def get(self, request):
        if not request.user.is_anonymous:
            content = {'message': f'Hello, {request.user.email}!'}
        else:
            content = {'message': 'Welcome!'}
        return Response(content)


class OurShops(APIView):

    def get(self):
        return Response(data={'title': gettext('Наши магазины')})


class ContactSupportView(APIView):

    def get(self):
        return Response(data={'title': 'Контакты и поддержка'})
