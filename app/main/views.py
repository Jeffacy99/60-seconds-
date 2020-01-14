from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
import datetime
from .forms import PitchForm

from . import main
from ..models import User, Pitch

# Views
@main.route('/')
def index():
    title = 'Pitches App'
    pitches = Pitch.get_pitches()

    return render_template('index.html', title=title, pitches=pitches)


@main.route('/pitch/<int:id>', methods=['GET', 'POST'])
def pitch(id):
    pitch = Pitch.get_single_pitch(id)
    posted_date = pitch.posted.strftime('%b %d, %Y')

    if request.args.get("like"):
        pitch.likes = pitch.likes + 1

        db.session.add(pitch)
        db.session.commit()

        return redirect("/pitch/{pitch_id}".format(pitch_id=pitch.id))
    elif request.args.get("dislikes"):
        pitch.dislikes = pitch.dislikes + 1

        db.session.add(pitch)
        db.session.commit()

        return redirect("/pitch/{pitch_id}".format(pitch_id=pitch.id))
    return render_template('pitch.html', pitch=pitch, date=posted_date)


@main.route('/pitch/new', methods=['GET', 'POST'])
@login_required
def new_pitches():
    pitch_form = PitchForm()
    if pitch_form.validate_on_submit():
        # title = request.form['title']
        # Comment = request.form['comment']

        # updating pitch instance
        if pitch_form.validate_on_submit():
            new_pitch = Pitch(content=pitch_form.description.data, user=current_user, likes=0, dislikes=0)
            # save pitch
            new_pitch.save_pitch()
            return redirect(url_for('main.index'))

    title = 'New Pitch'
    return render_template('new_pitches.html', title=title, pitch_form=pitch_form)
