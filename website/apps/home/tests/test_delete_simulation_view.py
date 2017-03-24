# Copyright (C) 2016, University of Notre Dame
# All rights reserved
from django.contrib.auth.models import User
from django.test.client import Client
from django.test.testcases import TestCase
from django.urls.base import reverse

from website.apps.home.models import Simulation


class DeleteSimulationViewTest(TestCase):
    def setUp(self):
        admin = User.objects.create(username="admin")
        admin.set_password("1")
        admin.is_superuser = True
        admin.is_staff = True
        admin.save()
        self.simulation = Simulation.objects.create()
        self.url = reverse("simulation.delete", kwargs={"simulation_id": self.simulation.id})
        self.client.login(username="admin", password="1")

    def test_anonymous(self):
        client = Client()
        response = client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_non_admin(self):
        user = User.objects.create(username="user")
        user.set_password("1")
        user.save()
        client = Client()
        client.login(username="user", password="1")
        self.assertEqual(Simulation.objects.all().count(), 1)
        response = client.get(self.url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Simulation.objects.all().count(), 1)

    def test_success(self):
        self.assertEqual(Simulation.objects.all().count(), 1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("home.display_simulations"))
        self.assertEqual(Simulation.objects.all().count(), 0)
