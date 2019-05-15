# Create your views here.
#from rest_framework.response import Response
from django.http import JsonResponse

def home(request):
    """
    Display home page.
    """
    #return Response({'data': 'You must suffix api/<feature>'})
    return JsonResponse({'error': 'This page is forbidden'}, status=403)
