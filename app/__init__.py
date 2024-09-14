import os
from flask import Flask, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail


app = Flask(__name__)
app.config.from_object('app.config.DevelopmentConfig')
db = SQLAlchemy()
mail = Mail(app)

def create_app():
    #Ensure the database directory exists
    os.makedirs(app.config['DATABASE_PATH'], exist_ok=True)

    db.init_app(app)

    #create models
    from .models import User, ServiceMode
    with app.app_context():
        db.create_all()

        #populate ServiceMode
        if not ServiceMode.query.first():
            mode_list = [
                'anarchy', 'authoritarian_democracy', 'benevolent_dictatorship',
                'capitalist_paradise', 'capitalizt', 'civil_rights_lovefest',
                'compulsory_consumerist_state', 'conservative_democracy', 'corporate_bordello',
                'corporate_police_state', 'corrupt_dictatorship', 'democratic_socialists',
                'father_or_mother_knows_best_state', 'free_market_paradise', 'inoffensive_centrist_democracy',
                'iron_fist_consumerists', 'iron_fist_socialists', 'left_leaning_college_state',
                'left_wing_utopia', 'liberal_democratic_socialists', 'libertarian_police_state',
                'moralistic_democracy', 'new_york_times_democracy', 'psychotic_dictatorship',
                'right_wing_utopia', 'scandinavian_liberal_paradise', 'tyranny_by_majority',
                'authoritarianism', 'average_income', 'average_income_of_poor',
                'average_income_of_rich', 'averageness', 'black_market',
                'business_subsidization','charmlessness','cheerfulness',
                'civil_rights','compliance','compassion',
                'corruption','crime','culture',
                'death_rate','defense_forces','economic_freedom',
                'economic_output','eco-friendliness','economy',
                'education','employment','environmental_beauty',
                'foreign_aid','freedom_from_taxation','government_size',
                'health','human_development_index','ideological_radicality',
                'ignorance','income_equality','industry:_arms_manufacturing',
                'industry:_automobile_manufacturing','industry:_basket_weaving','industry:_beverage_sales',
                'industry:_book_publishing','industry:_cheese_exports','industry:_furniture_restoration',
                'industry:_gambling','industry:_information_technology', 'industry:_insurance',
                'industry:_mining','industry:_pizza_delivery','industry:_retail',
                'industry:_timber_woodchipping','industry:_trout_fishing','influence',
                'intelligence','integrity','law_enforcement',
                'lifespan','niceness','nudity',
                'obesity','pacifism','political_apathy',
                'political_freedoms','population','primitiveness',
                'public_healthcare','public_transport','recreational_drug_use',
                'religiousness','residency','rudeness',
                'safety','scientific_advancement','sector:_agriculture',
                'sector:_manufacturing','secularism','social_conservatism',
                'taxation','tourism','weaponization',
                'wealth_gaps','weather','welfare',
                'world_assembly_endorsements','youth_rebelliousness', 'scheduled_logins'
            ]
            modes = []
            for index, name in enumerate(mode_list, start=1):
                service = 'issue_handler' if index <= 27 else 'single_score' if index <= 107 else 'scheduled_logins'
                modes.append(ServiceMode(name=name, service=service))
            db.session.bulk_save_objects(modes)
            db.session.commit()

    #Import/Register Blueprints
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    #login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    @login_manager.unauthorized_handler
    def unauthorized():
        flash('Please log in to access this page.', category='error')
        return redirect(url_for('auth.login'))

    return app

