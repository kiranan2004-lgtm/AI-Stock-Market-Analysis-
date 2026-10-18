"""
Authentication backends for StockSense AI platform.
Supports seamless authentication by username or email address, including usernames
with '@' characters (e.g., 'Kiran@123'), with whitespace trimming and case-insensitivity.
"""

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class EmailOrUsernameModelBackend(ModelBackend):
    """
    Authenticate against settings.AUTH_USER_MODEL using either username or email address.
    
    Robust behavior:
    1. Trims leading and trailing whitespace.
    2. Matches case-insensitively against username first. This ensures usernames
       containing '@' characters (such as 'Kiran@123') are correctly identified as
       usernames rather than mistreated as email addresses.
    3. If no matching username is found, matches case-insensitively against email.
    4. Checks password securely via Django's password hasher without bypassing validation.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)

        if not username or not password:
            return None

        clean_identifier = str(username).strip()

        user = None

        # Step 1: Look up by username (case-insensitive)
        try:
            user = UserModel.objects.get(username__iexact=clean_identifier)
        except UserModel.DoesNotExist:
            user = None
        except UserModel.MultipleObjectsReturned:
            # Fallback to exact match if duplicate case-variants exist
            user = UserModel.objects.filter(username=clean_identifier).first()

        # Step 2: If no username matched, look up by email address (case-insensitive)
        if user is None:
            try:
                user = UserModel.objects.get(email__iexact=clean_identifier)
            except UserModel.DoesNotExist:
                user = None
            except UserModel.MultipleObjectsReturned:
                user = UserModel.objects.filter(email__iexact=clean_identifier).first()

        # If user still not found, run default password hasher once to defend against timing attacks
        if user is None:
            UserModel().set_password(password)
            return None

        # Step 3: Verify password and that the user is active
        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None
