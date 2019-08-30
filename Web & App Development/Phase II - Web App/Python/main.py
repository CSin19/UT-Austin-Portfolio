import os
import time

from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
from jinja2 import Template
from werkzeug import useragents
import json
import ast
import pymysql
import pymysql.cursors

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

app = Flask(__name__)
app.secret_key = "secret99"

# Calculate 1 hour time slots between start time and end time
def CalculateTimeslots(startTime, endTime):
    import datetime
    # Convert user input into date format
    startTime = str(startTime)
    endTime = str(endTime)
    start = datetime.datetime.strptime(startTime,'%H%M')
    end = datetime.datetime.strptime(endTime, '%H%M')
    slots = []
    # Create variable to perform date operations i.e. calculate next time after one hour
    one_hour = datetime.timedelta(minutes=60)
    # Create list of starting times of all time slots
    while start < end and end >= start + one_hour:
            slots.append(start.strftime("%H%M"))
            start += one_hour
    return slots

#Route for handling the index page logic
@app.route('/')
def main():
    return render_template('index.html')

#Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name, cursorclass=pymysql.cursors.DictCursor)
    else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        host = '127.0.0.1'
        cnx = pymysql.connect(user='livestrong19', password='livestrong19',
                              host='127.0.0.1', db='PickupSport', cursorclass=pymysql.cursors.DictCursor)
    with cnx.cursor() as cursor:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            cursor.execute("SELECT * FROM Users WHERE uname = %s AND admin = 'False'", (username,))
            result= cursor.fetchone()
            cnx.close()
            if request.user_agent.platform == 'android':
                if not result:
                    return jsonify({'message': "User does not exist. Please sign up."})
                elif result['uPassword'] != password:
                    return jsonify({'message': 'Password is incorrect'})
                else:
                    session['muser_id'] = result['uId']
                    return jsonify({'message': 'Success', 'user_id': session['muser_id']})
            else:
                if not result:
                    error = 'Invalid Username. Please try again.'
                elif result['uPassword'] != password:
                    error = 'Invalid Password. Please try again.'
                else:
                    session['nuser_id'] = result['uId']
                    uid = session['nuser_id']
                    return redirect(url_for('home',uid=uid))

    return render_template('login.html', error=error)

# Route for handling the register page logic
@app.route('/createAccount', methods=['GET', 'POST'])
def createAccount():
    error = None
    if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name, cursorclass=pymysql.cursors.DictCursor)
    else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        host = '127.0.0.1'
        cnx = pymysql.connect(user='livestrong19', password='livestrong19',
                              host='127.0.0.1', db='PickupSport', cursorclass=pymysql.cursors.DictCursor)
    with cnx.cursor() as cursor:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            phone = request.form['phone']
            email = request.form['email']
            zipcode = request.form['zipcode']
            admin = "False"
            if request.user_agent.platform == 'android':
                        cursor.execute("INSERT INTO Users(uname, uphone, uemail, upassword, uZipcode, admin) \
                        VALUES(%s, %s, %s, %s, %s, %s)", (username, phone, email, password, zipcode, admin))
                        cnx.commit()
                        cursor.execute("SELECT * FROM Users WHERE uname = %s", (username,))
                        result = cursor.fetchone()
                        uid = result['uId']
                        cnx.close()
                        session['muser_id'] = result['uId']
                        return jsonify({'message': 'User created', 'user_id': session['muser_id']})
            else:
                    if username == '' or password == '' or phone == '' or email == '' or zipcode == '':
                        error = 'Invalid Credentials. Please try again.'
                    else:
                        cursor.execute("INSERT INTO Users(uname, uphone, uemail, upassword, uZipcode, admin) \
                        VALUES(%s, %s, %s, %s, %s, %s)", (username, phone, email, password, zipcode, admin))
                        cnx.commit()
                        cursor.execute("SELECT * FROM Users WHERE uname = %s", (username,))
                        result = cursor.fetchone()
                        uid = result['uId']
                        cnx.close()
                        session['nuser_id'] = result['uId']
                        uid = session['nuser_id']
                        return redirect(url_for('home'), uid =uid)

    return render_template('createAccount.html', error=error)


