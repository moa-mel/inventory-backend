from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)

#users should be able to register as either an investor or a regular user
class RegisterView(APIView):
    def post(self, request):
        User = get_user_model()  # Get the custom user model dynamically
        email = request.data.get("email")
        password = request.data.get("password")
        user_type = request.data.get("user_type", "REGULARUSER")  # Default to REGULARUSER

        if not email or not password:
            return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "User with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(email=email, password=password, user_type=user_type)

            # Generate a token for account activation
            activation_token = str(RefreshToken.for_user(user).access_token)
            activation_link = f"http://127.0.0.1:5000/api/v1/activate/?token={activation_token}"

            send_mail(
                subject="Activate Your Account",
                message=f"Click the link to activate your account: {activation_link}",
                from_email="noreply@example.com",  # Replace with a valid from_email
                recipient_list=[email],
                fail_silently=False,
            )

            return Response(
                {
                    "message": "Registration successful. Please check your email to activate your account.",
                    "activation_link": activation_link,
                },
                status=status.HTTP_201_CREATED,
            )
        except BadHeaderError:
            logger.error("Invalid header found while sending activation email.")
            return Response({"error": "Invalid header found in the email."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(f"An error occurred during registration: {str(e)}")
            return Response({"error": "An unexpected error occurred. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ActivateAccountView(APIView):
    """
    Activates a user's account when provided with a valid activation token.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("activation_token")
        try:
            user_id = RefreshToken(token).payload["user_id"]
            user = User.objects.get(id=user_id)
            if user.is_active:
                return Response({"message": "Account is already activated."}, status=status.HTTP_400_BAD_REQUEST)
            user.is_active = True
            user.save()
            return Response({"message": "Account activated successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    Allows users to log in with their email and password.
    Returns access and refresh tokens upon successful authentication.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        from django.contrib.auth import authenticate

        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(username=email, password=password)
        if user:
            if not user.is_active:
                return Response(
                    {"error": "Account is not activated. Please activate your account."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "user_type": user.user_type,
                    },
                },
                status=status.HTTP_200_OK,
            )
        return Response({"error": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)
    
