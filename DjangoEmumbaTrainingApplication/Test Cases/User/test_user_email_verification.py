from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.utils import timezone
from DjangoEmumbaTrainingApplication.models import OurUser

class UserEmailVerificationTestCase(APITestCase):

    """
    Unit Test Description: In this unit test, we will manually save a user, and will NOT USE the send_verification_email -
    - function. Rather we will use logic similar to it to create the tokens and then use them to verify our email with the -
    - API.
    """

    def setUp(self):

        """
        Function Description: In this setup function, we will first delete any user having the same username or email -
        - as our test username and email.
        We do this to ensure that there will be no clash when we try to save our test user. And that our fresh user will -
        - have a non-verified email.
        :return:
        """

        # This is the setup function, it will run each time before a test case
        self.url = reverse('login_user')
        self.test_email = 'abdurrafay0610@gmail.com'
        self.test_username = 'testuser645363452542'
        self.test_password = 'secure@1234'
        self.test_first_name = 'first'
        self.test_last_name = 'last'

        try:
            # Checking to see if a user is not already registered by this email
            temp_user = OurUser.objects.get(email=self.test_email)
            # If a user having our test email exist, then delete it, as we will be registering a user with this email
            temp_user.delete()
        except Exception as e:
            # If there is no user with that email then good
            pass

        try:
            # Checking to see if a user is not already registered by this username
            temp_user = OurUser.objects.get(username=self.test_username)
            # If a user having our username exist, then delete it, as we will be registering a user with this username
            temp_user.delete()
        except Exception as e:
            # If there is no user with that username then good
            pass

        # Creating the user, so that we can use these credentials to login
        self.user = OurUser.objects.create_user(
            username=self.test_username ,
            email=self.test_email,
            password=self.test_password,
            first_name=self.test_first_name,
            last_name=self.test_last_name
            # email verified is by default false
        )

    def tearDown(self):
        # This function will run each time after a test case is executed
        # Clean up: Delete the user after each test
        try:
            # Checking to see if a user is already registered by this email
            temp_user = OurUser.objects.get(email=self.test_email)
            # If a user having our test email exist, then delete it
            temp_user.delete()
        except Exception as e:
            # If there is no user with that email then good
            pass

        try:
            # Checking to see if a user is not already registered by this username
            temp_user = OurUser.objects.get(username=self.test_username)
            # If a user having our username exist, then delete it
            temp_user.delete()
        except Exception as e:
            # If there is no user with that username then good
            pass

    def test_verify_email_successfully(self):
        """
        Function Description: This is a POSITIVE test case. We are using a valid token to verify an email.

        IMPORTANT: We are not going to use the function registration or send_verification_email
         We will use the token generation logic from send_verification_email function and get the verification link in this function

        :return:
        """

        # Getting the verification link
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)

        # Creating the verify email function and giving it the verification link
        url = reverse('verify_email', kwargs={'uidb64': uid, 'token': token})
        response = self.client.post(url)

        # On Successful email verification
        # return Response({'message': 'Email successfully verified!'}, status=status.HTTP_200_OK)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Email successfully verified!')
        # Checking to see if the user attribute is_email_verified has been turned to true or not
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_email_verified)

    def test_already_verified_email_successfully(self):
        """
       Function Description: This is a POSITIVE test case. We are trying to reverify an already verified email.

       IMPORTANT: We are not going to use the function registration or send_verification_email
        We will use the token generation logic from send_verification_email function and get the verification link in this function

       :return:
       """

        # Getting the verification link
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)

        # Creating the verify email function and giving it the verification link
        url = reverse('verify_email', kwargs={'uidb64': uid, 'token': token})
        response = self.client.post(url)

        # On Successful email verification
        # return Response({'message': 'Email successfully verified!'}, status=status.HTTP_200_OK)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Email successfully verified!')
        # Checking to see if the user attribute is_email_verified has been turned to true or not
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_email_verified)

        #######################################################
        # Email has been verified once, now verifying it again
        #######################################################
        # Getting the verification link

        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)

        # Creating the verify email function and giving it the verification link
        url = reverse('verify_email', kwargs={'uidb64': uid, 'token': token})
        response = self.client.post(url)

        # On re email verification
        # return Response({'message': 'Email already verified.'}, status=status.HTTP_200_OK)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Email already verified.')
        # Checking to see if the user attribute is_email_verified is unchanged
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_email_verified)


    def test_verify_email_invalid_token(self):
        # Valid user id, invalid token
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        invalid_token = 'invalid-token'
        url = reverse('verify_email', kwargs={'uidb64': uid, 'token': invalid_token})

        response = self.client.post(url)

        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid or expired token.', response.json()['error'])

    def test_verify_email_invalid_uid(self):
        # Invalid userId, valid token
        token = default_token_generator.make_token(self.user)
        url = reverse('verify_email', kwargs={'uidb64': 'invaliduid', 'token': token})

        response = self.client.post(url)

        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid user ID.', response.json()['error'])