# Route for handling the home page logic
@app.route('/home/<uid>')
def home(uid):
    if request.user_agent.platform == 'android':
        return jsonify({'message': 'Success'})
    else:
        if 'nuser_id' in session:
            return render_template('home.html', uid=uid)
        else:
            return redirect(url_for('main'))

@app.route('/logout')
def logout():
    if request.user_agent.platform == 'android':
        return jsonify({'message': 'User logged out'})
    else:
        if 'nuser_id' in session:
            session.pop('nuser_id', None)
            return render_template('login.html')
        else:
            return redirect(url_for('main'))


@app.route('/joinEvents/<uid>', methods=['GET', 'POST'])
def joinEvents(uid):
    error = None
    if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name, cursorclass=pymysql.cursors.DictCursor)
    else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        host = '127.0.0.1'
        cnx = pymysql.connect(user='livestrong19', password='livestrong19',
                              host='127.0.0.1', db='PickupSport', cursorclass=pymysql.cursors.DictCursor)
    with cnx.cursor() as cursor:
        if request.user_agent.platform == 'android':
            cursor.execute("SELECT * FROM Events WHERE EventSpotsLeft > 0 AND EventId NOT IN (SELECT EventId FROM User_Events WHERE uId= %s)", (uid,))
            eresult = cursor.fetchall()
            cnx.close()
            return jsonify(eresult)
        else:
            if 'nuser_id' in session:
                cursor.execute("SELECT * FROM Events WHERE EventSpotsLeft > 0 AND EventId NOT IN (SELECT EventId FROM User_Events WHERE uId= %s)", (uid,))
                eresult = cursor.fetchall()
                cnx.close()
                return render_template('joinEvents.html', eresult=eresult, uid=uid, error=error)
            else:
                return redirect(url_for('main'))

@app.route('/joinEventsResult/<eresult>/<uid>', methods=['GET', 'POST'])
def joinEventsResult(eresult,uid):
    error = None
    if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name, cursorclass=pymysql.cursors.DictCursor)
    else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        host = '127.0.0.1'
        cnx = pymysql.connect(user='livestrong19', password='livestrong19',
                              host='127.0.0.1', db='PickupSport', cursorclass=pymysql.cursors.DictCursor)
    with cnx.cursor() as cursor:
        if request.user_agent.platform == 'android':
            event = ast.literal_eval(eresult)
            spots = event['EventSpotsLeft']
            eid = event['EventId']
            cursor.execute('''INSERT INTO User_Events(EventId, uId) VALUES(%s, %s)''', (eid, uid))
            cursor.execute('''UPDATE Events SET EventSpotsLeft = %s WHERE EventId = %s''', ((spots - 1), eid))
            cnx.commit()
            cnx.close()
            return jsonify({'message':'Success','eid': eid})
        else:
            if 'nuser_id' in session:
                event = ast.literal_eval(eresult)
                spots = event['EventSpotsLeft']
                eid = event['EventId']
                cursor.execute('''INSERT INTO User_Events(EventId, uId) VALUES(%s, %s)''', (eid, uid))
                cursor.execute('''UPDATE Events SET EventSpotsLeft = %s WHERE EventId = %s''', ((spots - 1), eid))
                cnx.commit()
                cnx.close()
                text = "Congratulations! You have joined the Event!"
                return render_template('joinEventsResult.html', text=text, uid=uid, error=error)
            else:
                return redirect(url_for('main'))

