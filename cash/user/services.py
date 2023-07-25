from django.contrib.auth import get_user_model


User = get_user_model()

def register(*, username: str, password: str) -> User:
    return User.objects.create_user(
        username=username, password=password,
    )
