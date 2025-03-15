# initialising the main  module

import os
from flask import Flask, render_template, Blueprint, request, jsonify, send_from_directory
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
from flask_mail import Mail
from flask_moment import Moment
from flask_socketio import SocketIO

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
socketio = SocketIO()
login_manager.login_view = 'auth.login'

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	mail.init_app(app)
	moment.init_app(app)
	bootstrap.init_app(app)
	db.init_app(app)
	login_manager.init_app(app)
	socketio.init_app(app, cors_allowed_origins="*")
	
	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)	

	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint, url_prefix='/auth')

	from .models import Permission
	@app.context_processor
	def inject_permissions():
		return dict(Permission = Permission)

	@app.errorhandler(404)
	def page_not_found(e):
		return render_template('404.html'), 404

	@app.errorhandler(500)
	def internal_server_error(e):
		return render_template('500.html'), 500
	
	@app.route('/favicon.ico')
	def favicon():
		return send_from_directory(
			os.path.join(app.root_path, 'static'),
			'favicon.ico', mimetype='image/vnd/microsoft.icon'
		)

	return app