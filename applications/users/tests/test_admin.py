"""
Tests for the Django admin modifications.
"""
import pytest
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


@pytest.mark.django_db
class AdminSiteTests(TestCase):
    """Tests for Django admin."""

    def setUp(self):
        """Create user and client."""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            first_name="Adam",
            last_name="Test",
            password="testpass123",
            additional_identifier="num.1"
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            username="user",
            first_name="Maria",
            last_name="Doe",
            password="testpass123",
            additional_identifier="num.2"
        )

    def test_users_lists(self):
        """Test that users are listed on page."""
        url = reverse("admin:users_user_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.username)
        self.assertContains(res, self.user.first_name)
        self.assertContains(res, self.user.last_name)
        self.assertContains(res, self.user.is_active)
        self.assertContains(res, self.user.is_staff)
        self.assertContains(res, self.user.additional_identifier)

    def test_edit_user_page(self):
        """Test the edit user page works."""
        url = reverse("admin:users_user_change", args=[self.user.pkid])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test the create user page works."""
        url = reverse("admin:users_user_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
