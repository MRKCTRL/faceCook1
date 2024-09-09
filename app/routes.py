from flask import Blueprint, render_template, redirect, url_for, request, flash 
from flask_login import login_user, logout_user, login_required, current_user 
from .models import User, DiaryEntry 
from . import db 
from werkzeug.security import generate_password_hash, check_password_hash

main=Blueprint('main', __name__)

@main.route('/')
def home():
    entries=DiaryEntry.query.filter_by(is_public=True).all()
    return render_template('home.html', entries=entries)


@main.route('/dashboard')
@login_required
def dashboard():
    user_entries=DiaryEntry.query.filter_by(author=current_user).all()
    return render_template('dashboard.html', entries=user_entries)

@main.route('/add', methods=['GET', 'POST'])
@login_required
def add_entry():
    if request.method == 'POST':
        title=request.form.get('content')
        is_public='is_public' in request.form
        
        new_entry=DiaryEntry(title=title, content=content, is_public=is_public. author=current_user)
        db.session.add(new_entry)
        db.session.commit()
        flash('diary entry created!', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('entry_form.html')

@main.route('/register', methods=['POST', 'POST'])
def register():
    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')
        
    
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
        return redirect(url_for('main.dashboard'))
    
        hashed_password=generate_password_hash(password, methods='sha245')
        new_user=User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('registeration successful! please login','success')
        return redirect(url_for(main.login))
    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')

        user=User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for(main.dashboard))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('main.login'))
    return render_template('login.html')

@main.route('logout') 
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))