@app.route('/joinEventsResultMobile/<uid>', methods=['GET', 'POST'])
def joinEventsResultMobile(uid):
    error = None
    if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name, cursorclass=pymysql.cursors.DictCursor)
    else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        host = '127.0.0.1'
        cnx = pymysql.connect(user='livestrong19', password='livestrong19',
                              host='127.0.0.1', db='PickupSport', cursorclass=pymysql.cursors.DictCursor)
    with cnx.cursor() as cursor:
        if request.user_agent.platform == 'android':
            eid = 12
            spots = 9
            cursor.execute('''INSERT INTO User_Events(EventId, uId) VALUES(%s, %s)''', (eid, uid))
            cursor.execute('''UPDATE Events SET EventSpotsLeft = %s WHERE EventId = %s''', ((spots - 1), eid))
            cnx.commit()
            cnx.close()
            return jsonify({'message':'Success','eid': eid})
        else:
            eid = 12
            spots = 8
            cursor.execute('''INSERT INTO User_Events(EventId, uId) VALUES(%s, %s)''', (eid, uid))
            cursor.execute('''UPDATE Events SET EventSpotsLeft = %s WHERE EventId = %s''', ((spots - 1), eid))
            cnx.commit()
            cnx.close()
            return jsonify({'message':'Success','eid': eid})
        return render_template('joinEventsResult.html', eid=eid)

# Route for handling the search events page logic
@app.route('/searchEvents/<uid>', methods=['GET', 'POST'])
def searchEvents(uid):
    error = None
    if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name, cursorclass=pymysql.cursors.DictCursor)
    else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        host = '127.0.0.1'
        cnx = pymysql.connect(user='livestrong19', password='livestrong19',
                              host='127.0.0.1', db='PickupSport', cursorclass=pymysql.cursors.DictCursor)
    with cnx.cursor() as cursor:
        if request.user_agent.platform == 'android':
            if request.method == 'POST':
                vname = request.form['name']
                date = request.form['date']
                startTime = request.form['start']
                endTime = request.form['end']
                if vname == '' or date == '' or startTime == '' or endTime == '':
                    error = 'Invalid Credentials. Please try again.'
                else:
                    cursor.execute("SELECT * FROM Venues WHERE VenueName = %s", (vname,))
                    vresult = cursor.fetchone()
                    vid = vresult['VenueId']
                    # get all events
                    cursor.execute("SELECT * FROM Events WHERE VenueId = %s AND EventDate = %s", (vid, date))
                    allEvents = cursor.fetchall()
                    matchList = []
                    for x in allEvents:
                        start = str(x['EventStartTime'])
                        end = str(x['EventEndTime'])
                        timeslot = CalculateTimeslots(start, end)
                        matchList.append((x['EventId'], timeslot))
                    givenTimeslot = CalculateTimeslots(startTime, endTime)
                    mactchEventId = []
                    for x in range(len(matchList)):
                        for time in matchList[x][1]:
                            for items in givenTimeslot:
                                if time in items:
                                    mactchEventId.append(matchList[x][0])
                        # return the id of events at a venue given date/time
                    mactchEventId = list(dict.fromkeys(mactchEventId))
                    cnx.close()
                    return jsonify({mactchEventId})
        else:
            if 'nuser_id' in session:
                    if request.method == 'POST':
                        vname = request.form['name']
                        date = request.form['date']
                        startTime = request.form['start']
                        endTime = request.form['end']
                        if vname == '' or date == '' or startTime == '' or endTime == '':
                            error = 'Invalid Credentials. Please try again.'
                        else:
                            cursor.execute("SELECT * FROM Venues WHERE VenueName = %s", (vname,))
                            vresult = cursor.fetchone()
                            vid = vresult['VenueId']
                            # get all events
                            cursor.execute("SELECT * FROM Events WHERE VenueId = %s AND EventDate = %s", (vid, date))
                            allEvents = cursor.fetchall()
                            matchList = []
                            for x in allEvents:
                                start = str(x['EventStartTime'])
                                end = str(x['EventEndTime'])
                                timeslot = CalculateTimeslots(start, end)
                                matchList.append((x['EventId'], timeslot))
                            givenTimeslot = CalculateTimeslots(startTime, endTime)
                            mactchEventId = []
                            for x in range(len(matchList)):
                                for time in matchList[x][1]:
                                    for items in givenTimeslot:
                                        if time in items:
                                            mactchEventId.append(matchList[x][0])
                                # return the id of events at a venue given date/time
                            mactchEventId = list(dict.fromkeys(mactchEventId))
                            cnx.close()
                            return redirect(url_for('searchEventsResults', mactchEventId=mactchEventId, uid=uid))
                    else:
                        return render_template('searchEvents.html', uid=uid, error=error)
            else:
                return redirect(url_for('main'))

