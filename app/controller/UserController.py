from flask import request, render_template, redirect, url_for, session, flash
from app.model.user import User
from app import db

def login():
    """Handle login user dengan autentikasi database"""
    if request.method == 'GET':
        # Jika sudah login, redirect ke home
        if 'user' in session:
            return redirect(url_for('inventory_index'))
        return render_template('user/login.html')

    try:
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        # Validasi
        if not username or not password:
            flash('Username dan password wajib diisi!', 'warning')
            return render_template('user/login.html')

        # Cari user di database
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password) and user.is_active:
            session['user'] = username
            session['user_id'] = user.id
            session['user_role'] = user.role
            flash(f'Selamat datang, {username}!', 'success')
            return redirect(url_for('inventory_index'))
        else:
            flash('Username atau password salah, atau akun tidak aktif!', 'danger')
            return render_template('user/login.html')
    except Exception as e:
        flash(f'Terjadi kesalahan saat login: {str(e)}', 'danger')
        return render_template('user/login.html')

def logout():
    """Handle logout user"""
    session.clear()
    flash('Anda telah logout!', 'info')
    return redirect(url_for('login'))

def register():
    """Handle registrasi user (hanya untuk admin)"""
    if request.method == 'GET':
        # Cek apakah user adalah admin
        if 'user_role' not in session or session.get('user_role') != 'admin':
            flash('Anda tidak memiliki akses!', 'danger')
            return redirect(url_for('inventory_index'))
        return render_template('user/register.html')
    
    try:
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        email = request.form.get('email', '').strip()
        role = request.form.get('role', 'staff')
        
        # Validasi
        if not username or not password:
            flash('Username dan password wajib diisi!', 'warning')
            return render_template('user/register.html')
        
        # Cek apakah username sudah ada
        existing = User.query.filter_by(username=username).first()
        if existing:
            flash('Username sudah digunakan!', 'warning')
            return render_template('user/register.html')
        
        # Buat user baru
        new_user = User(username=username, email=email, role=role)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash(f'User "{username}" berhasil didaftarkan!', 'success')
        return redirect(url_for('user_list'))
    except Exception as e:
        db.session.rollback()
        flash(f'Gagal mendaftarkan user: {str(e)}', 'danger')
        return render_template('user/register.html')

def user_list():
    """Tampilkan semua user (hanya admin)"""
    try:
        # Cek apakah user adalah admin
        if 'user_role' not in session or session.get('user_role') != 'admin':
            flash('Anda tidak memiliki akses!', 'danger')
            return redirect(url_for('inventory_index'))
        
        users = User.query.order_by(User.username).all()
        return render_template('user/index.html', data=users)
    except Exception as e:
        flash(f'Terjadi kesalahan: {str(e)}', 'danger')
        return render_template('user/index.html', data=[])