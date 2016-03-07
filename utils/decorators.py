from django.contrib.auth.decorators import user_passes_test
superuser_required = user_passes_test(lambda u: u.is_superuser)
superuser_required.__doc__ = (
    """
    Decorator for views that checks that the user is superuser, redirecting
    to the log-in page if necessary.
    """
    )