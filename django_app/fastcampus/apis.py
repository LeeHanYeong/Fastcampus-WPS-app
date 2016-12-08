from rest_framework.response import Response
from rest_framework.views import APIView


class TestApiView(APIView):
    def get(self, request, *args, **kwargs):
        ret = {
            'msg': 'Get Test',
        }
        return Response(ret)

    def post(self, request, *args, **kwargs):
        ret = {
            'msg': 'Post Test',
        }
        return Response(ret)