# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_cloudsql_mysql]
import os
from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
from jinja2 import Template
import pymysql
import pymysql.cursors

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

app = Flask(__name__)
app.secret_key = "secret"

if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        host = '127.0.0.1'
        cnx = pymysql.connect(user='livestrong19', password='livestrong19',
                              host='127.0.0.1', db='PickupSport')
        with cnx.cursor() as cursor:
            class Venues(db.Model):
                __tablename__ = "artists"

                id = db.Column(db.Integer, primary_key=True)
                name = db.Column(db.String)

                def __repr__(self):
                    return "{}".format(self.name)


            class Album(db.Model):
                """"""
                __tablename__ = "albums"

                id = db.Column(db.Integer, primary_key=True)
                title = db.Column(db.String)
                release_date = db.Column(db.String)
                publisher = db.Column(db.String)
                media_type = db.Column(db.String)

                artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"))
                artist = db.relationship("Artist", backref=db.backref(
                    "albums", order_by=id), lazy=True)

cnx.close()




