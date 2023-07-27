from django.contrib.auth import get_user_model


User = get_user_model()

def register(*, username: str, password: str) -> User:
    """
    Creates a new user with the given username and password.
    Returns the created User object.
    
    Args:
        username (str): The desired username for the new user.
        password (str): The desired password for the new user.
    
    Returns:
        User: The newly created User object.
    """
    return User.objects.create_user(
        username=username, password=password,
    )
