import json
from datetime import datetime

from django.test import TestCase, Client
from unittest import mock

from django.contrib.auth.hashers import check_password

from teachercan.users.models import User
from config.api import api


class UserModelTest(TestCase):
    def test_default_value(self):
        mock_date = datetime(2024, 1, 1, 0, 0, 0, 0)
        with mock.patch("django.utils.timezone.now") as mock_now:
            mock_now.return_value = mock_date
            user: User = User.objects.create_user(
                email="test@test.test",
                password="1234512345!!",
                nickname="test_nickname",
            )
        self.assertEquals(user.email, "test@test.test")
        self.assertTrue(check_password("1234512345!!", user.password))
        self.assertEquals(user.gender, "남")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertEquals(user.joined_at, mock_date)

        mock_update_date = datetime(2024, 1, 2, 0, 0, 0, 0)
        with mock.patch("django.utils.timezone.now") as mock_now:
            mock_now.return_value = mock_update_date
            user.is_superuser = True
            user.save()
        self.assertNotEquals(user.joined_at, mock_update_date)
        self.assertTrue(user.is_staff)


class AuthApiTest(TestCase):
    client = Client(api)

    def test_email_check(self):
        response = self.client.post(
            "/api/auth/signup/validation",
            {"email": "admin@admin.admin"},
            content_type="application/json",
        )
        self.assertEquals(response.status_code, 201)
        self.assertEquals(
            response.json(),
            {
                "success": True,
                "code": 2000,
                "message": "이 이메일은 사용할 수 있어요.",
                "data": None,
            },
        )

        response = self.client.post(
            "/api/auth/signup",
            {
                "email": "admin@admin.admin",
                "password": "1234512345!!",
                "nickname": "test_client",
            },
            content_type="application/json",
        )
        self.assertEquals(response.status_code, 201)

        response = self.client.post(
            "/api/auth/signup/validation",
            {"email": "admin@admin.admin"},
            content_type="application/json",
        )
        self.assertEquals(response.status_code, 409)
        self.assertEquals(
            response.json(),
            {
                "success": False,
                "code": 1102,
                "message": "이메일이 이미 존재해요.",
                "data": None,
            },
        )

        response = self.client.post(
            "/api/auth/signup/validation",
            {"email": "adminadmin.admin"},
            content_type="application/json",
        )
        self.assertEquals(response.status_code, 422)

    def test_signup(self):
        response = self.client.post(
            "/api/auth/signup",
            {
                "email": "admin@admin.admin",
                "password": "1234512345!!",
                "nickname": "test_client",
            },
            content_type="application/json",
        )
        self.assertEquals(response.status_code, 201)

        # 유효성 검사
        response = self.client.post(
            "/api/auth/signup",
            {
                "email": "admin@admin.admin",
                "password": "1234512345!!",
            },
            content_type="application/json",
        )
        self.assertEquals(response.status_code, 422)

        response = self.client.post(
            "/api/auth/signup",
            {
                "email": "admin@admin.admin",
                "password": "1234512345",
                "nickname": "test_client",
            },
            content_type="application/json",
        )
        self.assertEquals(response.status_code, 422)

        response = self.client.post(
            "/api/auth/signup",
            {
                "email": "admin@admin.admin",
                "password": "1234512345!!",
                "nickname": "test_client!@#$%^&*()",
            },
            content_type="application/json",
        )
        self.assertEquals(response.status_code, 422)

        response = self.client.post(
            "/api/auth/signup",
            {
                "email": "admin@admin.admin",
                "password": "1234512345!!",
                "nickname": "tooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo_long_test_client",
            },
            content_type="application/json",
        )
        self.assertEquals(response.status_code, 422)

        response = self.client.post(
            "/api/auth/signup",
            {
                "email": "admin@admin.admin",
                "password": "1234512345!!",
                "nickname": "test_client",
            },
            content_type="application/json",
        )
        self.assertEquals(response.status_code, 409)

    def test_signin(self):
        response = self.client.post("/api/auth/signin", {"email": "admin"})
