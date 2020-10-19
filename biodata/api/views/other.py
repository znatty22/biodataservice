"""
Views for endpoints that are not part of the biodata CRUD API
"""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def health_check(request):
    """
    Health check endpoint 
    """
    return Response(
        {
            'message': 'Welcome to the biodataservice API',
            'status': status.HTTP_200_OK
        }
    )
