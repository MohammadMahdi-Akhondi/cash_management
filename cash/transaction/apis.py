from django.utils.translation import gettext_lazy as _
from django.db import DatabaseError
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework import permissions
from rest_framework import status

from .validators import validate_transaction_id
from .permission import IsOwnerOrAdmin
from . models import Transaction
from . import selectors
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


class UpdateTransactionApi(APIView):
    authentication_classes = (JWTAuthentication, )
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)

    class InputUpdateTransactionSerializer(serializers.Serializer):
        amount = serializers.IntegerField()
        transaction_type = serializers.ChoiceField(
            choices=Transaction.TypeChoices.choices,
        )
        category = serializers.IntegerField()
        date = serializers.DateField()

        def validate_amount(self, amount):
            if amount < 1:
                raise serializers.ValidationError(_('please enter a valid amount'))

            return amount

        def validate_category(self, category):
            category= selectors.get_category_by_id(category_id=category)
            if not category:
                raise serializers.ValidationError(_('category not found'))
    
            return category

    class OutputUpdateTransactionSerializer(serializers.ModelSerializer):
        class Meta:
            model = Transaction
            exclude = ('deleted_at', )

    @extend_schema(
        request=InputUpdateTransactionSerializer,
        responses=OutputUpdateTransactionSerializer,
    )
    def put(self, request, transaction_id):

        transaction = validate_transaction_id(transaction_id)
        self.check_object_permissions(request, transaction)

        serializer = self.InputUpdateTransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            transaction = services.update_transaction(
                transaction=transaction,
                amount=serializer.validated_data.get('amount'),
                transaction_type=serializer.validated_data.get('transaction_type'),
                category=serializer.validated_data.get('category'),
                date=serializer.validated_data.get('date'),
            )

            return Response(
                data=self.OutputUpdateTransactionSerializer(instance=transaction).data,
                status=status.HTTP_200_OK,
            )

        except DatabaseError as e:
            return Response(
                data=f'database error: {e}',
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class DetailTransactionApi(APIView):
    authentication_classes = (JWTAuthentication, )
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)


    class OutputDetailTransactionSerializer(serializers.ModelSerializer):
        class Meta:
            model = Transaction
            exclude = ('deleted_at', )

    @extend_schema(responses=OutputDetailTransactionSerializer)
    def get(self, request, transaction_id):

        transaction = validate_transaction_id(transaction_id)
        self.check_object_permissions(request, transaction)

        return Response(
            data=self.OutputDetailTransactionSerializer(instance=transaction).data,
            status=status.HTTP_200_OK,
        )
