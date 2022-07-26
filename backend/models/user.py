from __future__ import annotations

import datetime
import hashlib
import random
import re
from typing import Union

from google.cloud import ndb

from backend.exceptions import CredentialsInvalid, EmailInvalid, EmailTaken
from backend.models import base


class UserCredentials(base.BaseModel):
    email = ndb.StringProperty(indexed=True)
    email_verified = ndb.BooleanProperty(indexed=False)
    password = ndb.StringProperty(indexed=True)
    salt = ndb.StringProperty(indexed=True)

    @classmethod
    def create(cls, user: str, email: str, password: str) -> UserCredentials:
        salt = "%040x" % random.getrandbits(160)

        entity = cls(
            parent=user.key,
            email=email,
            email_verified=False,
            password=cls._hash_password(salt, password),
            salt=salt,
        )
        entity.put()
        return entity

    @classmethod
    def get_by_email(cls, email: str) -> Union[UserCredentials, None]:
        entities = cls.query(cls.email == email).fetch(1)
        return entities[0] if entities else None

    @classmethod
    def get_by_user(cls, user: User) -> Union[UserCredentials, None]:
        entities = cls.query(ancestor=user.key).fetch(1)
        return entities[0] if entities else None

    @classmethod
    def _hash_password(cls, salt: str, password: str) -> str:
        return hashlib.sha512(
            ("%s%s" % (salt, (password or ""))).encode("utf8")
        ).hexdigest()

    @classmethod
    def _legacy_hash_password(cls, salt: str, password: str) -> str:
        return hashlib.sha256(
            ("%s%s" % (salt, (password or ""))).encode("utf8")
        ).hexdigest()

    @property
    def user(self):
        return User.get(self.key.parent().urlsafe())

    def verify(self, password):
        return (
            self._hash_password(self.salt, password) == self.password
            or self._legacy_hash_password(self.salt, password) == self.password
        )

    def verify_email(self) -> bool:
        self.email_verified = True
        self.put()
        return True

    def update_password(self, password):
        self.salt = "%040x" % random.getrandbits(160)
        self.password = self._hash_password(self.salt, password)
        self.put()

    def update_email(self, email):
        self.email = email
        self.email_verified = False
        self.put()

    def update(self, **kwargs):
        updates = [
            setattr(self, key, value)
            for key, value in kwargs.items()
            if getattr(self, key) != value
        ]
        if len(updates) > 0:
            self.put()
        return self


class User(base.BaseModel):
    created = ndb.DateTimeProperty(indexed=False)
    name = ndb.StringProperty(indexed=True)
    phone = ndb.StringProperty(indexed=True)
    normalized_name = ndb.ComputedProperty(
        lambda self: self.name and self.name.lower(), indexed=True
    )

    @classmethod
    def get_by_email(cls, email):
        credentials = UserCredentials.get_by_email(email)
        return credentials.user if credentials else None

    @classmethod
    def login(cls, email, password):
        entity = cls.get_by_email(email)

        if entity is None or not entity.credentials.verify(password):
            raise CredentialsInvalid("No user found with given email and password")
        return entity

    @classmethod
    def search(cls, search, offset=0, limit=25):
        query = cls.query()
        if search is not None and len(search) >= 3:
            query = query.filter(
                cls.normalized_name >= search.lower(),
                cls.normalized_name < search.lower() + "\uFFFD",
            )
        return query.fetch(offset=offset, limit=limit)

    @classmethod
    def create(cls, email=None, password=None, name=None):
        if email is not None:
            if not cls.is_valid_email(email):
                raise EmailInvalid("%s is not a valid email address" % email)
            if cls.get_by_email(email) is not None:
                raise EmailTaken("%s is already in use" % email)

        entity = cls(created=datetime.datetime.now(), name=name)
        entity.put()

        UserCredentials.create(entity, email, password)

        return entity

    @classmethod
    def is_valid_email(cls, email):
        return re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email)

    def update(self, **kwargs):
        updates = [
            setattr(self, key, value)
            for key, value in kwargs.items()
            if getattr(self, key) != value
        ]
        if len(updates) > 0:
            self.put()
        return self

    def update_password(self, current_password, password):
        if not self.credentials.verify(current_password):
            raise CredentialsInvalid("Current password is invalid")

        self.credentials.update_password(password)

    def update_email(self, current_password, email):
        if not self.is_valid_email(email):
            raise EmailInvalid("%s is not a valid email address" % email)

        if self.get_by_email(email) is not None:
            raise EmailTaken("%s is already in use" % email)

        if not self.credentials.verify(current_password):
            raise CredentialsInvalid("Current password is invalid")

        self.credentials.update_email(email)

    @property
    def credentials(self):
        return UserCredentials.get_by_user(self)

    @property
    def email(self):
        return self.credentials.email if self.credentials else None

    def verify_email(self):
        return self.credentials.verify_email()

    @property
    def email_verified(self):
        return self.credentials.email_verified if self.credentials else None
