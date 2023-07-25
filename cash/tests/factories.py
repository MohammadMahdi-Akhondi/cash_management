from django.contrib.auth import get_user_model
import factory

from cash.transaction.models import Category
from .utils import faker


User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save=True

    username = factory.LazyAttribute(lambda _: f'{faker.unique.company()}')
    password = factory.PostGenerationMethodCall('set_password', 'admin_password')


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.LazyAttribute(lambda _: f'{faker.unique.company()}')