# Route for handling the search results page logic
@app.route('/searchEventsResults/<mactchEventId>/<uid>', methods=['GET', 'POST'])
def searchEventsResults(mactchEventId,uid):
    error = None
    if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name, cursorclass=pymysql.cursors.DictCursor)
    else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        host = '127.0.0.1'
        cnx = pymysql.connect(user='livestrong19', password='livestrong19',
                              host='127.0.0.1', db='PickupSport', cursorclass=pymysql.cursors.DictCursor)
    with cnx.cursor() as cursor:
        if request.user_agent.platform == 'android':
            eventId = ast.literal_eval(mactchEventId)
            cursor.execute("SELECT * FROM Events WHERE EventId IN %s", (eventId,))
            eresult = cursor.fetchall()
            cnx.close()
            return jsonify(eresult)
        else:
            if 'nuser_id' in session:
                # get matched event with eventid
                eventId = ast.literal_eval(mactchEventId)
                cursor.execute("SELECT * FROM Events WHERE EventId IN %s", (eventId,))
                eresult = cursor.fetchall()
                cnx.close()
                return jsonify(eresult)
                return render_template('searchEventsResults.html', eresult=eresult, uid=uid, error=error)
            else:
                return redirect(url_for('main'))

# Route for handling the search events page logic
@app.route('/searchEventsMobile/<uid>', methods=['GET', 'POST'])
def searchEventsMobile(uid):
    error = None
    if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name, cursorclass=pymysql.cursors.DictCursor)
    else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        host = '127.0.0.1'
        cnx = pymysql.connect(user='livestrong19', password='livestrong19',
                              host='127.0.0.1', db='PickupSport', cursorclass=pymysql.cursors.DictCursor)
    with cnx.cursor() as cursor:
        if request.user_agent.platform == 'android':
            if request.method == 'POST':
                vname = request.form['name']
                date = request.form['date']
                startTime = request.form['start']
                endTime = request.form['end']
                if vname == '' or date == '' or startTime == '' or endTime == '':
                    error = 'Invalid Credentials. Please try again.'
                else:
                    cursor.execute("SELECT * FROM Venues WHERE VenueName = %s", (vname,))
                    vresult = cursor.fetchone()
                    vid = vresult['VenueId']
                    # get all events
                    cursor.execute("SELECT * FROM Events WHERE VenueId = %s AND EventDate = %s", (vid, date))
                    allEvents = cursor.fetchall()
                    matchList = []
                    for x in allEvents:
                        start = str(x['EventStartTime'])
                        end = str(x['EventEndTime'])
                        timeslot = CalculateTimeslots(start, end)
                        matchList.append((x['EventId'], timeslot))
                    givenTimeslot = CalculateTimeslots(startTime, endTime)
                    mactchEventId = []
                    for x in range(len(matchList)):
                        for time in matchList[x][1]:
                            for items in givenTimeslot:
                                if time in items:
                                    mactchEventId.append(matchList[x][0])
                        # return the id of events at a venue given date/time
                    mactchEventId = list(dict.fromkeys(mactchEventId))
                    cursor.execute("SELECT * FROM Events WHERE EventId IN %s", (mactchEventId,))
                    eresult = cursor.fetchall()
                    cnx.close()
                    return jsonify(eresult)
        else:
            if request.method == 'GET':
                vname = "Venue 1"
                date = "02-03-2019"
                startTime = "1600"
                endTime = "1800"
                if vname == '' or date == '' or startTime == '' or endTime == '':
                    error = 'Invalid Credentials. Please try again.'
                else:
                    cursor.execute("SELECT * FROM Venues WHERE VenueName = %s", (vname,))
                    vresult = cursor.fetchone()
                    vid = vresult['VenueId']
                    # get all events
                    cursor.execute("SELECT * FROM Events WHERE VenueId = %s AND EventDate = %s", (vid, date))
                    allEvents = cursor.fetchall()
                    matchList = []
                    for x in allEvents:
                        start = str(x['EventStartTime'])
                        end = str(x['EventEndTime'])
                        timeslot = CalculateTimeslots(start, end)
                        matchList.append((x['EventId'], timeslot))
                    givenTimeslot = CalculateTimeslots(startTime, endTime)
                    mactchEventId = []
                    for x in range(len(matchList)):
                        for time in matchList[x][1]:
                            for items in givenTimeslot:
                                if time in items:
                                    mactchEventId.append(matchList[x][0])
                        # return the id of events at a venue given date/time
                    mactchEventId = list(dict.fromkeys(mactchEventId))
                    cursor.execute("SELECT * FROM Events WHERE EventId IN %s", (mactchEventId,))
                    eresult = cursor.fetchall()
                    cnx.close()
                    return jsonify(eresult)

