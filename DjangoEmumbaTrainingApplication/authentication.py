from rest_framework.authentication import SessionAuthentication

class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    The Purpose of this class is to override the csrf authentication, for when testing with Postman
    IMPORTANT: DO NOT USE this class as the default in settings.py in production
        REST_FRAMEWORK = {
            'DEFAULT_AUTHENTICATION_CLASSES': (
                'your_app.authentication.CsrfExemptSessionAuthentication',
            )
        }
    Only use this when testing with postman
    """
    def enforce_csrf(self, request):
        return  # Skip CSRF check
