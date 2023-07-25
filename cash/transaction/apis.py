from django.utils.translation import gettext_lazy as _
from django.db import DatabaseError
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework import permissions
from rest_framework import status

from . models import Transaction
from . import services


class CreateTransactionApi(APIView):
    authentication_classes = (JWTAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    class InputCreateTransactionSerializer(serializers.ModelSerializer):
        class Meta:
            model = Transaction
            fields = (
                'amount',
                'transaction_type',
                'category',
                'date'
            )

    class OutputCreateTransactionSerializer(serializers.ModelSerializer):
        class Meta:
            model = Transaction
            exclude = ('deleted_at', )

    @extend_schema(
        request=InputCreateTransactionSerializer,
        responses=OutputCreateTransactionSerializer,
    )
    def post(self, request):
        serializer = self.InputCreateTransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            transaction = services.create_transaction(
                user=request.user,
                amount=serializer.validated_data.get('amount'),
                transaction_type=serializer.validated_data.get('transaction_type'),
                category=serializer.validated_data.get('category'),
                date=serializer.validated_data.get('date'),
            )

            return Response(
                data=self.OutputCreateTransactionSerializer(instance=transaction).data,
                status=status.HTTP_201_CREATED,
            )

        except DatabaseError as e:
            return Response(
                data=f'database error: {e}',
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
