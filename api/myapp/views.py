from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from .models import Student, Token
from .serializers import StudentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.decorators import api_view
from django.core.mail import EmailMessage
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
import random
from .models import OTP
from django.contrib.auth.models import User

# Student Views
class StudentListView(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentDetailView(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_object(self, id):
        try:
            return Student.objects.get(id=id)
        except Student.DoesNotExist:
            return None

    def get(self, request, id):
        student = self.get_object(id)
        if not student:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StudentSerializer(student)
        return Response(serializer.data)


    def put(self, request, id):
        student = self.get_object(id)
        if not student:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        student = self.get_object(id)
        if not student:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Authentication Views
@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def token_verification_view(request):
    entered_token = request.data.get('token')
    if entered_token:
        try:
            AccessToken(entered_token)
            return Response({'message': 'Token is valid'})
        except (InvalidToken, TokenError):
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Token not provided'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout_view(request):
    response = Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
    response.delete_cookie('access_token')
    return response

@api_view(['GET'])
def view_tokens(request):
    tokens = Token.objects.all()
    return Response({'tokens': [token.key for token in tokens]})

from django.core.mail import EmailMessage
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['POST'])
def test_send_email(request):
    try:
        # Define the HTML content with styling
        html_content = """
        <html>
        <head>
            <style>
                body {
                    font-family: 'Arial', sans-serif;
                    background-color: #f4f4f4;
                    color: #333;
                    padding: 20px;
                }
                .container {
                    background-color: #fff;
                    padding: 20px;
                    border-radius: 5px;
                    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                }
                h1 {
                    color: #333;
                }
                p {
                    font-size: 16px;
                    line-height: 1.5;
                }
                .footer {
                    margin-top: 20px;
                    font-size: 12px;
                    color: #777;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Reset your password</h1>
                <p>Hello,</p>
                <p>You seem to have forgotten your password</p>
                <p>Unortunately,for security reasons we will have to ask you to get the password reset at your nearest branch</p>
                <p>We have attached below , a list of our branches for your convenience </p>
                <p>Best regards,</p>
                <p>Div Sharma</p>
                <div class="footer">
                    <p>This is an automated message, please do not reply.</p>
                </div>
            </div>
        </body>
        </html>
        """

        # Create the email message
        email_message = EmailMessage(
            subject="Email Testing",
            body=html_content,
            from_email="div@gmail.com",
            to=['test@gmail.com'],
        )

        # Attach the file
        email_message.content_subtype = "html"  # Set the content type to HTML
        with open(r"C:\Users\divya\OneDrive\Documents\QWC_InformationForm.xlsx", "rb") as file:
            email_message.attach("QWC_InformationForm.xlsx", file.read())

        # Send the email
        email_message.send(fail_silently=False)
        print("Email has been sent")
    except Exception as e:
        print(f"Unable to send the email due to {str(e)}")

    return Response({"message": "Email sent successfully!"})

@api_view(['POST'])
def generate_otp(request):
    try:
        email = request.data.get('email')
        user = User.objects.get(email=email)
        
        # Generate a random 6-digit OTP
        otp_code = str(random.randint(100000, 999999))
        expires_at = timezone.now() + timedelta(minutes=10)  # OTP expires in 10 minutes
        
        # Save OTP to database
        otp = OTP.objects.create(user=user, otp=otp_code, expires_at=expires_at)
        
        # Define the plain HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Your OTP Code</title>
        </head>
        <body>
            <p>Hello,</p>
            <p>We received a request to verify your email address. Please use the following OTP to complete the verification process:</p>
            <h2>{otp_code}</h2>
            <p>The OTP is valid for 10 minutes. If you did not request this code, please ignore this email.</p>
            <p>Best regards,</p>
            <p>Your Company Team</p>
        </body>
        </html>
        """

        # Prepare and send OTP email
        subject = "Your OTP Code"
        email_message = EmailMessage(
            subject=subject,
            body=html_content,
            from_email="div@gmail.com",  # Replace with your email
            to=[email],
        )
        email_message.content_subtype = "html"  # Set the content type to HTML
        email_message.send(fail_silently=False)
        
        return Response({"message": "OTP sent successfully!"}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
from django.http import JsonResponse

@api_view(['POST'])
def verify_otp(request):
    email = request.data.get('email')
    otp_input = request.data.get('otp')
    
    try:
        # Get the user by email
        user = User.objects.get(email=email)
        
        # Filter by the user's OTP and check if it matches
        otp_record = OTP.objects.filter(user=user, otp=otp_input).first()
        
        if otp_record:
            # Proceed with OTP verification logic
            return JsonResponse({"success": "OTP verified successfully!"})
        else:
            return JsonResponse({"error": "Invalid OTP or email."}, status=400)
    except User.DoesNotExist:
        return JsonResponse({"error": "User does not exist."}, status=400)