# Route for handling the show events page logic
@app.route('/showEvents/<uid>')
def showEvents(uid):
    error = None
    if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name, cursorclass=pymysql.cursors.DictCursor)
    else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        host = '127.0.0.1'
        cnx = pymysql.connect(user='livestrong19', password='livestrong19',
                              host='127.0.0.1', db='PickupSport', cursorclass=pymysql.cursors.DictCursor)
    with cnx.cursor() as cursor:
        if request.user_agent.platform == 'android':
            cursor.execute("SELECT EventId FROM User_Events WHERE uid = %s", (uid,))
            allresult = cursor.fetchall()
            eventList = []
            for result in allresult:
                eid = result['EventId']
                cursor.execute('''SELECT * FROM Events WHERE EventId = %s''', (eid,))
                eventResult = cursor.fetchall()
                eventList.extend(eventResult)
            cnx.close()
            return jsonify(eventList)
        else:
            if 'nuser_id' in session:
                cursor.execute("SELECT EventId FROM User_Events WHERE uid = %s", (uid,))
                allresult = cursor.fetchall()
                eventList = []
                for result in allresult:
                    eid = result['EventId']
                    cursor.execute('''SELECT * FROM Events WHERE EventId = %s''', (eid,))
                    eventResult = cursor.fetchall()
                    eventList.extend(eventResult)
                cnx.close()
                return render_template('showEvents.html',uid=uid, eventList=eventList)
            else:
                return redirect(url_for('main'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    error = None
    # When deployed to App Engine, the `GAE_ENV` environment variable will be
    # set to `standard`
    if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name, cursorclass=pymysql.cursors.DictCursor)
    else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        host = '127.0.0.1'
        cnx = pymysql.connect(user='livestrong19', password='livestrong19',
                              host='127.0.0.1', db='PickupSport', cursorclass=pymysql.cursors.DictCursor)
    with cnx.cursor() as cursor:
        if request.method == 'POST':
            uName = request.form['username'];
            statement = """SELECT * FROM Users WHERE uName = %s AND admin = 'True'""";
            cursor.execute(statement, uName);
            admin = cursor.fetchone()
            cnx.close()
            if request.user_agent.platform == 'android':
                if admin is None:
                    return jsonify({'message': "User does not exist. Please sign up."})
                elif admin['uPassword'] != request.form['password']:
                    return jsonify({'message': 'Password is incorrect'})
                else:
                    session['mobile_user_id'] = admin['uId']
                    return jsonify({'message': 'Successfully logged in', 'user_id': session['mobile_user_id']})
            else:

                    # Return true if such user found with Admin rights in Users table
                if admin is None:
                    flash('Invalid username')
                elif admin['uPassword'] != request.form['password']:
                    flash('Invalid password')
                else:
                    session['user_id'] = admin['uId']
                    return redirect(url_for('adminHome'))

    return render_template('admin.html', error=error)

@app.route('/adminHome')
def adminHome():
        if request.user_agent.platform == 'android':
            if 'mobile_user_id' in session:
                return jsonify({'message': 'Success'})
            else:
                return jsonify({'message': 'Login required'})

        else:
            if 'user_id' in session:
                return render_template('adminHome.html')
            else:
                return redirect(url_for('admin'))

@app.route('/adminLogout')
def adminlogout():
    error = None
    if request.user_agent.platform == 'android':
        session.pop('mobile_user_id', None)
        return jsonify({'message': 'User logged out'})
    else:
        session.pop('user_id', None)
        return redirect(url_for('admin'))

@app.route('/adminAddVenue', methods=['GET', 'POST'])
def adminAddVenue():

    if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name, cursorclass=pymysql.cursors.DictCursor)
    else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        host = '127.0.0.1'
        cnx = pymysql.connect(user='livestrong19', password='livestrong19',
                              host='127.0.0.1', db='PickupSport', cursorclass=pymysql.cursors.DictCursor)
    with cnx.cursor() as cursor:
        if request.user_agent.platform == 'android':
            if 'mobile_user_id' in session:
                if request.method == 'POST':
                    VenueName = request.form['vname'];
                    VenueZipcode = request.form['vzipcode']
                    VenueAddress = request.form['vaddress']
                    VenueOpeningTime = request.form['vopening']
                    VenueClosingTime = request.form['vclosing']
                    VenueSports = request.form['vsports']
                    statement = """INSERT INTO Venues(VenueName, VenueZipcode, VenueAddress, VenueOpeningTime, VenueClosingTime, VenueSports) VALUES(%s,%s,%s,%s,%s,%s)""";
                    data = (VenueName, VenueZipcode, VenueAddress, VenueOpeningTime, VenueClosingTime, VenueSports);
                    cursor.execute(statement, data);
                    cnx.commit()
                    cnx.close()
                    return jsonify({'message': 'Success'})
            else:
                return jsonify({'message': 'Login required'})
        else:
            if 'user_id' in session:
                if request.method == 'POST':
                    VenueName = request.form['vname'];
                    VenueZipcode = request.form['vzipcode']
                    VenueAddress = request.form['vaddress']
                    VenueOpeningTime = request.form['vopening']
                    VenueClosingTime = request.form['vclosing']
                    VenueSports = request.form['vsports']
                    statement = """INSERT INTO Venues(VenueName, VenueZipcode, VenueAddress, VenueOpeningTime, VenueClosingTime, VenueSports) VALUES(%s,%s,%s,%s,%s,%s)""";
                    data = (VenueName, VenueZipcode, VenueAddress, VenueOpeningTime, VenueClosingTime, VenueSports);
                    cursor.execute(statement, data);
                    cnx.commit()
                    cnx.close()
                    text = 'Venue added successfully.'
                    return redirect(url_for('adminAddVenue', text=text))
                return render_template('adminAddVenue.html')
            else:
                return redirect(url_for('admin'))


