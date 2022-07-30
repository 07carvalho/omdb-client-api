from backend import test
from backend.test.factories import create_user_and_get_access_token


class TestUserApi(test.TestCase):
    def test_create(self):
        resp = self.api_client.post(
            "user.create", dict(email="test@gmail.com", password="test")
        )
        access_token = resp.get("access_token")
        self.assertEqual(resp.get("error"), None)
        resp = self.api_client.post("user.me", headers=dict(authorization=access_token))
        self.assertEqual(resp.get("error"), None)
        self.assertEqual(resp.get("email"), "test@gmail.com")
        resp = self.api_client.post(
            "user.get",
            dict(id=resp.get("id")),
            headers=dict(authorization=access_token),
        )
        self.assertEqual(resp.get("error"), None)
        resp = self.api_client.post(
            "user.email_verified",
            headers=dict(authorization=access_token),
        )
        self.assertFalse(resp.get("email_verified"))

    def test_login(self):
        access_token = create_user_and_get_access_token(self.api_client)

        resp = self.api_client.post("user.me", headers=dict(authorization=access_token))

        self.assertEqual(resp.get("email"), "test@gmail.com")

    def test_logout(self):
        access_token = create_user_and_get_access_token(self.api_client)
        resp = self.api_client.post("user.me", headers=dict(authorization=access_token))
        self.assertEqual(resp.get("email"), "test@gmail.com")

        resp = self.api_client.post(
            "user.logout", headers=dict(authorization=access_token)
        )

        self.assertEqual(resp.get("error"), None)
        resp = self.api_client.post("user.me")
        self.assertTrue(resp.get("error"))

    def test_token(self):
        session = self.api_client.post(
            "user.create", dict(email="test@gmail.com", password="test")
        )
        self.assertEqual(session.get("error"), None)

        resp = self.api_client.post(
            "user.token",
            dict(
                access_token=session.get("access_token"),
                refresh_token=session.get("refresh_token"),
            ),
        )
        self.assertEqual(resp.get("error"), None)
        self.assertTrue(resp.get("access_token") != session.get("access_token"))
        self.assertTrue(resp.get("refresh_token") != session.get("refresh_token"))

        # try to renew an already used refreshtoken
        resp = self.api_client.post(
            "user.token",
            dict(
                access_token=session.get("access_token"),
                refresh_token=session.get("refresh_token"),
            ),
        )
        self.assertTrue(resp.get("error"))

    def test_search_by_name(self):
        access_token = create_user_and_get_access_token(self.api_client)

        resp = self.api_client.post(
            "user.search", dict(search="test"), headers=dict(authorization=access_token)
        )

        self.assertEqual(len(resp.get("users")), 1)

    def test_search_by_email(self):
        access_token = create_user_and_get_access_token(self.api_client)

        resp = self.api_client.post(
            "user.search",
            dict(search="test@gmail.com"),
            headers=dict(authorization=access_token),
        )

        self.assertEqual(len(resp.get("users")), 1)

    def test_update_password(self):
        access_token = create_user_and_get_access_token(self.api_client)

        resp = self.api_client.post(
            "user.update_password",
            dict(current_password="test", password="test2"),
            headers=dict(authorization=access_token),
        )

        self.assertEqual(resp.get("error"), None)
        resp = self.api_client.post(
            "user.login", dict(email="test@gmail.com", password="test2")
        )
        self.assertEqual(resp.get("error"), None)

    def test_update_user(self):
        access_token = create_user_and_get_access_token(self.api_client)

        self.api_client.post(
            "user.update",
            dict(name="new name", phone="9999999999"),
            headers=dict(authorization=access_token),
        )

        resp = self.api_client.post("user.me", headers=dict(authorization=access_token))
        self.assertEqual(resp.get("name"), "new name")
        self.assertEqual(resp.get("phone"), "9999999999")

    def test_update_email(self):
        access_token = create_user_and_get_access_token(self.api_client)

        resp = self.api_client.post(
            "user.update_email",
            dict(current_password="test", email="test2@gmail.com"),
            headers=dict(authorization=access_token),
        )
        self.assertEqual(resp.get("error"), None)
        resp = self.api_client.post(
            "user.login", dict(email="test2@gmail.com", password="test")
        )
        self.assertEqual(resp.get("error"), None)

    def test_verify_email(self):
        access_token = create_user_and_get_access_token(self.api_client)

        resp = self.api_client.post(
            "user.verify_email",
            headers=dict(authorization=access_token),
        )

        self.assertTrue(resp.get("email_verified"))

    def test_email_verified(self):
        access_token = create_user_and_get_access_token(self.api_client)
        self.api_client.post(
            "user.verify_email",
            headers=dict(authorization=access_token),
        )

        resp = self.api_client.post(
            "user.email_verified",
            headers=dict(authorization=access_token),
        )

        self.assertTrue(resp.get("email_verified"))
