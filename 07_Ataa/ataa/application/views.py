"""
Main Application Views
"""
import os
from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required, login_user, logout_user
from . import sessiondb, login_manager, secrets
from .models import Budget, DonationPost, User
from datetime import datetime
from werkzeug.utils import secure_filename


main = Blueprint('main', __name__)


@main.route('/home')
@main.route('/')
def index():
    try:
        projects = sessiondb.query(DonationPost).filter(
            DonationPost.category == 1).all()
        individual = sessiondb.query(DonationPost).filter(
            DonationPost.category == 2).all()
        organisational = sessiondb.query(DonationPost).filter(
            DonationPost.category == 3).all()
    except Exception as error:
        print("############################ ERROR ############################")
        print(error)
        print("###############################################################")
    return render_template('index.html', projects=projects, individual=individual, organisational=organisational, images_path=secrets['UPLOAD_FOLDER'])


@main.route('/signup', methods=['POST', 'GET'])
def signup():
    try:
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            user = sessiondb.query(User).filter(
                User.email == email).first()
            if not user:
                current_time = str(datetime.now()).split('.')[0]
                user = User(name=name,
                            email=email, password=password, balance=0, created_at=current_time, updated_at=current_time)
                sessiondb.add(user)
                sessiondb.commit()
                login_user(user=user)
                flash(message='Signup Successful!', category='success')
            else:
                flash(message='User Already Exists!', category='error')
            return redirect(url_for('main.index'))
        if request.method == 'GET':
            return render_template('signup.html')
    except Exception as error:
        print("############################ ERROR ############################")
        print(error)
        print("###############################################################")
        return redirect(url_for('main.index'))


@main.route('/login', methods=['POST', 'GET'])
def login():
    try:
        if request.method == 'GET':
            return render_template('/login.html')
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            user = sessiondb.query(User).filter(
                User.email == email).first()
            if user and password == user.password:
                login_user(user=user)
            else:
                flash(
                    message='Please check your email/password and try again.', category='error')
                return redirect('/login')
    except Exception as error:
        print("############################ ERROR ############################")
        print(error)
        print("###############################################################")
    return redirect(url_for('main.index'))


@main.route('/request_donation', methods=['POST', 'GET'])
def publish_donation():
    try:
        if request.method == 'GET':
            return render_template('/request_donation.html')
        if request.method == 'POST' and current_user.is_authenticated:
            title = request.form.get('title')
            category = request.form.get('category')
            requested_amount = request.form.get('requested_amount')
            description = request.form.get('description')
            file = request.files['donation_image']
            path = os.path.join(
                secrets['UPLOAD_FOLDER'], secure_filename(file.filename))
            file.save(path)
            current_time = str(datetime.now()).split('.')[0]
            
            # add some initial amount from budget if there is
            budget = sessiondb.query(Budget).first()
            collected_amount = 0
            if budget:
                if budget.amount > 200:
                    collected_amount = 200
                    budget.amount -= 200
                else:
                    collected_amount = budget.amount
                    budget.amount = 0
            sessiondb.commit()
            donation_post = DonationPost(user_id=current_user.id, title=title, requested_amount=requested_amount, collected_amount=collected_amount,
                                         category=category, image_path=file.filename, description=description, created_at=current_time, updated_at=current_time)
            sessiondb.add(donation_post)
            sessiondb.commit()
        else:
            flash(message='Please Login to proceed!', category='error')
    except Exception as error:
        print("############################ ERROR ############################")
        print(error)
        print("###############################################################")
    return redirect(url_for('main.index'))


@main.route('/donation_post/<int:pk>')
def donation_post(pk):
    try:
        project = sessiondb.query(DonationPost).filter(
            DonationPost.id == pk).first()
        return render_template('donation_post.html', project=project)
    except Exception as error:
        print("############################ ERROR ############################")
        print(error)
        print("###############################################################")

    return redirect(url_for('main.index'))


@main.route('/donate/<int:pk>', methods=['GET', 'POST'])
def donate(pk):
    try:
        if request.method == 'POST' and current_user.is_authenticated:
            amount = float(request.form.get('amount')
                           if request.form.get('amount') else 0)
            if amount > 0 and current_user.balance >= amount:
                project = sessiondb.query(DonationPost).filter(
                    DonationPost.id == pk).first()
                project.collected_amount += amount
                sessiondb.commit()
                user = sessiondb.query(User).filter(User.id == current_user.id).first()
                user.balance -= amount
                sessiondb.commit()
                flash(message='Amount Donated Successfully!', category='success')
            else:
                flash(message='You do not have sufficient balance!', category='error')
        else:
            flash(message='Please login to proceed!', category='error')
    except Exception as error:
        print("############################ ERROR ############################")
        print(error)
        print("###############################################################")
        flash(message='Something went wrong.', category='error')

    return redirect(url_for('main.index'))


@main.route('/general_donation', methods=['POST'])
def general_donation():
    try:
        if request.method == 'POST' and current_user.is_authenticated:
            amount = float(request.form.get('amount')
                           if request.form.get('amount') else 0)
            if amount > 0 and current_user.balance >= amount:
                general = sessiondb.query(Budget).first()
                current_time = str(datetime.now()).split('.')[0]
                if general:
                    general.amount += amount
                    general.updated_at = current_time
                else:
                    general = Budget(
                        amount=amount, created_at=current_time, updated_at=current_time)
                    sessiondb.add(general)
                sessiondb.commit()
                user = sessiondb.query(User).filter(User.id == current_user.id).first()
                user.balance -= amount
                sessiondb.commit()
                flash(message='Amount Donated Successfully!', category='success')
            else:
                flash(message='Please Enter Valid Amount!', category='error')
        else:
            flash(message='Please Login to proceed!', category='error')
    except Exception as error:
        print("############################ ERROR ############################")
        print(error)
        print("###############################################################")
        flash(message='Something went wrong.', category='error')

    return redirect(url_for('main.index'))


# @main.route('/help')
# def help():
#     return render_template('help_section.html')


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        user_id = sessiondb.query(User).get(user_id)
        sessiondb.close()
        return user_id
    return None
