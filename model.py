# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask import Flask,request,render_template


# # DATABASES = {
# #     'default': {
# #         'ENGINE': 'django.db.backends.postgresql',
# #         'NAME': "skindetection", 
# #         'USER': "skindetection",
# #         'PASSWORD': "binam",
# #         'HOST': "localhost", 
# #         'PORT': "",
# #     }


# app = Flask(__name__)
# # database section
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://skindetection:binam@localhost/postgres'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)


# class doctorData(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     specialized = db.Column(db.String(100))
#     introduction = db.Column(db.String(100))
#     photopath = db.Column(db.String(100))



# class addDoctors(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     specialized = db.Column(db.String(100))
#     introduction = db.Column(db.String(100))
#     photopath = db.Column(db.String(100))
#     phoneNUmber = db.Column(db.String(100))

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     phoneNumber = db.Column(db.String(100))
#     role = db.Column(db.Boolean)
#     profession = db.Column(db.String(100))  # Add the 'profession' column
