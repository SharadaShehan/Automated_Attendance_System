from api.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        response.data['style_guide'] = token.user.company.style_guide

        return response
