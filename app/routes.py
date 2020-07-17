from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import MainDefaultMacroForm, SavesMacroForm, StarfinderAttackMacroForm, InitiativeMacroForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/generic_macro', methods=['GET', 'POST'])
def generic_macro():
    form = MainDefaultMacroForm()
    macro = ''
    if form.validate_on_submit():
        if form.build.data:
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
    form = StarfinderAttackMacroForm()
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
    form = SavesMacroForm()
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
    form = InitiativeMacroForm()
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