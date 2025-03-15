
# python file for handling user views
# Create role based views for users and provider/admin panel

from datetime import date, datetime, timezone
import os
from flask import (app, render_template, request,
				session, flash, current_app,
				redirect, url_for, send_from_directory)
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required, login_user
from app.email import send_email
from . import main
from .forms import EditProfileForm, RareDiseaseRegistryForm, ArticleUploadForm
from ..auth.forms import LoginForm, RegistrationForm
from .. import db, socketio
from..models import Role, User, Test, TestOrder, Article, Clinic

@main.route('/', methods=['GET', 'POST'])
def index():
	login_form = LoginForm()
	register_form = RegistrationForm()
	
	if login_form.validate_on_submit():
		user = User.query.filter_by(email=login_form.email.data).first()
		if user is not None and user.verify_password(login_form.password.data):
			login_user(user, login_form.remember_me.data)
			return redirect(request.args.get('next') or url_for('main.user_portal'))
		flash('Invalid username or password.')

	if register_form.validate_on_submit():
		user = User(
			email=register_form.email.data,
			username=register_form.username.data,
			password=register_form.password.data,
			role=Role.query.filter_by(default=True).first()
		)
		db.session.add(User)
		db.session.commit
		flash('You can now proceed to login.')
		return redirect(url_for('auth.login'))
	return render_template(
						'index.html',
						login_form=login_form,
						register_form=register_form,
						current_time=datetime.now(timezone.utc))


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm()
	if form.validate_on_submit():
		current_user.name = form.name.data
		current_user.location = form.location.data
		db.session.add(current_user._get_current_object())
		db.session.commit()
		flash('Your proile has been updated')
		return redirect(url_for('.user', username = current_user.username))
	form.name.data = current_user.name
	form.location.data = current_user.location
	return render_template('edit_profile.html')

@main.route('/user_portal')
@login_required
def user_portal():
	return render_template('main/user_portal.html')

@main.route('/tests')
@login_required
def view_tests():
	tests = Test.query.filter_by(is_available=True).all()
	return render_template('main.view_tests.html', tests=tests)

@main.route('/tests/<int:test_id>')
@login_required
def test_details(test_id):
	test = Test.query.get_or_404(test_id)
	return render_template('test_details.html', test=test)

main.route('/order_test/<int:test_id>', methods=['GET', 'POST'])
@login_required
def order_test(test_id):
	test = Test.query.get_or_404(test_id)
	return render_template('order_test.html', test=test)

@main.route('/orders')
@login_required
def view_orders():
	orders = TestOrder.query.filter_by(user_id=current_user.user_id).all()
	return render_template(view_orders.html)

@main.route('/rare_disease_clinic', methods=['GET', 'POST'])
def rare_disease_clinic():
	form = RareDiseaseRegistryForm()
	if form.validate_on_submit():
		pass
	return render_template('main/rare_disease_clinic.html', form=form)

@main.route('/about')
def about():
    """About page"""
    return render_template('main/about.html')

@main.route('/contact')
def contact():
    """Contact page"""
    return render_template('main/contact.html')

@main.route('/precision_diabetes')
def precision_diabetes():
    return render_template('main/precision_diabetes.html')

@main.route('/precision_cardiology')
def precision_cardiology():
    return render_template('main/precision_cardiology.html')

@main.route('/precision_oncology')
def precision_oncology():
    return render_template('main/precision_oncology.html')

@main.route('/order_prescriptions')
def order_prescriptions():
	return render_template('main/order_prescriptions.html')


@main.route('/articles', methods=['GET'])
def list_articles():
    articles = Article.query.all()
    return render_template('main/list_articles.html', articles=articles)

@main.route('/articles', methods=['GET'])
def learn_more():
    articles = Article.query.all()
    return render_template('main/list_articles.html', articles=articles)

@main.route('/articles/<int:article_id>', methods=['GET'])
def view_article(article_id):
    article = Article.query.get_or_404(article_id)
    return send_from_directory(directory=os.path.dirname(article.pdf_path), filename=os.path.basename(article.pdf_path))

@main.route('/admin/upload_article', methods=['GET', 'POST'])
@login_required
def upload_article():
    form = ArticleUploadForm()
    if form.validate_on_submit():
        clinic = Clinic.query.filter_by(name=form.clinic.data).first()
        if not clinic:
            clinic = Clinic(name=form.clinic.data)
            db.session.add(clinic)
            db.session.commit()
        
        pdf_file = form.pdf_file.data
        filename = secure_filename(pdf_file.filename)
        pdf_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        pdf_file.save(pdf_path)
        
        article = Article(title=form.title.data, clinic=clinic, pdf_path=pdf_path)
        db.session.add(article)
        db.session.commit()
        flash('Article uploaded successfully.')
        return redirect(url_for('main.list_articles'))
    return render_template('admin/upload_article.html', form=form)

@main.route('/share_story', methods=['GET', 'POST'])
def share_story():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        story = request.form.get('story')
        # Implement the logic to handle the submitted story, e.g., save to the database
        flash('Thank you for sharing your story!')
        return redirect(url_for('main.share_story'))
    return render_template('main/share_story.html')


# Routes for access permission and payment

@socketio.on('connect')
def handle_connect():
	pass

@socketio.on('disconnect')
def handle_disconnect():
	pass
	print('Client disconnected')

@socketio.on('message')
def handle_message(data):
	print('Recieved message:', data)
	socketio.emit('message', data)