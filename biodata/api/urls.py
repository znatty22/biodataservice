from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from biodata.api.views import api_views, other

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'studies', api_views.StudyViewSet)
router.register(r'participants', api_views.ParticipantViewSet)
router.register(r'biospecimens', api_views.BiospecimenViewSet)


# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('health-check', other.health_check)
]
url_patterns = format_suffix_patterns(urlpatterns)
