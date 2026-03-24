from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from .service import authenticate
from .decorators import login_required
from app.models import *

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = authenticate(email, password)

        if user:
            session['user_id'] = user.id
            session['role'] = user.role

            flash("Connexion réussie")
            return redirect('/')
        else:
            flash("Identifiants incorrects")

    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("Déconnecté")
    return redirect('/auth/login')

@auth_bp.route('/profile')
@login_required
def profile():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    if not user:
        session.clear()
        return redirect(url_for('auth.login'))
    
    teacher_profile = None
    student_profile = None
    
    if user.role == 'teacher':
        teacher_profile = Teacher.query.get(user.id)
    elif user.role == 'student':
        student_profile = Student.query.get(user.id)
    elif user.role == 'admin':
        pass
        
    return render_template(
        'auth/profile.html', 
        user=user, 
        teacher=teacher_profile, 
        student=student_profile
    )