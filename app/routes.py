from flask import render_template, flash, redirect, url_for
from app import app
import app.forms as forms
import math


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/generic_macro', methods=['GET', 'POST'])
def generic_macro():
    form = forms.MainDefaultMacroForm()
    macro = ''
    if form.is_submitted():
        if form.build.data and form.validate():
            macro = '&{template:default} {{name= ' + form.name.data + ' }}'
            for idx, pair in enumerate(form.pairs):
                if pair.data['key'] and pair.data['value']:
                    line = '{{ ' + pair.data['key'] + ' = ' + pair.data['value'] + ' }}'
                    macro = macro + ' ' + line
                elif pair.data['value']:
                    form.pairs.errors.append('missing key for line ' + str(idx))
                elif pair.data['key']:
                    form.pairs.errors.append('missing value for line ' + str(idx))
        if form.restart.data:
            return redirect(url_for('generic_macro'))
    return render_template('generic_macro.html', title='Generic Macro', form=form, macro=macro)


@app.route('/starfinder_attack_macro', methods=['GET', 'POST'])
def starfinder_attack_macro():
    form = forms.StarfinderAttackMacroForm()
    single = ''
    full = ''
    trick = ''
    if form.is_submitted():
        if form.build.data and form.validate():
            preamble = '&{template:default} {{name=@{selected|token_name}'
            strike = (
                    '{{strike=' + form.ac_type.data +
                    ' [[1d20 + ' + str(form.to_hit.data) + ' MAP +?{to hit modifier|0}]], ' +
                    'dmg [[' + form.damage.data + '+?{damage modifier|0}]] ' + form.damage_type.data +
                    (
                        ' plus ' + form.rider_effects.data + ' }}' if form.rider_effects.data
                        else ' }}'
                    )
            )
            if not form.ask_to_hit_modifier.data:
                strike = strike.replace('+?{to hit modifier|0}', '')
            if not form.ask_damage_modifier.data:
                strike = strike.replace('+?{damage modifier|0}', '')

            # single strike
            single = preamble + ' attacks}} {{weapon=' + form.weapon.data + '}} '
            single = single + ' ' + strike.replace('MAP', '')

            # optional trick attack
            if form.trick_attack_check.data and form.trick_attack_damage.data:
                trick = (
                        preamble + ' trick attacks}} ' +
                        '{{trick attack = CR [[1d20 + ' + str(form.trick_attack_check.data) + ' -20 ]] }}' +
                        '{{weapon=' + form.weapon.data + '}} ' +
                        strike.replace('MAP', '') +
                        '{{trick damage = [[ ' + form.trick_attack_damage.data + ' ]] }}'
                )

            elif form.trick_attack_check.data:
                trick = 'TRICK ATTACK DAMAGE MISSING'
            elif form.trick_attack_damage.data:
                trick = 'TRICK ATTACK CHECK MISSING'
            else:
                trick = ''

            # full attack
            full_strike = strike.replace('MAP', '+' + str(form.full_attack_penalty.data) + '[FA]')
            full = preamble + ' full attacks}} {{weapon=' + form.weapon.data + '}} '
            full = full + ' ' + full_strike.replace('strike', '1st strike')
            full = full + ' ' + full_strike.replace('strike', '2nd strike')
            if form.number_of_attacks.data >= 3:
                full = full + ' ' + full_strike.replace('strike', '3rd strike')
            if form.number_of_attacks.data == 4:
                full = full + ' ' + full_strike.replace('strike', '4th strike')
        if form.restart.data:
            return redirect(url_for('starfinder_attack_macro'))
    return render_template(
        'starfinder_attack_macro.html',
        title='Starfinder Attack Macro',
        form=form,
        single=single,
        full=full,
        trick=trick
    )


@app.route('/saves_macro', methods=['GET', 'POST'])
def saves_macro():
    form = forms.SavesMacroForm()
    macro = ''
    if form.is_submitted():
        if form.build.data and form.validate():  # valid data -> build macro
            macro = ('&{template:default} {{name=@{selected|token_name} saves}} {{save=?{choose' +
                     '|fortitude, fortitude [[1d20+{modifier}]]'.format(modifier=form.fortitude.data) +
                     '|reflex, reflex [[1d20+{modifier}]]'.format(modifier=form.reflex.data) +
                     '|will, will [[1d20+{modifier}]]'.format(modifier=form.will.data) +
                     '} }}'
                     )
            if form.notes.data:
                macro = macro + ' {{notes=' + form.notes.data + '}}'
        if form.restart.data:  # clear form
            return redirect(url_for('saves_macro'))
    return render_template('saves_macro.html', title='Saving Throws Macro', form=form, macro=macro)