@app.route('/adminDeleteVenue', methods=['GET', 'POST'])
def adminDeleteVenue():
    if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name, cursorclass=pymysql.cursors.DictCursor)
    else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        host = '127.0.0.1'
        cnx = pymysql.connect(user='livestrong19', password='livestrong19',
                              host='127.0.0.1', db='PickupSport', cursorclass=pymysql.cursors.DictCursor)
    with cnx.cursor() as cursor:
        if request.user_agent.platform == 'android':
            if 'mobile_user_id' in session:
                if request.method == 'POST':
                    VenueName = request.form['vname'];
                    VenueZipcode = request.form['vzipcode']
                    statement = """DELETE FROM Venues WHERE VenueName = %s AND VenueZipcode = %s""";
                    data = (VenueName,VenueZipcode);
                    cursor.execute(statement, data);
                    cnx.commit()
                    cnx.close()
                    return jsonify({'message': 'Success'})
            else:
                return jsonify({'message': 'Login required'})
        else:
            if 'user_id' in session:
                if request.method == 'POST':
                    VenueName = request.form['vname'];
                    VenueZipcode = request.form['vzipcode']
                    statement = """DELETE FROM Venues WHERE VenueName = %s AND VenueZipcode = %s""";
                    data = (VenueName, VenueZipcode);
                    cursor.execute(statement, data);
                    cnx.commit()
                    cnx.close()
                    flash('Venue deleted successfully.')
                return render_template('adminDeleteVenue.html')
            else:
                return redirect(url_for('admin'))

