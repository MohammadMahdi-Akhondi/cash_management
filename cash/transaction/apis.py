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
from cash.api import pagination
from . import selectors
from . import services


class CreateTransactionApi(APIView):
    """
    API endpoint for creating a new Transaction object.
    """

    authentication_classes = (JWTAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    class InputCreateTransactionSerializer(serializers.ModelSerializer):
        """
        Serializer class for validating input when creating a new Transaction object.
        """

        class Meta:
            model = Transaction
            fields = (
                'amount',
                'transaction_type',
                'category',
                'date'
            )

    class OutputCreateTransactionSerializer(serializers.ModelSerializer):
        """
        Serializer class for returning output when creating a new Transaction object.
        """

        class Meta:
            model = Transaction
            exclude = ('deleted_at', )

    @extend_schema(
        request=InputCreateTransactionSerializer,
        responses=OutputCreateTransactionSerializer,
    )
    def post(self, request):
        """
        This endpoint for create a new Transaction object with the given input data and returns it in the output format.
        """

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
                data={'detail': f'database error: {e}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UpdateTransactionApi(APIView):
    """
    API endpoint for updating an existing Transaction object.
    """

    authentication_classes = (JWTAuthentication, )
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)

    class InputUpdateTransactionSerializer(serializers.Serializer):
        """
        Serializer class for validating input when updating an existing Transaction object.
        """

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
        """
        This endpoint for Update an existing Transaction object with the given input data and returns it in the output format.
        """

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
                data={'detail': f'database error: {e}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class DetailTransactionApi(APIView):
    """
    API endpoint for retrieving details of a Transaction object.
    """

    authentication_classes = (JWTAuthentication, )
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)

    class OutputDetailTransactionSerializer(serializers.ModelSerializer):
        """
        Serializer class for returning output when retrieving details of a Transaction object.
        """
        class Meta:
            model = Transaction
            exclude = ('deleted_at', )

    @extend_schema(request=None, responses=OutputDetailTransactionSerializer)
    def get(self, request, transaction_id):
        """
        This endpoint for retrieve the details of a Transaction object with the given ID and returns it in the output format.
        """

        transaction = validate_transaction_id(transaction_id)
        self.check_object_permissions(request, transaction)

        return Response(
            data=self.OutputDetailTransactionSerializer(instance=transaction).data,
            status=status.HTTP_200_OK,
        )


class DeleteTransactionApi(APIView):
    """
    API endpoint for deleting an existing Transaction object.
    """

    authentication_classes = (JWTAuthentication, )
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)

    @extend_schema(request=None, responses=None)
    def delete(self, request, transaction_id):
        """
        This endpoint for delete an existing Transaction object with the given ID.
        
        Args:
            transaction_id: The ID of the Transaction object to delete.
        
        Returns:
            Response: A HTTP 204 No Content response indicating the deletion was successful.
        """

        transaction = validate_transaction_id(transaction_id)
        self.check_object_permissions(request, transaction)
        services.delete_transaction(transaction=transaction)

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


class ListTransactionApi(APIView):
    """
    API endpoint for listing Transaction objects with filtering and pagination.
    """

    authentication_classes = (JWTAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    class Pagination(pagination.LimitOffsetPagination):
        """
        Pagination class for limiting the number of Transaction objects returned in a single request.
        """

        default_limit = 10

    class InputListTransactionSerializer(serializers.Serializer):
        """
        Serializer class for validating input when listing Transaction objects with filtering.
        """

        date = serializers.DateField(required=False)
        category__in = serializers.CharField(required=False)
        amount__range = serializers.CharField(required=False)
        transaction_type = serializers.ChoiceField(
            required=False,
            choices=Transaction.TypeChoices.choices,
        )
        order_by = serializers.ChoiceField(
            required=False,
            choices=[
                'amount',
                'category',
                'date',
                'transaction_type'
            ],
        )
        date__range = serializers.ChoiceField(
            required=False,
            choices=(
                'today',
                'yesterday',
                'week',
                'month',
                'year',
            )
        )

    class OutputListTransactionSerializer(serializers.ModelSerializer):
        class Meta:
            model = Transaction
            exclude = ('deleted_at', )

    @extend_schema(
        parameters=[InputListTransactionSerializer],
        responses=OutputListTransactionSerializer,
    )
    def get(self, request):
        """
        This endpoint for list Transaction objects with filtering and pagination based on the given input parameters.
        
        Queries:

            date: Filter transactions by exact date

            category__in: Filter transactions based on categories ID.
                for example: category__in=1,2,3

            amount__range: Filter transactions based on amount range.
                for example: amount__range=10, 100

            transaction_type: Filter transactions based on type of transaction

            date__range: Filter transactions based on date range.
                for example: week

            order_by: Order transaction based on transaction fields
                for example: amount
        
        Returns:
            Response: A paginated list of Transaction objects in the output format.
        """

        filter_serializer = self.InputListTransactionSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        try:
            query = selectors.list_transaction(
                order_by=filter_serializer.validated_data.pop('order_by', 'date'),
                filters=filter_serializer.validated_data,
                user=request.user,
            )

        except Exception as e:
            return Response(
                data={'detail': 'Filter Error - ' + str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return pagination.get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=self.OutputListTransactionSerializer,
            queryset=query,
            request=request,
            view=self,
        )


class BalanceApi(APIView):
    """
    API endpoint for retrieving the balance of a user's Transaction objects.
    """

    authentication_classes = (JWTAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    class OutputBalanceSerializer(serializers.Serializer):
        """
        Serializer class for returning output when retrieving the balance of a user's Transaction objects.
        """
        balance = serializers.IntegerField()

    @extend_schema(request=None, responses=OutputBalanceSerializer)
    def get(self, request):
        """
        This endpoint for Retrieve the balance of a user's Transaction objects and returns it in the output format.
        """
        data = {
            'balance': selectors.get_balance(user=request.user),
        }
        return Response(
            data=self.OutputBalanceSerializer(instance=data).data,
            status=status.HTTP_200_OK,
        )
