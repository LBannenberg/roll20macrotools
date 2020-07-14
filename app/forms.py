from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, FieldList, Form, FormField, RadioField
from wtforms.validators import DataRequired
from wtforms.fields import html5 as h5fields
from wtforms.widgets import html5 as h5widgets


class KeyValuePair(Form):
    """ https://www.rmedgar.com/blog/dynamic-fields-flask-wtf """
    key = StringField('Key')
    value = StringField('Value')


class MainDefaultMacroForm(FlaskForm):
    """ https://www.rmedgar.com/blog/dynamic-fields-flask-wtf """
    name = StringField('Name', validators=[DataRequired()], render_kw={'autofocus': True})
    pairs = FieldList(
        FormField(KeyValuePair),
        min_entries=3,
        max_entries=20
    )
    build = SubmitField('Build It!')
    restart = SubmitField('Start Over!')


class SavesMacroForm(FlaskForm):
    fortitude = h5fields.IntegerField('Fortitude', validators=[DataRequired()], render_kw={'autofocus': True})
    reflex = h5fields.IntegerField('Reflex', validators=[DataRequired()])
    will = h5fields.IntegerField('Will', validators=[DataRequired()])
    notes = StringField('Notes')
    build = SubmitField('Build It!')
    restart = SubmitField('Start Over!')


class StarfinderAttackMacroForm(FlaskForm):
    weapon = StringField('Weapon', validators=[DataRequired()], render_kw={'autofocus': True})
    to_hit = h5fields.IntegerField('To Hit', validators=[DataRequired()])
    ac_type = RadioField('AC', choices=[('KAC', 'KAC'), ('EAC', 'EAC')], validators=[DataRequired()])
    damage = StringField('Damage', validators=[DataRequired()])
    damage_type = StringField('Damage Type', validators=[DataRequired()])
    full_attack_penalty = h5fields.IntegerField('Full Attack Penalty', default=-4, validators=[DataRequired()])
    rider_effects = StringField('Rider Effects')
    ask_to_hit_modifier = BooleanField('Ask to hit modifiers', default='')
    ask_damage_modifier = BooleanField('Ask damage modifiers', default='')
    build = SubmitField('Build It!')
    restart = SubmitField('Start Over!')