.. _Tutorial:

Quick Start
===========


Install
-------

.. code:: bash

   pip install macumba_pass


Declaring a model
-----------------


.. code:: python

    import bcrypt
    from macumba_pass import (
        Model, db, MetaData,
        get_or_create_engine,
    )

    metadata = MetaData()
    engine = get_or_create_engine('sqlite:///example.db')

    class User(Model):
        table = db.Table(
            'auth_user',
            metadata,
            db.Column('id', db.Integer, primary_key=True),
            db.Column('email', db.String(100), nullable=False, unique=True),
            db.Column('password', db.String(100), nullable=False, unique=True),
            db.Column('created_at', db.DateTime, default=datetime.now),
            db.Column('updated_at', db.DateTime, default=datetime.now)
        )

        @classmethod
        def create(cls, email, password, **kw):
            email = email.lower()
            password = cls.secretify_password(password)
            return super(User, cls).create(email=email, password=password, **kw)

        def to_dict(self):
            data = self.serialize()
            data.pop('password')
            return data

        @classmethod
        def secretify_password(cls, plain):
            return bcrypt.hashpw(plain, bcrypt.gensalt(12))

        def match_password(self, plain):
            return self.password == bcrypt.hashpw(plain, self.password)

        def change_password(self, old_password, new_password):
            right_password = self.match_password(old_password)
            if right_password:
                secret = self.secretify_password(new_password)
                self.set(password=secret)
                self.save()
                return True

            return False

    metadata.drop_all(engine)
    metadata.create_all(engine)


Creating new records
--------------------

.. code:: python

    data = {
        "email": "octocat@github.com",
        "password": "1234",
    }
    created = User.create(**data)

    assert created.id == 1

    assert created.to_dict() == {
        'id': 1,
    }

    same_user = User.get_or_create(**data)
    assert same_user.id == created.id


Querying
--------

.. code:: python


    user_count = User.count()
    user_list = User.all()

    github_users = User.find_by(email__contains='github.com')
    octocat = User.find_one_by(email='octocat@github.com')

    assert octocat == user_list[0]

    assert octocat.id == 1

    assert user_count == 1


Editing active records
----------------------

.. code:: python


    octocat = User.find_one_by(email='octocat@github.com')

    # modify in memory

    octocat.password = 'much more secure'
    # or ...
    octocat.set(
        password='much more secure',
        email='octocat@gmail.com',
    )

    # save changes (commit transaction and flush db session)
    octocat.save()


    # or ...

    # modify and save changes in a single call
    saved_cat = octocat.update_and_save(
        password='even more secure now',
        email='octocat@protonmail.com',
    )
    assert saved_cat == octocat


Deleting
--------

.. code:: python

    octocat = User.find_one_by(email='octocat@github.com')

    # delete row, commit and flush session
    ghost_cat = octocat.delete()

    # but the copy in memory still has all the data
    assert ghost_cat.id == 1

    # resurrecting the cat
    octocat = ghost_cat.save()
