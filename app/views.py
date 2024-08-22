from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
from .models import Keep
import json

#contains general routes and endpoints
views = Blueprint('views', __name__)


@views.route('/')
@views.route('/home')
def home():
    return render_template("general/home.html", user=current_user)

@views.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dash():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note too short!', category='error')
        else:
            new_note = Keep(text=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note Added!', category='success')

    return render_template("general/dash.html", user=current_user)




#ENDPOINTS:
@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteID = note['noteId']
    note = Keep.query.get(noteID)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
