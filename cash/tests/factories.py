from django.contrib.auth import get_user_model
import factory

from .utils import faker


User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda _: f'{faker.unique.company()}')
    password = factory.PostGenerationMethodCall('set_password', 'admin_password')
