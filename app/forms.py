from flask import redirect, url_for
from flask_wtf import Form
from wtforms import (BooleanField, HiddenField, SelectField, StringField,
                     TextAreaField)
from wtforms.validators import DataRequired

from app.utils import get_redirect_target, is_safe_url


class RedirectForm(Form):
    """
    Redirects the client to a certain page on submit.

    Use the redirect method to set the redirect URL, as long as the URL is secure.
    If it is not set, the default will be the previous page.

    """

    next = HiddenField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.next.data:
            self.next.data = get_redirect_target() or ''

    def redirect(self, endpoint='index', **values):
        if is_safe_url(self.next.data):
            return redirect(self.next.data)

        target = get_redirect_target()
        return redirect(target or url_for(endpoint, **values))


class WordForm(RedirectForm):
    pass


class NounForm(WordForm):
    singular = StringField('Singular', [DataRequired()])
    plural = StringField('Plural', [DataRequired()])
    gender = SelectField('Gender', choices=[('neuter', 'neuter'),
                                            ('feminine', 'feminine'),
                                            ('masculine', 'masculine')])


class VerbForm(WordForm):
    infinitive = StringField('Infinitive', [DataRequired()])
    past_tense = StringField('Past Tense', [DataRequired()])
    present_perfect_tense = StringField('Present Perfect Tense',
                                        [DataRequired()])
    consonant_change = BooleanField('Consonant Change - 2./3. pers. sgl.')


class AdjectiveForm(WordForm):
    positive = StringField('Positive', [DataRequired()])
    comparative = StringField('Comparative', [DataRequired()])
    superlative = StringField('Superlative', [DataRequired()])


class AdverbForm(WordForm):
    adverb = StringField('Adverb', [DataRequired()])


class ConjunctionForm(WordForm):
    conjunction = StringField('Conjunction', [DataRequired()])


class PrepositionForm(WordForm):
    preposition = StringField('Preposition', [DataRequired()])
    accusative = BooleanField('Accusative')
    dative = BooleanField('Dative')


WordForm.meaning = TextAreaField('Meaning', [DataRequired()])
WordForm.examples = TextAreaField('Examples', [DataRequired()])


class SearchForm(Form):
    search_field = StringField('Search')
