# Copyright (C) 2015, University of Notre Dame
# All rights reserved

from django.test import TestCase, Client
from io import BytesIO

from django.urls.base import reverse
from website.database_apps.big_brother.middleware import BigBrotherMiddleware
from website.database_apps.big_brother.models import PageVisit, TrackingCode
from website.database_apps.invitation_manager.models import PortalEmailConfirmation
from website.database_apps.subject_manager.models import Subject


class TestBigBrotherMiddleware(TestCase):
    def setUp(self):
        self.middleware = BigBrotherMiddleware()

    def test1(self):
        c = Client()
        response = c.get("/")
        page_visit = PageVisit.objects.get(url="/")
        self.assertEqual(page_visit.http_code, "302")
        self.assertIsNone(page_visit.user)
        self.assertEqual(page_visit.url, "/")

    def test_page_visit_post_ascii(self):
        self.client.post("/", data={"file": BytesIO("1234")})
        page_visit = PageVisit.objects.get(url="/")
        # Django test client (as of v1.10) only allows form-encoded data
        # POST content is something like
        # print page_visit.post_content
        # --BoUnDaRyStRiNg
        # Content-Disposition: form-data; name="file"; filename="file"
        # Content-Type: application/octet-stream
        #
        # 1234
        # --BoUnDaRyStRiNg--
        self.assertIn("1234", page_visit.post_content)

    def test_page_visit_post_binary(self):
        data = "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10"
        self.client.post("/", data={"data": BytesIO(data)})
        page_visit = PageVisit.objects.get(url="/")
        # Django test client (as of v1.10) only allows form-encoded data
        # Note that encode('string_escape') in big brother middleware converts \x09 to \t, \0x0a to \n and so on
        self.assertIn(
            "\\x00\\x01\\x02\\x03\\x04\\x05\\x06\\x07\\x08\\t\\n\\x0b\\x0c\\r\\x0e\\x0f\\x10",
            page_visit.post_content,
        )

    def test_page_visit_post_binary_2(self):
        # content = "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0f\xff"
        content = ""
        for ch in range(0, 256):
            content += chr(ch)
        self.client.post("/", data={"test": BytesIO(content)})
        page_visit = PageVisit.objects.get(url="/")
        # Django test client (as of v1.10) only allows form-encoded data
        # Note that encode('string_escape') in big brother middleware converts \x0a to \t etc
        self.assertIn(
            "\\x00\\x01\\x02\\x03\\x04\\x05\\x06\\x07\\x08\\t\\n\\x0b\\x0c\\r\\x0e\\x0f\\x10",
            page_visit.post_content,
        )


class TestPageViewModel(TestCase):
    def test_str(self):
        page_visit = PageVisit.objects.create(user_id=1, url="/subject_manager/")
        self.assertEqual(page_visit.url, "/subject_manager/")
        self.assertEqual(str(page_visit), "/subject_manager/")


class TrackingCodeViewTest(TestCase):
    def test(self):
        response = self.client.get(reverse("big_brother.track", kwargs={"tracking_code": "aaaaa"}))
        self.assertEqual(response.status_code, 200)
        tracking_code = TrackingCode.objects.all()[0]
        self.assertEqual(tracking_code.code, "aaaaa")


class TrackInvitationCodeViewTest(TestCase):
    def test_confirmation_code_no_subject(self):
        confirmation = PortalEmailConfirmation.objects.create(email="1232@example.com", is_invited=False)
        client = Client()
        url = reverse("big_brother.track", kwargs={"tracking_code": confirmation.confirmation_code})
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.content), 95)
        # Tracking code should be created
        tracking_code = TrackingCode.objects.all()[0]
        self.assertEqual(tracking_code.code, confirmation.confirmation_code)
        self.assertEqual(tracking_code.ip, "127.0.0.1")
        self.assertEqual(tracking_code.action, "GET")

    def test_confirmation_code_with_subject(self):
        subject = Subject.objects.create(created_by_id=1)
        confirmation = PortalEmailConfirmation.objects.create(
            email="1232@example.com",
            subject=subject,
            is_invited=True
        )
        client = Client()
        url = reverse("big_brother.track", kwargs={"tracking_code": confirmation.confirmation_code})
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.content), 95)
        # Tracking code should be created
        tracking_code = TrackingCode.objects.all()[0]
        self.assertEqual(tracking_code.code, confirmation.confirmation_code)
        self.assertEqual(tracking_code.ip, "127.0.0.1")
        self.assertEqual(tracking_code.action, "GET")

    def test_wrong_invitation_code(self):
        client = Client()
        url = reverse("big_brother.track", kwargs={"tracking_code": "123"})
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.content), 95)
        # Tracking code should be created even though confirmation doesn't exist
        tracking_code = TrackingCode.objects.all()[0]
        self.assertEqual(tracking_code.code, "123")