@app.route('/adminDeleteUser', methods=['GET', 'POST'])
def adminDeleteUser():
    if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name, cursorclass=pymysql.cursors.DictCursor)
    else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        host = '127.0.0.1'
        cnx = pymysql.connect(user='livestrong19', password='livestrong19',
                              host='127.0.0.1', db='PickupSport', cursorclass=pymysql.cursors.DictCursor)
    with cnx.cursor() as cursor:
        if request.user_agent.platform == 'android':
            if 'mobile_user_id' in session:
                if request.method == 'POST':
                    UserEmail = request.form['uemail'];
                    statement = """DELETE FROM Users WHERE uEmail = %s""";
                    data = (UserEmail);
                    cursor.execute(statement, data);
                    cnx.commit()
                    cnx.close()
                    return jsonify({'message': 'Success'})
            else:
                return jsonify({'message': 'Login required'})
        else:
            if 'user_id' in session:
                if request.method == 'POST':
                    UserEmail = request.form['uemail'];
                    statement = """DELETE FROM Users WHERE uEmail = %s""";
                    data = (UserEmail);
                    cursor.execute(statement, data);
                    cnx.commit()
                    cnx.close()
                    flash('User deleted successfully.')
                return render_template('adminDeleteUser.html')
            else:
                return redirect(url_for('admin'))

@app.route('/adminDeleteEvent', methods=['GET', 'POST'])
def adminDeleteEvent():
    if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name, cursorclass=pymysql.cursors.DictCursor)
    else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        host = '127.0.0.1'
        cnx = pymysql.connect(user='livestrong19', password='livestrong19',
                              host='127.0.0.1', db='PickupSport', cursorclass=pymysql.cursors.DictCursor)
    with cnx.cursor() as cursor:
        if request.user_agent.platform == 'android':
            if 'mobile_user_id' in session:
                if request.method == 'POST':
                    EventName = request.form['ename'];
                    EventDate = request.form['edate'];
                    statement = """DELETE FROM Events WHERE EventName = %s AND EventDate = %s""";
                    data = (EventName,EventDate);
                    cursor.execute(statement, data);
                    cnx.commit()
                    cnx.close()
                    return jsonify({'message': 'Success'})
            else:
                return jsonify({'message': 'Login required'})
        else:
            if 'user_id' in session:
                if request.method == 'POST':
                    EventName = request.form['ename'];
                    EventDate = request.form['edate'];
                    statement = """DELETE FROM Events WHERE EventName = %s AND EventDate = %s""";
                    data = (EventName, EventDate);
                    cursor.execute(statement, data);
                    cnx.commit()
                    cnx.close()
                    flash('Event deleted successfully.')
                return render_template('adminDeleteEvent.html')
            else:
                return redirect(url_for('admin'))

@app.route('/info')
def info():
   error = None
   return render_template('info.html',error=error)

@app.route('/about')
def about():
   error = None
   return render_template('about.html',error=error)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)