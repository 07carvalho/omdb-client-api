from backend import test


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

    def test_login(self):
        resp = self.api_client.post(
            "user.create", dict(email="test@gmail.com", password="test")
        )
        access_token = resp.get("access_token")
        self.assertEqual(resp.get("error"), None)
        resp = self.api_client.post("user.me", headers=dict(authorization=access_token))
        self.assertEqual(resp.get("email"), "test@gmail.com")

    def test_logout(self):
        resp = self.api_client.post(
            "user.create", dict(email="test@gmail.com", password="test")
        )
        access_token = resp.get("access_token")
        self.assertEqual(resp.get("error"), None)
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

    def test_search(self):
        resp = self.api_client.post(
            "user.create", dict(email="test@gmail.com", password="test", name="test")
        )
        access_token = resp.get("access_token")
        self.assertEqual(resp.get("error"), None)
        resp = self.api_client.post(
            "user.search", dict(search="test"), headers=dict(authorization=access_token)
        )
        self.assertEqual(len(resp.get("users")), 1)

    def test_update_password(self):
        resp = self.api_client.post(
            "user.create", dict(email="test@gmail.com", password="test")
        )
        access_token = resp.get("access_token")
        self.assertEqual(resp.get("error"), None)
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

    def test_update_email(self):
        resp = self.api_client.post(
            "user.create", dict(email="test@gmail.com", password="test")
        )
        access_token = resp.get("access_token")
        self.assertEqual(resp.get("error"), None)
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
