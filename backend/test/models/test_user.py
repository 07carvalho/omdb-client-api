from backend import test
from backend.models import user


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
