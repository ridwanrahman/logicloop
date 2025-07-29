from ninja import NinjaAPI
from ninja.security import HttpBearer

# Import your app apis
from users.api import router as users_router


# Custom authentication
class BearerAuth(HttpBearer):
    def authenticate(self, request, token):
        # Simple token authentication
        from django.contrib.auth.models import User
        try:
            user = User.objects.get(auth_token=token)
            if user.is_active:
                return user
        except User.DoesNotExist:
            return None

# create the main API instance
api = NinjaAPI(
    title="Logic Loop API",
    version="1.0.0",
    description="Logic Loop API",
    docs_url="/docs",
    # auth=BearerAuth()
)


# Add routers for each app
api.add_router("/users", users_router, tags=["users"])



# Global exception handler
@api.exception_handler(Exception)
def handle_exception(request, exc):
    return api.create_response(
        request,
        {"error": "Internal server error", "message": str(exc)},
        status=500
    )

# health check endpoint
@api.get("/health", auth=None)
def health_check(request):
    """
    Health check endpoint to verify API is running
    """
    return {"status": "ok", "message": "API is running"}
