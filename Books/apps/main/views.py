from django.utils.translation import gettext
from rest_framework import viewsets
from rest_framework.response import Response

from apps.products.models import Products


class HomePageViewSet(viewsets.ViewSet):
    queryset = Products.objects.all()

    def list(self, request, *args, **kwargs):
        if not request.user.is_anonymous:
            content = {'message': f'Hello, {request.user.email}!'}
        else:
            content = {'message': 'Welcome!'}
        return Response(data=content)


class OurShopsViewSet(viewsets.ModelViewSet):

    def list(self, request, *args, **kwargs):
        return Response(data={'title': gettext('Наши магазины')})


class ContactSupportViewSet(viewsets.ModelViewSet):

    def list(self, request, *args, **kwargs):
        return Response(data={'title': 'Контакты и поддержка'})
