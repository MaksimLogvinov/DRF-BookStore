from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from apps.main.views import HomePageViewSet

schema_view = get_swagger_view(title='Main API')

main_router = routers.DefaultRouter()
main_router.register(r'', HomePageViewSet, basename='home_page')
urlpatterns = main_router.urls
