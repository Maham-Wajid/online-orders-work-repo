from flask import Blueprint, redirect, render_template, request, session, url_for, flash
from datetime import datetime
import sqlite3
from password_hashing import Hash

main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
def home():
    try:
        connection = sqlite3.connect('forum_db.sqlite')
        cursor = connection.cursor()
        query = f"""
                SELECT 
                topic.topicID, user.userName, topic.topicName, topic.creationTime 
                FROM user 
                INNER JOIN topic 
                ON user.userID=topic.postingUser
                ORDER by topic.topicID DESC;
        """
        cursor.execute(query)
        topic_data = cursor.fetchall()
        like_data = list()
        if 'user' in session:
            query = f"""
                    SELECT topic
                    FROM Like 
                    WHERE user_id = {session['user'][0][0]};
            """
            cursor.execute(query)
            likes = cursor.fetchall()
            for like in likes:
                like_data.append(like[0])
        cursor.close()
        connection.close()
    except Exception as error:
        print(error)

    return render_template('index.html', topic_data=topic_data, like_data=like_data)


@main.route('/signup', methods=['GET', 'POST'])
def signup():
    try:
        connection = sqlite3.connect('forum_db.sqlite')
        cursor = connection.cursor()
        if request.method == 'POST':
            username = request.values.get('username')
            password = Hash.hash_password(request.values.get('password'))
            created_at = datetime.now().date()
            query = f"""
                    select * from user 
                    where userName = "{username}"
                    """
            cursor.execute(query)
            user = cursor.fetchall()
            if not user:
                query = f"""
                        insert into 
                        user (userName, passwordHash, creationTime)
                        values("{username}", "{password}", "{created_at}");
                        """
                cursor.execute(query)
                connection.commit()
                cursor.close()
                connection.close()
                flash('User Added succesfully', 'info')
            else:
                flash('User Already Exists', 'error')
                cursor.close()
    except Exception as error:
        print(error)
        flash('Something went wrong please try again later', 'error')

    return redirect(url_for('main.home'))


@main.route('/signin', methods=['GET', 'POST'])
def signin():
    try:
        connection = sqlite3.connect('forum_db.sqlite')
        cursor = connection.cursor()
        if request.method == 'POST':
            username = request.values.get('username')
            password = request.values.get('password')
            query = f"""
                    select * from user 
                    where userName = "{username}"
                    """
            cursor.execute(query)
            user = cursor.fetchall()
            if user and Hash.verify_password(user[0][2], password):
                session['user'] = user

            else:
                flash('Username or password is incorrect', 'error')
    except Exception as error:
        print(error)
        flash('Something went wrong please try again later', 'error')

    return redirect(url_for('main.home'))


@main.route('/logout')
def logout():
    try:
        session.pop('user', None)
    except Exception as error:
        print(error)
    return redirect(url_for('main.home'))


@main.route('/create_topic', methods=['GET', 'POST'])
def create_topic():
    try:
        if request.method == 'POST':
            topic_name = request.form.get('topicName')
            user_id = session['user'][0][0]
            connection = sqlite3.connect('forum_db.sqlite')
            cursor = connection.cursor()
            current_date = datetime.now().date()
            query = f"""
                    insert into 
                    topic (topicName, postingUser, creationTime, updateTime) 
                    values("{topic_name}", {user_id}, "{current_date}", "{current_date}");
                    """
            cursor.execute(query)
            connection.commit()
            cursor.close()
            connection.close()
    except Exception as error:
        print(error)
    return redirect(url_for('main.home'))


@main.route('/claims/<int:topic_id>')
def claims(topic_id=None):
    try:
        connection = sqlite3.connect('forum_db.sqlite')
        cursor = connection.cursor()
        query = f"""
                SELECT 
                claim.claimID , claim.topic, claim.postingUser, claim.text, claim.creationTime, claim.updateTime, user.userName, topic.topicName 
                FROM claim 
                INNER JOIN 
                user ON user.userID=claim.postingUser 
                inner join 
                topic on topic.topicID=claim.topic 
                where topic.topicID = {topic_id}
                ORDER BY claim.claimID DESC;
                """
        cursor.execute(query)
        claims = cursor.fetchall()
        query = f"""
                SELECT * from topic where topicID = {topic_id};
                """
        cursor.execute(query)
        topic = cursor.fetchall()
        cursor.close()
        connection.close()
    except Exception as error:
        print(error)
    return render_template('claim.html', claims=claims, topic=topic)


@main.route('/create_claim/<int:topic_id>', methods=['POST'])
def create_claim(topic_id):
    try:
        if request.method == 'POST':
            claim_text = request.form.get('claim_text')
            user_id = session['user'][0][0]
            connection = sqlite3.connect('forum_db.sqlite')
            cursor = connection.cursor()
            current_date = datetime.now().date()
            query = f"""
                    insert into 
                    claim (topic, postingUser, text, creationTime, updateTime) 
                    values({topic_id}, {user_id}, "{claim_text}", "{current_date}", "{current_date}");
                    """
            cursor.execute(query)
            connection.commit()
            cursor.close()
            connection.close()
    except Exception as error:
        print(error)
        flash('Something went wrong')
        return redirect(url_for('main.home'))
    return redirect(url_for('main.claims', topic_id=topic_id))

@main.route('/add_like', methods=['POST'])
def add_like():
    try:
        if 'user' in session:
            topic_id = request.form.get('topic_id')
            user_id = session['user'][0][0]
            query = f"""
                INSERT INTO 
                Like (user_id,topic) 
                VALUES ({user_id},{topic_id});
            """
            connection = sqlite3.connect('forum_db.sqlite')
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            cursor.close()
            connection.close()
            return str(1)
        else:
            return str(0)
    except Exception as error:
        print(error)
        return str(0)


@main.route('/remove_like', methods=['POST'])
def remove_like():
    try:
        if 'user' in session:
            topic_id = request.form.get('topic_id')
            user_id = session['user'][0][0]
            query = f"""
                DELETE FROM 
                Like WHERE 
                user_id = {user_id} and topic = {topic_id};
            """
            connection = sqlite3.connect('forum_db.sqlite')
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            cursor.close()
            connection.close()
            return str(1)
        else:
            return str(0)
    except Exception as error:
        print(error)
        return str(0)
