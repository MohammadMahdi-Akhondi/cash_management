from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import DatabaseError
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework import status

from .services import register


User = get_user_model()

class RegisterApi(APIView):

    class InputRegisterSerializer(serializers.Serializer):
        username = serializers.CharField(max_length=255)
        password = serializers.CharField(
            max_length=128,
            validators=[validate_password]
        )
        confirm_password = serializers.CharField()

        def validate_username(self, username):
            if User.objects.filter(username=username, deleted_at__isnull=True).exists():
                raise serializers.ValidationError(_('this username already taken'))

            return username


        def validate(self, data):
            if data.get('password') != data.get('confirm_password'):
                raise serializers.ValidationError({
                    'confirm_password': _('confirm password is not equal to password'),
                })

            return data


    class OutputRegisterSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            exclude = ('password', 'deleted_at')

    @extend_schema(request=InputRegisterSerializer, responses=OutputRegisterSerializer)
    def post(self, request):
        serializer = self.InputRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = register(
                username=serializer.validated_data.get('username'),
                password=serializer.validated_data.get('password'),
            )

            return Response(
                data=self.OutputRegisterSerializer(instance=user).data,
                status=status.HTTP_201_CREATED,
            )

        except DatabaseError as e:
            return Response(
                data=f'database error: {e}',
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
