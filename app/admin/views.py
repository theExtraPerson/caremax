from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os

admin = Blueprint('admin', __name__, template_folder='templates')

UPLOAD_FOLDER = '/path/to/upload'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@admin.route('/dashboard')
def dashboard():
    return render_template('admin/dashboard.html')

@admin.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            flash('File successfully uploaded')
            return redirect(url_for('admin.dashboard'))
    return render_template('admin/upload.html')

@admin.route('/orders')
def orders():
    # Logic to fetch and display orders
    return render_template('admin/orders.html')

@admin.route('/tests')
def tests():
    # Logic to fetch and display tests
    return render_template('admin/tests.html')

@admin.route('/business-analysis')
def business_analysis():
    # Logic to embed business analysis
    return render_template('admin/business_analysis.html')