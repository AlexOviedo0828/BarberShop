from flask import render_template, session, redirect
from flask_app import app

# ruta admin


@app.route('/dashboard/admin')
def dashboard_admin():
    if 'usuario_id' not in session:
        return redirect('/login')
    if session.get('rol') != 'admin':
        return redirect('/dashboard/usuario')
    return render_template('admin.html')
