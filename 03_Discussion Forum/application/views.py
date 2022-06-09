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
    except Exception as error:
        print(error)

    return render_template('index.html', topic_data=topic_data)


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


@main.route('/claim_replies/<int:claim_id>')
def claim_replies(claim_id=None):
    try:
        connection = sqlite3.connect('forum_db.sqlite')
        cursor = connection.cursor()
        query = f"""select *
                    from
                        claim as a
                             join
                        replyToClaim as b
                            on a.claimID = b.claim
                             join 
                        replyText as c
                            on b.reply = c.replyTextID
                             join
                        user as d
                            on d.userID = c.postingUser
                    where a.claimID = {claim_id}
                    ORDER by c.replyTextID DESC;
                """
        cursor.execute(query)
        replies = cursor.fetchall()
        query = f"""
                SELECT * from claim 
                where claimID = {claim_id};
                """
        cursor.execute(query)
        claim = cursor.fetchall()
        cursor.close()
        connection.close()
    except Exception as error:
        print(error)
        flash('Something went wrong')
        return redirect(url_for('main.home'))
    return render_template('claim_reply.html', replies=replies, claim=claim)


@main.route('/create_reply_to_claim/<int:claim_id>', methods=['POST'])
def create_reply_to_claim(claim_id):
    try:
        connection = sqlite3.connect('forum_db.sqlite')
        cursor = connection.cursor()
        reply_text = request.form.get('reply_text')
        reply_relation = request.form.get('reply_relation')
        user_id = session['user'][0][0]
        current_date = datetime.now().date()
        query = f"""
                insert into 
                replyText (postingUser, text, creationTime) 
                values({user_id}, "{reply_text}", "{current_date}");
                """
        cursor.execute(query)
        connection.commit()
        query = f"""
                SELECT * FROM replyText 
                order by replyTextID DESC;
                """
        cursor.execute(query)
        reply_text = cursor.fetchall()
        query = f"""
                insert into 
                replyToClaim (reply, claim, replyToClaimRelType) 
                values({reply_text[0][0]}, {claim_id}, {int(reply_relation)});                
                """
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as error:
        print(error)
        flash('Something went wrong')
        return redirect(url_for('main.home'))
    return redirect(url_for('main.claim_replies', claim_id=claim_id))


@main.route('/reply_to_reply/<int:reply_text_id>')
def reply_to_reply(reply_text_id=None):
    try:
        connection = sqlite3.connect('forum_db.sqlite')
        cursor = connection.cursor()
        query = f"""select *
                    from
                        replyText as a
                             join
                        replyToReply as b
                            on a.replyTextID= b.parent

                             join 
                        replyText as c
                            on b.reply = c.replyTextID
                             join
                        user as d
                            on d.userID = c.postingUser
                    where a.replyTextID = {reply_text_id}
                    ORDER by b.replyToReplyID DESC;
                """
        cursor.execute(query)
        replies = cursor.fetchall()
        query = f"""
                SELECT * from replyText 
                where replyTextID = {reply_text_id};
                """
        cursor.execute(query)
        reply_to_claim = cursor.fetchall()
        cursor.close()
        connection.close()
    except Exception as error:
        print(error)
        flash('Something went wrong')
        return redirect(url_for('main.home'))
    return render_template('claim_reply_to_reply.html', replies=replies, reply_to_claim=reply_to_claim)


@main.route('/create_reply_to_reply/<int:reply_id>', methods=['POST'])
def create_reply_to_reply(reply_id):
    try:
        connection = sqlite3.connect('forum_db.sqlite')
        cursor = connection.cursor()
        reply_text = request.form.get('reply_text')
        reply_relation = request.form.get('reply_relation')
        user_id = session['user'][0][0]
        current_date = datetime.now().date()
        query = f"""
                insert into
                replyText (postingUser, text, creationTime) 
                values({user_id}, "{reply_text}", "{current_date}");
                """
        cursor.execute(query)
        connection.commit()
        query = f"""
                SELECT * FROM replyText 
                order by replyTextID DESC;
                """
        cursor.execute(query)
        reply_text = cursor.fetchall()
        query = f"""
                insert into 
                replyToReply (reply, parent, replyToReplyRelType) 
                values({reply_text[0][0]}, {reply_id}, {int(reply_relation)});
                """
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as error:
        print(error)
        flash('Something went wrong')
        return redirect(url_for('main.home'))
    return redirect(url_for('main.reply_to_reply', reply_text_id=reply_id))
