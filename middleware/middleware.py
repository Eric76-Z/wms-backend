import jwt
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from myuser.models import UserProfile
from wms import settings

REQUIRE_LOGIN_JSON = [
    # '/',

]

REQUIRE_LOGIN = [
    # '/',
    '/mywork/bladeapply/',
    '/myuser/userinfo/',
    '/mywork/weldinggunclothesapply/',
    '/mywork/maintenancerecord/'
]

class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print(request.META.get('HTTP_AUTHORIZATION'))
        # if request.META.get('HTTP_AUTHORIZATION'):
        #     token = request.META.get('HTTP_AUTHORIZATION')
        #     decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

        # if request.path in REQUIRE_LOGIN_JSON:
        #     user_id = request.session.get('user_id')
        #     if user_id:
        #         try:
        #             user = User.objects.get(pk=user_id)
        #             request.user = user
        #         except:
        #             data = {
        #                 'status': 302,
        #                 'msg': 'user not avaliable'
        #             }
        #             return JsonResponse(data)
        #     else:
        #         data = {
        #             'status': 302,
        #             'msg': 'not login'
        #         }
        #         return JsonResponse(data)
        # if request.path in REQUIRE_LOGIN:
        #     user_id = request.session.get('user_id')
        #     if user_id:
        #         try:
        #             user = UserProfile.objects.get(pk=user_id)
        #             request.user = user
        #         except:
        #             return redirect(reverse('myuser:userlogin'))
        #     else:
        #         return redirect(reverse('myuser:userlogin'))