@app.route('/initiative_macro', methods=['GET', 'POST'])
def initiative_macro():
    form = forms.InitiativeMacroForm()
    macro = ''
    if form.is_submitted():
        if form.build.data and form.validate():  # valid data -> build macro
            macro = (
                    '/w gm &{template:default} {{name= @{selected|token_name} rolls initiative }} ' +
                    '{{ initiative = [[1d20 + ' +
                    str(form.initiative.data + round(form.initiative.data/100, 2)) +
                    ' &{tracker} ]] }}'
            )
        if form.restart.data:  # clear form
            return redirect(url_for('initiative_macro'))
    return render_template('initiative_macro.html', title='Initiative Macro', form=form, macro=macro)


@app.route('/starship_macro', methods=['GET', 'POST'])
def starship_macro():
    form = forms.StarshipMacroForm()
    macros = {'placeholder': 'placeholder macro'}
    if form.is_submitted():
        if form.build.data and form.validate():  # valid data -> build macro

            macros = {}
            scale = math.floor(form.ship_tier.data * 1.5)

            floating = form.floating_bonus.data if form.floating_bonus.data else 0

            # ENGINEERING
            if form.engineer.data:
                header = '/w gm &{template:default} {{name=ENGINEER}}'
                actions = '|'.join([
                    'choose action',
                    'divert power to shields ['+str(math.floor(form.pcu.data*0.05))+' points] (DC {t10})',
                    'divert power to engines (DC {t10})',
                    'divert power to weapons (DC {t10})',
                    'hold it together (DC {t15})',
                    'patch glitching system (DC {t10})',
                    'patch malfunctioning system (DC {t15})',
                    'patch wrecked system (DC {t20})',
                    # 'overpower, overpower (DC {t15})',
                    # 'quick fix, quick fix (DC {t20})'
                ]).format(t10=10+scale, t15=15+scale, t20=20+scale)
                switch = '{{ action = ?{' + actions + '} }}'
                roll = '{{ check = [[1d20 + ' + str(form.engineer.data) + ' ?{modifiers|0} ]] }}'
                macros['ENGINEER'] = ' '.join([header, switch, roll])

            # SCIENCE
            if form.science_officer.data:
                sensors = form.sensors_bonus.data if form.sensors_bonus.data else 0
                header = '/w gm &{template:default} {{name=SCIENCE OFFICER}}'
                actions = '{{ action = ?{' + '|'.join([
                    'choose action',
                    'target system',
                    'scan',
                    # 'lock on',
                    # 'improve countermeasures'
                ]) + '}' + ' (DC [[5 + floor(1.5*?{enemy tier}) + ?{enemy countermeasures}]]) }}'
                roll = '{{ check = [[1d20 + ' + str(form.science_officer.data + sensors) + ' + ?{modifiers|0} ]] }}'
                macros['SCIENCE OFFICER'] = ' '.join([header, actions, roll])
                action = '{{action = balance shields (DC ' + str(10+scale) + ') }}'
                macros['SCIENCE: balance'] = ' '.join([header, action, roll])

            # CAPTAIN
            bluff = form.captain_bluff.data if form.captain_bluff.data else 0
            diplomacy = form.captain_diplomacy.data if form.captain_diplomacy.data else 0
            intimidation = form.captain_intimidation.data if form.captain_intimidation.data else 0
            if bluff or intimidation:
                header = '/w gm &{template:default} {{name=CAPTAIN}}'
                action = '{{ action = taunt (DC [[15+?{enemy tier}]])}}'
                check = '{{ check = [[1d20 + ' + str(max(bluff, intimidation)) + ' + ?{modifier|0}]] }}'
                macros['CAPTAIN: taunt'] = ' '.join([header, action, check])
            if diplomacy:
                header = '/w gm &{template:default} {{name=CAPTAIN}}'
                action = '{{ action = encourage (DC 15)}}'
                check = '{{ check = [[1d20 + ' + str(diplomacy) + ' + ?{modifiers|0}]] }}'
                macros['CAPTAIN: encourage'] = ' '.join([header, action, check])
            if intimidation:
                header = '/w gm &{template:default} {{name=CAPTAIN}}'
                action = '{{ action = demand (DC ' + str(15 + scale) + ')}}'
                check = '{{ check = [[1d20 + ' + str(intimidation) + ' + ?{modifiers|0}]] }}'
                macros['CAPTAIN: demand'] = ' '.join([header, action, check])

            # PILOT
            pilot = form.pilot.data if form.pilot.data else 0
            if pilot:
                ship_pilot = form.ship_pilot_bonus.data if form.ship_pilot_bonus.data else 0
                header = '/w gm &{template:default} {{name=PILOT}}'
                # Initiative: by default we use the computer bonus
                action = '{{ action = the pilot rolls initiative }}'
                check = (
                        '{{ check = [[ 1d20 + ' + str(pilot) + '[pilot] + ' +
                        str(ship_pilot) + '[ship] + ' +
                        '?{floating bonus?|' + str(floating) + '}[floating bonus] + ' +
                        '?{modifiers|0}[other] ]] }}'
                )
                macros['PILOT: init'] = ' '.join([header, action, check])
                # Stunts are like initiative, but by default we don't use the computer bonus
                actions = '?{' + '|'.join([
                    'choose stunt',
                    'evade (DC {t10})',
                    'back off (DC {t10})',
                    'barrell roll (DC {t10}) ',
                    'flip and burn (DC {t15})',
                    'flyby (DC 10 + 1.5x enemy tier)',
                    'slide (DC {t10})'
                ]).format(t10=10+scale, t15=15+scale) + '}'
                action = '{{ action = ' + actions + ' }}'
                check = check.replace('?{floating bonus?|' + str(floating) + '}', '?{floating bonus?|0}')
                macros['PILOT: stunt'] = ' '.join([header, action, check])

            # GUNNER
            if form.gunner.data:
                gunnery = form.gunner.data

                for idx, wpn in enumerate(form.weapons):
                    weapon = wpn.data
                    if not weapon['weapon_name']:
                        continue
                    print(weapon)
                    header = '&{template:default} {{name=GUNNERY}}'
                    arc = '{{ arc = ' + weapon['facing'] + ' }}'
                    gun = '{{ weapon = ' + weapon['weapon_name'] + ' }}'

                    # To Hit roll
                    to_hit = (
                            '{{ to hit = SURFACE [[ 1d20 + ' + str(gunnery) +
                            ' + ?{computer|0}[computer] RANGE +?{modifiers|0} ]] }}'
                    )
                    if weapon['weapon_type'] == 'direct':
                        to_hit = to_hit.replace('SURFACE', 'AC')
                    else:
                        to_hit = to_hit.replace('SURFACE', 'TL')
                    if form.ask_range.data:
                        to_hit = to_hit.replace('RANGE', ' - [[ ( ceil( ?{distance to target|0} / ' +
                                                str(weapon['range']) + ' ) -1 ) * 2 ]][range]')
                    else:
                        to_hit = to_hit.replace('RANGE', '')
                    if weapon['use_computers']:
                        to_hit = to_hit.replace('{computer|0}', '{computer|' + str(floating) + '}')
                    if not floating:
                        to_hit = to_hit.replace('+ ?{computer|0}[computer]', '')

                    # Damage
                    damage = '{{ damage = [[ ' + weapon['damage'] + ' ]] }}'

                    # Tracking weapons
                    if weapon['weapon_type'] == 'tracking' and weapon['tracking_speed']:
                        tracking = '{{ tracking speed = ' + str(weapon['tracking_speed']) + ' }}'
                    else:
                        tracking = ''

                    # Special properties
                    if weapon['special']:
                        special = '{{ special = ' + weapon['special'] + ' }}'
                    else:
                        special = ''

                    name = weapon['facing'].upper() + ' ' + weapon['weapon_name']
                    macros[name] = ' '.join([header, arc, gun, to_hit, damage, tracking, special])

            if not macros:
                macros = {'placeholder': 'placeholder macro'}

        if form.restart.data:  # clear form
            return redirect(url_for('starship_macro'))
    return render_template('starship_macro.html', title='Starship Macro', form=form, macros=macros)
