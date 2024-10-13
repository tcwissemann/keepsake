from flask import Blueprint, redirect, render_template, request, flash, url_for
from flask_login import login_required, current_user
from .models import Nation, ServiceMode
from .forms import NationForm
from . import db
#contains general routes and endpoints
views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home')
def home():
    return render_template("base/landing.html", user=current_user)

#rename dashboard
@views.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    nations = get_user_nations()
    remaining_slots = (5-(len(nations)))
    form = nation_form_init()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                create_nation(form)
                flash(f'Success, {form.nation_name.data} was added', category='success')
            except Exception as e:
                flash(f'failure, {form.nation_name.data} was not added error: {e}', category='error')
                print(form.data)
        else:
             # Print out each field's errors
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Error in {getattr(form, field).label.text}: {error}")
            flash('Invalid Nation submission', category='error')
            return redirect(url_for('views.dashboard'))

    return render_template("core/dashboard.html", form=form, user=current_user, nations=nations, remaining_slots=remaining_slots)

#modes endpoint for dependent select
@views.route('/get_modes', methods=['POST'])
@login_required
def get_modes():
    service = request.form.get('service_type', type=str)

    if service == 'issue_handler':
        modes = ServiceMode.query.filter(ServiceMode.id <= 27).all()
    elif service == 'score_maximizer' or service == 'score_minimizer':
        modes = ServiceMode.query.filter(ServiceMode.id > 27, ServiceMode.id <= 107).all()
    else:
        modes = ServiceMode.query.filter_by(id=108).all()

    return render_template("core/select_mode_response.html", modes=modes)

def create_nation(form):
    nation_exists = Nation.query.filter_by(nation_name=form.nation_name.data).first()
    if nation_exists:
        flash('A nation with this name already exists in NSRegent!', category='error')
    else:
        new_nation = Nation(nation_name=form.nation_name.data, nation_password=form.nation_password.data, service_type=form.service_type.data, mode=form.mode.data, user_id=current_user.id)
        db.session.add(new_nation)
        db.session.commit()


@views.route('/delete_nation', methods=['POST'])
@login_required
def delete_nation():
    #htmx to take user from add to the form with alpine focus
    #htmx to delete the nation without page reload
    pass

def get_user_nations():
    nations = Nation.query.filter_by(user_id=current_user.id).all()
    nation_array = []
    for nation in nations:
        nation_array.append(DisplayNation(nation.flag, nation.nation_name, nation.service_type, nation.mode, nation.status, nation.date_created))
    return nation_array

def nation_form_init():
    form = NationForm()
    form.mode.choices = [(mode.id, mode.name) for mode in ServiceMode.query.all()]
    form.mode.choices.insert(0, (0, 'Select Service First'))
    return form
class DisplayNation:
    def __init__(self, flag, nation_name, service_type, mode, status, date_created):
        self.flag = flag
        self.nation_name = nation_name
        self.service_type = service_type
        self.mode = mode
        self.status = status
        self.date_created = date_created