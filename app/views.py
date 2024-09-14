from flask import Blueprint, redirect, render_template, request, flash, url_for
from flask_login import login_required, current_user
from .models import ServiceMode
from .forms import NationForm
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
    form = NationForm()
    form.mode.choices = [(mode.id, mode.name) for mode in ServiceMode.query.all()]
    form.mode.choices.insert(0, (0, 'Select Service First'))
    if request.method == 'POST':
        if form.validate_on_submit():
            flash(f'Success, {form.nation_name.data} was added', category='success')
            print(form.data)
        else:
             # Print out each field's errors
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Error in {getattr(form, field).label.text}: {error}")
            flash('Invalid Nation submission', category='error')
            return redirect(url_for('views.dashboard'))

    return render_template("core/dashboard.html", form=form, user=current_user)

#modes endpoint for dependent select
@views.route('/get_modes', methods=['POST'])
@login_required
def get_modes():
    service = request.form.get('service', type=str)

    if service == 'issue_handler':
        modes = ServiceMode.query.filter(ServiceMode.id <= 27).all()
    elif service == 'score_maximizer' or service == 'score_minimizer':
        modes = ServiceMode.query.filter(ServiceMode.id > 27, ServiceMode.id <= 107).all()
    else:
        modes = ServiceMode.query.filter_by(id=108).all()

    return render_template("core/select_mode_response.html", modes=modes)

@views.route('/create-nation', methods=['POST'])
@login_required
def create_nation():
    pass

@views.route('/update-nation', methods=['POST'])
@login_required
def update_nation():
    pass

@views.route('/delete-nation', methods=['POST'])
@login_required
def delete_nation():
    pass