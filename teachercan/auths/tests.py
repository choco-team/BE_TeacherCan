from django.test import TestCase
from unittest import mock
from datetime import datetime

from django.contrib.auth.hashers import check_password

from teachercan.users.models import User


class UserModelTest(TestCase):
    def test_default_value(self):
        mock_date = datetime(2024, 1, 1, 0, 0, 0, 0)
        with mock.patch("django.utils.timezone.now") as mock_now:
            mock_now.return_value = mock_date
            user: User = User.objects.create_user(
                email="test@test.test", password="1234512345!!"
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
