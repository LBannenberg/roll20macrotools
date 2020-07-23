from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, FieldList, Form, FormField, RadioField
from wtforms.validators import DataRequired, NumberRange, Optional
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
    full_attack_penalty = h5fields.IntegerField(
        'Full Attack Penalty',
        default=-4,
        validators=[DataRequired(), NumberRange(min=-4, max=0)]
    )
    number_of_attacks = h5fields.IntegerField(
        'Number of Attacks',
        default=2,
        validators=[DataRequired(), NumberRange(min=1, max=4)]
    )
    rider_effects = StringField('Rider Effects')
    trick_attack_check = h5fields.IntegerField('Trick Attack Bonus', validators=[Optional()])
    trick_attack_damage = StringField('Trick Attack Damage')
    ask_to_hit_modifier = BooleanField('Ask to hit modifiers', default='')
    ask_damage_modifier = BooleanField('Ask damage modifiers', default='')
    build = SubmitField('Build It!')
    restart = SubmitField('Start Over!')


class InitiativeMacroForm(FlaskForm):
    initiative = h5fields.IntegerField('Initiative', validators=[DataRequired()], render_kw={'autofocus': True})
    build = SubmitField('Build It!')
    restart = SubmitField('Start Over!')


class ShipWeaponField(Form):
    weapon_name = StringField('Name')
    range = h5fields.IntegerField("Range", validators=[Optional()])
    weapon_type = RadioField(
        'Type',
        choices=[('direct', 'direct'), ('tracking', 'tracking')],
        validators=[Optional()]
    )
    tracking_speed = h5fields.IntegerField("Tracking Speed", validators=[Optional()])
    facing = RadioField('Facing', choices=[
        ('turret', 'turret'),
        ('forward', 'forward'),
        ('port', 'port'),
        ('starboard', 'starboard'),
        ('aft', 'aft')
    ], validators=[Optional()])
    damage = StringField('Damage')
    special = StringField('Special')
    use_computers = BooleanField("Use computers?")


class StarshipMacroForm(FlaskForm):
    # Ship
    ship_tier = h5fields.IntegerField('Ship Tier', render_kw={'autofocus': True})
    pcu = h5fields.IntegerField('PCU', validators=[Optional()])
    sensors_bonus = h5fields.IntegerField('Sensor Bonus (to Computers)', validators=[Optional()])
    ship_pilot_bonus = h5fields.IntegerField("Ship's Pilot Bonus", validators=[Optional()])
    floating_bonus = h5fields.IntegerField("Floating Bonus (from ship's computer)", validators=[Optional()])
    # Crew
    captain_bluff = h5fields.IntegerField("Captain's Bluff", validators=[Optional()])
    captain_diplomacy = h5fields.IntegerField("Captain's Diplomacy", validators=[Optional()])
    captain_intimidation = h5fields.IntegerField("Captain's Intimidation", validators=[Optional()])
    engineer = h5fields.IntegerField("Engineer", validators=[Optional()])
    gunner = h5fields.IntegerField("Gunner", validators=[Optional()])
    ask_range = BooleanField("Add range query to attack rolls")
    apply_ship_bonuses = BooleanField("Apply ship bonuses to Pilot and Science Officer rolls")
    pilot = h5fields.IntegerField("Pilot", validators=[Optional()])
    science_officer = h5fields.IntegerField("Science Officer", validators=[Optional()])
    # Guns
    weapons = FieldList(
        FormField(ShipWeaponField),
        min_entries=3,
        max_entries=20
    )
    # Form
    build = SubmitField('Build It!')
    restart = SubmitField('Start Over!')





