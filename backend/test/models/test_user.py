from unittest.mock import patch

from backend import test
from backend.models import user
from backend.test.factories import create_user


class TestUser(test.TestCase):
    def test_create(self):
        obj = user.User.create(email="test@gmail.com", password="test")
        self.assertEqual(obj, user.User.get(obj.id))
        self.assertTrue(obj.email == "test@gmail.com")
        self.assertTrue(obj.credentials.password != "test")
        self.assertRaises(
            user.EmailInvalid, lambda: user.User.create(email="test@", password="test")
        )
        user.User.create(email="test2@gmail.com", password="åäö")

    def test_login(self):
        obj = user.User.create(email="test@gmail.com", password="test")
        self.assertRaises(
            user.CredentialsInvalid,
            lambda: user.User.login("test@gmail.com", "wrong_password"),
        )
        self.assertEqual(obj, user.User.login("test@gmail.com", "test"))
        self.assertEqual(obj, user.User.login("test@gmail.com", "test"))

    def test_email(self):
        user.User.create(email="test@gmail.com", password="test")
        self.assertRaises(
            user.EmailTaken,
            lambda: user.User.create(email="test@gmail.com", password="test"),
        )

        user.User.create(email="test2@gmail.com", password="test")
        self.assertRaises(
            user.EmailTaken,
            lambda: user.User.create(email="test2@gmail.com", password="test"),
        )

    def test_search(self):
        user.User.create("test@gmail.com", "test", name="test")
        self.assertEqual(1, len(user.User.search("test", offset=0)))

    def test_update_password(self):
        obj = user.User.create("test@gmail.com", "test")
        obj.update_password(current_password="test", password="test2")
        self.assertEqual(obj, user.User.login("test@gmail.com", "test2"))

    def test_update_email(self):
        obj = user.User.create("test@gmail.com", "test")
        obj.update_email(current_password="test", email="test2@gmail.com")
        self.assertEqual(obj, user.User.login("test2@gmail.com", "test"))


class TestUserCredentials(test.TestCase):
    def test_create_credentials(self):
        with patch.object(user.UserCredentials, "create") as method_call:
            email = "test@test.gmail"
            password = "password"
            user_entity = user.User.create(
                email=email,
                password=password,
                name="Test User",
            )

            method_call.assert_called_once_with(user_entity, email, password)

    def test_get_by_email(self):
        user_entity = create_user()

        resp = user.UserCredentials.get_by_email("test@test.com")

        self.assertEqual(user_entity.credentials.id, resp.id)

    def test_get_by_user(self):
        user_entity = create_user()

        resp = user.UserCredentials.get_by_user(user_entity)

        self.assertEqual(user_entity.credentials.id, resp.id)

    def test_get_user_as_property(self):
        user_entity = create_user()

        credential_entity = user.UserCredentials.get_by_user(user_entity)

        self.assertEqual(user_entity.__hash__(), credential_entity.user.__hash__())

    def test_verify_user_credentials(self):
        user_entity = create_user()

        resp = user_entity.credentials.verify("password")

        self.assertTrue(resp)

    def test_verify_user_credentials_wrong_password(self):
        user_entity = create_user()

        resp = user_entity.credentials.verify("pass123")

        self.assertFalse(resp)

    def test_verify_email(self):
        user_entity = create_user()

        self.assertFalse(user_entity.credentials.email_verified)

        resp = user_entity.credentials.verify_email()

        self.assertTrue(resp)
        self.assertTrue(user_entity.credentials.email_verified)

    def test_update_password(self):
        user_entity = create_user()
        user_entity.credentials.update_password("pass123")

        resp = user_entity.credentials.verify("password")
        self.assertFalse(resp)

        resp = user_entity.credentials.verify("pass123")
        self.assertTrue(resp)

    def test_update_email(self):
        user_entity = create_user()
        new_email = "test123.new@gmail.com"
        user_entity.credentials.update_email(new_email)

        resp = user_entity.credentials.get_by_email("test@test.com")
        self.assertIsNone(resp)

        resp = user_entity.credentials.get_by_email(new_email)
        self.assertEqual(user_entity.credentials, resp)
        self.assertFalse(user_entity.credentials.email_verified)

    def test_update(self):
        user_entity = create_user()

        resp = user_entity.credentials.update(
            **{"email": "new.test@test.com", "email_verified": True}
        )

        self.assertEqual(resp.email, "new.test@test.com")
        self.assertTrue(resp.email_verified)
