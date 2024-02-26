from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from urllib.request import urlopen
import environ
import requests
import json

class PostListView(APIView):
    def __init__(self):
        super().__init__()
        self.env = environ.Env(DEBUG=(bool, False))
        
    def post(self, request):
        required_fields = ['username', 'title', 'content']

        for field in required_fields:
            if field not in request.data or not request.data[field]:
                return Response({'error': f'Insert the field "{field}".'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        try:
            response = requests.post(self.env('EXTERNAL_API_URL'), json=request.data)
            response.raise_for_status()
            return Response(response.json(), status=response.status_code)
        except requests.RequestException as e:
            return Response({'error': f'Error when creating post: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get(self, request):
        try:
            with urlopen(self.env('EXTERNAL_API_URL')) as response:
                data = json.loads(response.read())
                return Response(data)
        except requests.RequestException as e:
            return Response({'error': f'Error when fetching posts: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, id):
        try:
            response = requests.patch(f'{self.env('EXTERNAL_API_URL')}{id}/', json=request.data)
            response.raise_for_status()
            return Response(response.json(), status=response.status_code)
        except requests.RequestException as e:
            return Response({'error': f'Error when updating post: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, id):
        try:
            response = requests.delete(f'{self.env('EXTERNAL_API_URL')}{id}/')
            response.raise_for_status()
            return Response({'message': 'Post deleted successfully'}, status=response.status_code)
        except requests.RequestException as e:
            return Response({'error': f'Error when deleting post: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)