from django.contrib.auth.tokens import PasswordResetTokenGenerator

class UserActivationToken(PasswordResetTokenGenerator):

     def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) +
            user.password +
            str(user.last_login) +
            str(user.is_active) +
            str(timestamp)
        )

