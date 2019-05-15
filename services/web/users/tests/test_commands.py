import os
from io import StringIO
from unittest import mock
#https://realpython.com/testing-in-django-part-1-best-practices-and-examples/
#from admin_scripts.tests import AdminScriptTestCase
from django.apps import apps
from django.core import management
from django.core.management import BaseCommand, CommandError, find_commands
from django.core.management.utils import (
    find_command, get_random_secret_key, popen_wrapper,
)
from django.db import connection
from django.test import SimpleTestCase, override_settings, TestCase
from django.test.utils import captured_stderr, extend_sys_path
from django.utils import translation
from users.management.commands import createuser #<-- testing createuser command
from django.test import TestCase
from django.contrib.auth.models import User

# A minimal set of apps to avoid system checks running on all apps. otherwise it will run tests on all installed apps
# this will run tests only on comamnds
@override_settings(
    INSTALLED_APPS=[
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'users',
    ],
)


class CommandTests(TestCase):
    #this is helpful for testing duplicates
    def setUp(self):
        User.objects.create_user(username='john', email='john@doe.com', password='123456')  # <- included this line here

    def test_createuser_positional_args_none(self):
        msg = 'Error: the following arguments are required: username, email, passwd'
        with self.assertRaisesMessage(CommandError, msg):
            management.call_command('createuser')

    def test_createuser_positional_args_onlyusername(self):
        msg = 'Error: the following arguments are required: email, passwd'
        with self.assertRaisesMessage(CommandError, msg):
            management.call_command('createuser', 'dexter')

    def test_createuser_positional_args_username_and_email(self):
        msg = 'Error: the following arguments are required: passwd'
        with self.assertRaisesMessage(CommandError, msg):
            management.call_command('createuser', 'dexter', 'test@test.com')

    def test_createuser_positional_args_threeargs(self):
        out = StringIO()
        management.call_command('createuser', 'eddie', 'eddie@django.com', 'eddie', stdout=out)
        self.assertIn("Successfully created", out.getvalue())

    def test_createuser_positional_args_duplicate(self):
        out = StringIO()
        user = 'john'
        email = 'john@doe.com'
        msg = 'Duplicate user or email {} {}'.format(user, email )
        with self.assertRaisesMessage(CommandError, msg):
            management.call_command('createuser', user, email, '123456')
