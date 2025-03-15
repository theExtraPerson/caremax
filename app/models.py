# python file for different models 
# TO DO: Create models for Provider, User, Order, test, Payment, Notification

from flask_login import UserMixin, AnonymousUserMixin
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
from flask import current_app
from datetime import datetime, timezone
from sqlalchemy import  ForeignKey, event
from sqlalchemy.event import listens_for

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Permission:
    FILL_TEST_FORM = 1
    UPLOAD_VCF = 2
    ACCESS_RESULTS = 4
    ORDER_TEST = 8
    ADMIN = 16

class Role (db.Model):
    __tablename__ = 'roles'
    role_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    permissions = db.Column(db.Integer)
    default = db.Column(db.Boolean, default=False, index=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0
        
    
    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.ACCESS_RESULTS, Permission.ORDER_TEST],
            'Clinician': [Permission.FILL_TEST_FORM],
            'Sequencer': [Permission.UPLOAD_VCF],
            'Administrator': [Permission.ADMIN, Permission.UPLOAD_VCF]
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name ==default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm
    
# User
class User (UserMixin, db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'))
    name = db.Column(db.String(64))
    location = db.Column(db.String(64), unique=True, index=True)
    confirmed = db.Column(db.Boolean, default=False)
    test_orders = db.relationship('TestOrder', backref='user', lazy='dynamic')
    
    def get_id(self):
        return str(self.user_id)
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
 
    def generate_confirmation_token(self, expiration=3600):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return s.dumps({'confirm': self.user_id}) 

    def confirm(self, token, expiration=3600):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'), max_age=expiration)
        except Exception:
            return False
        if data.get('confirm') != self.user_id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True
    

# evaluating permissions
    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)
    
    def is_administrator(self):
        return self.can(Permission.ADMIN)
    
    def ping(self):
        self.last_seen = datetime.now(timezone.utc)
        db.session.add(self)

    def __repr__(self):
        return f'<User {self.username}>'

@listens_for(User, 'before_insert')
def assign_role_before_insert(mapper, connection, target):
    if target.role is None:
        if target.email == current_app.config.get('RDC_ADMIN'):
            target.role = Role.query.filter_by(name='Administrator').first()
        else:
            target.role = Role.query.filter_by(default=True).first()
    
class AnonymousUser(AnonymousUserMixin):
    def __init__(self):
        super(AnonymousUser, self).__init__()

    def can(self, permissions):
        return False
    
    def is_administrator(self):
        return False
    
login_manager.anonymous_user = AnonymousUser


class Test (db.Model):
    __tablename__ = 'tests'
    test_id = db.Column(db.Integer, primary_key=True)
    test_name = db.Column(db.String(128), unique=True, index=True)
    test_description = db.Column(db.String(255))
    test_category = db.Column(db.String(255))
    test_subcategory = db.Column(db.String(255))
    test_type = db.Column(db.String(64))
    sample_type = db.Column(db.String(15))
    turn_around_time = db.Column(db.Integer)
    test_price = db.Column(db.Float(), unique=True, index=True)
    is_available = db.Column(db.Boolean)
    test_orders = db.relationship('TestOrder', backref='test', lazy='dynamic')
   
class TestOrder (db.Model):
    __tablename__ = 'test_orders'
    request_id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.test_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    status = db.Column(db.String, default='pending') # include the available options
    tube_size = db.Column(db.Integer)
    location = db.Column(db.String(255), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    
    
class Admin (db.Model):     
    __tablename__ = 'admins'
    admin_id = db.Column(db.Integer, primary_key=True)
    is_authenticated = db.Column(db.Boolean)
    is_available = db.Column(db.Boolean, default=True)

class Payment(db.Model):
    __tablename__ = 'payments'
    payment_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, db.ForeignKey('tests.test_price')) # realted to test amount 
    payment_method = db.Column(db.String(64), default='Cash')
    status = db.Column(db.String(64), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

# app/models.py

class Clinic(db.Model):
    __tablename__ = 'clinics'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    articles = db.relationship('Article', backref='clinic', lazy='dynamic')

class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinics.id'))
    pdf_path = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


    

