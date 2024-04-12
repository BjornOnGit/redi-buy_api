import requests
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
from .serializers import UserSerializer, PasswordResetRequestSerializer, PasswordResetSerializer, SellerProfileSerializer, BuyerProfileSerializer
from .models import CustomUser, SellerProfile, BuyerProfile
from django.apps import apps
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import redirect
from django.conf import settings

class SignUpView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        self.send_mail_with_template(user_data['email'], 'Sign Up')

        return Response(user_data, status=status.HTTP_201_CREATED)
    
    def send_mail_with_template(to_email, template_name):
        return requests.post(
        "https://api.mailgun.net/v3/your-domain.com/messages",
        auth=("api", settings.MAILGUN_API_KEY),
        data={"from": "Mailgun Sandbox https://api.mailgun.net/v3/sandboxd0988133d21a41338404e299a217a190.mailgun.org/messages",
              "to": [to_email],
              "template": template_name,
              "t:text": "yes"})
    send_mail_with_template("to@example.com", "your-template-name")

signup = SignUpView.as_view()

class SellerVerificationView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        user = request.user
        data = {
            'is_author': user.is_seller
        }
        return Response(data, status=status.HTTP_200_OK)
    
    def patch(self, request):
        user = request.user
        user.is_author = True
        user.save()
        serializer = self.serializer_class(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            self.send_mail_with_template(user['email'], 'Author Verification')
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def send_mail_with_template(to_email, template_name):
        return requests.post(
        "https://api.mailgun.net/v3/your-domain.com/messages",
        auth=("api", settings.MAILGUN_API_KEY),
        data={"from": "Mailgun Sandbox https://api.mailgun.net/v3/sandboxd0988133d21a41338404e299a217a190.mailgun.org/messages",
              "to": [to_email],
              "template": template_name,
              "t:text": "yes"})
    send_mail_with_template("to@example.com", "your-template-name")

seller_verification = SellerVerificationView.as_view()

class PasswordRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        email = request.data['email']
        user = CustomUser.objects.filter(email=email).first()
        if user:
            token = CustomUser.objects.create_password_reset_token(user)
            self.send_mail_with_template(email, 'Password Reset Request')
            return Response({'token': token}, status=status.HTTP_200_OK)
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def send_mail_with_template(to_email, template_name):
        return requests.post(
        "https://api.mailgun.net/v3/your-domain.com/messages",
        auth=("api", settings.MAILGUN_API_KEY),
        data={"from": "Mailgun Sandbox https://api.mailgun.net/v3/sandboxd0988133d21a41338404e299a217a190.mailgun.org/messages",
              "to": [to_email],
              "template": template_name,
              "t:text": "yes"})
    send_mail_with_template("to@example.com", "your-template-name")

password_request = PasswordRequestView.as_view()

class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request):
        token = request.data['token']
        new_password = request.data['new_password']
        confirm_new_password = request.data['confirm_new_password']
        if new_password != confirm_new_password:
            return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
        PasswordReset = apps.get_model('users', 'PasswordReset')
        password_reset = PasswordReset.objects.filter(token=token).first()
        if password_reset and not password_reset.is_expired():
            user = password_reset.user
            CustomUser = apps.get_model('users', 'CustomUser')
            if CustomUser.objects.reset_password(user, token, new_password):
                self.send_mail_with_template(user['email'], 'Password reset confirmation')
                return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
    
    def send_mail_with_template(to_email, template_name):
        return requests.post(
        "https://api.mailgun.net/v3/your-domain.com/messages",
        auth=("api", settings.MAILGUN_API_KEY),
        data={"from": "Mailgun Sandbox https://api.mailgun.net/v3/sandboxd0988133d21a41338404e299a217a190.mailgun.org/messages",
              "to": [to_email],
              "template": template_name,
              "t:text": "yes"})
    send_mail_with_template("to@example.com", "your-template-name")

password_reset = PasswordResetView.as_view()

class GoogleAuthRedirect(generics.GenericAPIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        redirect_url = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY}&response_type=code&scope=https://www.googleapis.com/auth/userinfo.profile%20https://www.googleapis.com/auth/userinfo.email&access_type=offline&redirect_uri=http://127.0.0.1:8000/api/v1/auth/google-redirect"
        return redirect(redirect_url)

google_auth_redirect = GoogleAuthRedirect.as_view()

class GoogleRedirectURIView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        # Extract the authorization code from the request URL
        code = request.GET.get('code')
        
        if code:
            # Prepare the request parameters to exchange the authorization code for an access token
            token_endpoint = 'https://oauth2.googleapis.com/token'
            token_params = {
                'code': code,
                'client_id': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
                'client_secret': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
                'redirect_uri': 'http://127.0.0.1:8000/api/v1/auth/google-redirect',  # Must match the callback URL configured in your Google API credentials
                'grant_type': 'authorization_code',
            }
            
            # Make a POST request to exchange the authorization code for an access token
            response = requests.post(token_endpoint, data=token_params)
            
            if response.status_code == 200:
                access_token = response.json().get('access_token')
                
                if access_token:
                    # Make a request to fetch the user's profile information
                    profile_endpoint = 'https://www.googleapis.com/oauth2/v1/userinfo'
                    headers = {'Authorization': f'Bearer {access_token}'}
                    profile_response = requests.get(profile_endpoint, headers=headers)
                    
                    if profile_response.status_code == 200:
                        data = {}
                        profile_data = profile_response.json()
                        # Proceed with user creation or login
                        user, created = CustomUser.objects.get_or_create(email=profile_data["email"],
                                                                              defaults={'first_name': profile_data["given_name"]})
                        if "family_name" in profile_data:
                            user.last_name = profile_data["family_name"]
                            user.save()
                        refresh = RefreshToken.for_user(user)
                        data['access'] = str(refresh.access_token)
                        data['refresh'] = str(refresh)
                        return Response(data, status.HTTP_201_CREATED)
            else:
                print(f"Error exchanging authorization code for access token: {response.json()}")
        
        return Response({}, status.HTTP_400_BAD_REQUEST)

google_redirect = GoogleRedirectURIView.as_view()

class SellerProfileView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SellerProfileSerializer

    def post(self, request):
        user = request.user
        data = request.data
        data['user'] = user.id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        user = request.user
        seller = SellerProfile.objects.filter(user=user).first()
        if seller:
            serializer = self.serializer_class(seller)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_404_NOT_FOUND)
    
    def patch(self, request):
        user = request.user
        seller = SellerProfile.objects.filter(user=user).first()
        if seller:
            serializer = self.serializer_class(seller, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status=status.HTTP_404_NOT_FOUND)

seller_profile = SellerProfileView.as_view()

class BuyerProfileView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BuyerProfileSerializer

    def post(self, request):
        user = request.user
        data = request.data
        data['user'] = user.id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        user = request.user
        buyer = BuyerProfile.objects.filter(user=user).first()
        if buyer:
            serializer = self.serializer_class(buyer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_404_NOT_FOUND)
    
    def patch(self, request):
        user = request.user
        buyer = BuyerProfile.objects.filter(user=user).first()
        if buyer:
            serializer = self.serializer_class(buyer, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status=status.HTTP_404_NOT_FOUND)

buyer_profile = BuyerProfileView.as_view()

# Create your views here.
