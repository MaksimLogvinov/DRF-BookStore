from django.utils.translation import gettext
from rest_framework import viewsets
from rest_framework.response import Response

from apps.products.models import Products


class HomePageViewSet(viewsets.ViewSet):
    queryset = Products.objects.all()

    def get(self, request):
        if not request.user.is_anonymous:
            content = {'message': f'Hello, {request.user.email}!'}
        else:
            content = {'message': 'Welcome!'}
        return Response(content)


class OurShopsViewSet(viewsets.ModelViewSet):

    def get(self):
        return Response(data={'title': gettext('Наши магазины')})


class ContactSupportViewSet(viewsets.ModelViewSet):

    def get(self):
        return Response(data={'title': 'Контакты и поддержка'})
