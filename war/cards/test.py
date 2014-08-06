from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from cards.forms import EmailUserCreationForm
from cards.test_utils import run_pyflakes_for_package, run_pep8_for_package
from cards.utils import create_deck
from cards.models import Card, Player

__author__ = 'kevin'
from django.test import TestCase
# class BasicMathTestCase(TestCase):
#     def test_math(self):
#         a = 1
#         b = 1
#         self.assertEqual(a+b, 2)
#
#     def test_failing_case(self):
#         a = 1
#         b = 1
#         self.assertEqual(a+b, 1)
#
class UtilTestCase(TestCase):
    def test_create_deck_count(self):
        """Test that we created 52 cards"""
        create_deck()
        self.assertEqual(Card.objects.count(), 52)

class ModelTestCase(TestCase):
    def test_get_ranking(self):
        """Test that we get the proper ranking for a card"""
        card = Card.objects.create(suit=Card.CLUB, rank="jack")
        self.assertEqual(card.get_ranking(), 11)

    def test_get_war_result(self):
        card = Card.objects.create(suit=Card.CLUB, rank="jack")
        card1 = Card.objects.create(suit=Card.CLUB, rank="queen")
        self.assertEqual(card.get_war_result(card1), -1)

    def test_clean_username_exception(self):
        # Create a player so that this username we're testing is already taken
        Player.objects.create_user(username='test-user')

        # set up the form for testing
        form = EmailUserCreationForm()
        form.cleaned_data = {'username': 'test-user'}

        # use a context manager to watch for the validation error being raised
        with self.assertRaises(ValidationError):
            form.clean_username()

    def test_clean_username_pass(self):
        Player.objects.create_user(username='bla')
        form = EmailUserCreationForm()
        form.cleaned_data = {'username':'test'}
        self.assertEqual(form.clean_username(), 'test')

    def setUp(self):
        create_deck()

    def test_faq_page(self):
        response = self.client.get(reverse('filters'))
        self.assertIn('Capitalized Suit: 3', response.content)

    # def test_login_page(self):
    #     data = {'username':'yo', 'password':'bla'}
    #     response = self.client.post(reverse('login'),data)
    #     pass

class SyntaxTest(TestCase):
    def test_syntax(self):
        """
        Run pyflakes/pep8 across the code base to check for potential errors.
        """
        packages = ['cards']
        warnings = []
        # Eventually should use flake8 instead so we can ignore specific lines via a comment
        for package in packages:
            warnings.extend(run_pyflakes_for_package(package, extra_ignore=("_settings",)))
            warnings.extend(run_pep8_for_package(package, extra_ignore=("_settings",)))
        if warnings:
            self.fail("{0} Syntax warnings!\n\n{1}".format(len(warnings), "\n".join(warnings)))
