# src/users.py
# This file holds API routes for user functionality and nav
from . import users_bp
from src.user_utils import *
from werkzeug.security import generate_password_hash
from flask import render_template, request, flash, redirect, session


@users_bp.get('/users/signup')
def user_signup():
    if 'user_id' in session:
        flash('You are already logged in.')
        return redirect('/')
    return render_template('signup.html')


@users_bp.post('/users/signup')
def signup_user():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')


    result = create_user(username, email, hashed_password)
    if result == 'Success':
        flash('Account successfully created')
        return redirect('/')
    else:
        flash(result) 
        return redirect('/users/signup')


@users_bp.get('/users/login')
def login_form():
    if 'user_id' in session:
        flash('You are already logged in.')
        return redirect('/')
    return render_template('login.html')


@users_bp.post('/users/login')
def login_user():
    email = request.form['email']
    password = request.form['password']
    user = check_user_credentials(email, password)
    if user:
        session['user_id'] = user.user_id
        session['username'] = user.username
        return redirect('/')
    else:
        flash('Invalid email or password')
        return redirect('/')


@users_bp.get('/users/profile')
def profile():
    if not 'user_id' in session:
        flash('Please log in to access your profile.')
        return redirect('/')
    user_id = session['user_id']
    user = get_user_by_id(user_id)
    return render_template('profile.html', user=user)


@users_bp.get('/users/profile/edit')
def edit_profile_form():
    if not 'user_id' in session:
        flash('Please log in to edit your profile.')
        return redirect('/')
    user_id = session['user_id']
    user = get_user_by_id(user_id)
    return render_template('edit_profile.html', user=user)


@users_bp.post('/users/profile/edit')
def edit_profile():
    if 'user_id' not in session:
        flash('Please log in to edit your profile')
        return redirect('/')
    user_id = session['user_id']
    username = request.form['username']
    email = request.form['email']

    result = update_user_profile(user_id, username, email)
    if result == 'Success':
        session['username'] = username
        flash('Profile updated successfully')
        return redirect('/users/profile')
    else:
        flash(result)  
        return redirect('/users/profile/edit')


@users_bp.get('/users/logout')
def logout():
    if 'user_id' not in session:
        flash('You are not logged in.')
        return redirect('/')
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been successfully logged out.')
    return redirect('/')


@users_bp.post('/users/delete')
def delete_user():
    if 'user_id' not in session:
        flash('Please log in to delete your account.')
        return redirect('/')
    user_id = session['user_id']
    if delete_user_account(user_id):
        session.clear()
        flash('Your account has been successfully deleted.')
    else:
        flash('User could not be found')
    return redirect('/')