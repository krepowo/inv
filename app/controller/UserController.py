from flask import request, render_template, redirect, url_for, session, flash
from app.model.user import User
from app import db

def login():
    """Handle user login with database authentication"""
    if request.method == 'GET':
        # If already logged in, redirect to home
        if 'user' in session:
            return redirect(url_for('inventory_index'))
        return render_template('login.html')

    try:
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        # Validation
        if not username or not password:
            flash('Username dan password wajib diisi!', 'warning')
            return render_template('login.html')

        # Find user in database
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password) and user.is_active:
            session['user'] = username
            session['user_id'] = user.id
            session['user_role'] = user.role
            flash(f'Selamat datang, {username}!', 'success')
            return redirect(url_for('inventory_index'))
        else:
            flash('Username atau password salah, atau akun tidak aktif!', 'danger')
            return render_template('login.html')
    except Exception as e:
        flash(f'Terjadi kesalahan saat login: {str(e)}', 'danger')
        return render_template('login.html')

def logout():
    """Handle user logout"""
    session.clear()
    flash('Anda telah logout!', 'info')
    return redirect(url_for('login'))

def register():
    """Handle user registration (for admin only)"""
    if request.method == 'GET':
        # Check if user is admin
        if 'user_role' not in session or session.get('user_role') != 'admin':
            flash('Anda tidak memiliki akses!', 'danger')
            return redirect(url_for('inventory_index'))
        return render_template('register.html')
    
    try:
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        email = request.form.get('email', '').strip()
        role = request.form.get('role', 'staff')
        
        # Validation
        if not username or not password:
            flash('Username dan password wajib diisi!', 'warning')
            return render_template('register.html')
        
        # Check if username exists
        existing = User.query.filter_by(username=username).first()
        if existing:
            flash('Username sudah digunakan!', 'warning')
            return render_template('register.html')
        
        # Create new user
        new_user = User(username=username, email=email, role=role)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash(f'User "{username}" berhasil didaftarkan!', 'success')
        return redirect(url_for('user_list'))
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal mendaftarkan user: {str(e)}', 'danger')
        return render_template('register.html')

def user_list():
    """Display all users (admin only)"""
    try:
        # Check if user is admin
        if 'user_role' not in session or session.get('user_role') != 'admin':
            flash('Anda tidak memiliki akses!', 'danger')
            return redirect(url_for('inventory_index'))
        
        users = User.query.order_by(User.username).all()
        return render_template('user_list.html', data=users)
    except Exception as e:
        flash(f'Terjadi kesalahan: {str(e)}', 'danger')
        return render_template('user_list.html', data=[])