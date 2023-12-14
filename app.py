import os
import tensorflow as tf
import numpy as np

from PIL import Image
import cv2
from keras.models import load_model
from flask import Flask,request,render_template,jsonify,flash,session,redirect
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin,login_user,LoginManager,logout_user,current_user
from flask_login import login_required
import bcrypt 

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': "skindetection", 
#         'USER': "skindetection",
#         'PASSWORD': "binam",
#         'HOST': "localhost", 
#         'PORT': "",
#     }


app = Flask(__name__)
# database section
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://skindetection:binam@localhost/postgres'
app.config['SECRET_KEY']='okookkokko'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class doctorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    specialized = db.Column(db.String(100))
    introduction = db.Column(db.String(100))
    photopath = db.Column(db.String(100))
    phoneNumber = db.Column(db.String(100))


class addDoctors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    specialized = db.Column(db.String(100))
    introduction = db.Column(db.String(100))
    photopath = db.Column(db.String(255))
    phoneNUmber = db.Column(db.String(100))



class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100),unique=True)
    message = db.Column(db.Text)  


class Signup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)  # Assuming email is unique for each user
    password = db.Column(db.String(100))
    phoneNumber = db.Column(db.String(100))
    role = db.Column(db.Boolean)
    profession = db.Column(db.String(100))


    def __init__(self,email,password,name,phoneNumber,role,profession):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.phoneNumber = phoneNumber
        self.profession = profession

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))



@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email =request.form['email']
        password =request.form['password']
        if email == 'admin@yopmail.com' and password == 'admin':
            return redirect('/allDoctors')
        user = Signup.query.filter_by(email = email).first()

        if user and user.check_password(password):
            session['name']=user.name
            session['email']=user.email
            session['password']=user.password
            session['logged_in'] = True

            return redirect('/predict')
        else:
            flash("username password incorrect")

            return render_template('login.html',error='Invalid User')
    return render_template('login.html')


@app.route("/predict", methods=["GET"])
def predict():
    if 'email' in session:
        user = Signup.query.filter_by(email=session['email']).first()
        return render_template('predict.html', user=user)
    else:
        flash('Please login first', 'error')
        return redirect("/login")


@app.route("/logout")
def logout():
    session.pop('email',None)
    session['logged_in'] = False
    return redirect('/login')

class Blog(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      heading = db.Column(db.String(100))
      blogdetail = db.Column(db.Text)  # Assuming email is unique for each user    
      profession = db.Column(db.String(100))


class faq(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      question = db.Column(db.Text)
      answer = db.Column(db.Text) 

# database end

model=load_model('skincancer10epocs.h5')
# print('Model loaded .Check https://127.0.0.1:5000/')

def get_className(classNo):
    if classNo ==0:
        return "No Skin Cancer"
    elif classNo == 1:
        return "Skin Cancer"


def getResults(img):
    image=cv2.imread(img)
    image=Image.fromarray(image,'RGB')
    image=image.resize((64,64))
    image=np.array(image)
    input_img=np.expand_dims(image,axis=0)
    result=model.predict(input_img)
    return result


@app.route("/",methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/home",methods=["GET"])
def home():
    return render_template("index.html")

# @app.route("/predict",methods=["GET"])
# def predict():
#     return render_template("predict.html")






# @app.route("/login",methods=["GET"])
# def login():
#     return render_template("login.html")

# @app.route('/api/checkCredentials', methods=['POST'])
# def check_credentials():
#     # Retrieve the data from the request
#     data = request.get_json()
#     email = data.get('email')
#     password = data.get('password')
 
#     # Check if the credentials exist in the signup table
#     user = Signup.query.filter_by(email=email, password=password).first()
#     print(user)
#     if user:
#         return jsonify({'success': True}), 200
#     else:
#         return jsonify({'success': False}), 401


@app.route('/predict',methods=['GET','POST'])
def upload():
    if request.method =='POST':
        f=request.files['file']

        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        value= getResults(file_path)
        result=get_className(value)
        return result
    return None

@app.route("/output",methods=["GET"])
def output():
    return render_template("output.html")


# @app.route('/contact',methods=["GET"])
# def contact():
#     return render_template("contact.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        # Check if the email already exists in the Contact table
        existing_contact = Contact.query.filter_by(email=email).first()
        if existing_contact:
            flash("Email already exists", "error")
        else:
            # Create a new Contact instance and add it to the database
            new_contact = Contact(name=name, email=email, message=message)
            db.session.add(new_contact)
            db.session.commit()

            flash("Message sent successfully", "success")

    return render_template("contact.html")


@app.route('/signup',methods=["GET"])
def signup():
    return render_template("signup.html")


@app.route('/about',methods=["GET"])
def about():
    return render_template("about.html")


@app.route('/admin',methods=["GET"])
def admin():
    doctors = addDoctors.query.all()

    return render_template("admin.html")

@app.route("/blog",methods=["GET"])
def blog():
    return render_template("blog.html")


@app.route("/faqs",methods=["GET"])
def faqs():
    return render_template("faq.html")


@app.route("/message",methods=["GET"])
def message():
    return render_template("message.html")


@app.route("/faquser",methods=["GET"])
def faquser():
    return render_template("faqot.html")

@app.route('/fetchfaqs')
def fetchfaqs():
    faqs = faq.query.all()
    faqs_list = [{'question': faq.question, 'answer': faq.answer} for faq in faqs]
    return jsonify(faqs_list)

@app.route('/fetchblogs')
def fetchblogs():
    blog = Blog.query.all()
    blog_list = [{'heading': blog.heading, 'blogdetail': blog.blogdetail,'profession':blog.profession} for blog in blog]
    return jsonify(blog_list)

@app.route('/mainadmin',methods=["GET"])
def mainadmin():
    return render_template("mainAdmin.html")

# Update the route to work with the 'addDoctors' model
@app.route('/add_doctor', methods=['POST'])
def add_doctor():
    if request.method == 'POST':
        # Extract form data
        name = request.form['name']
        specialized = request.form['specialized']  # Updated to 'specialized'
        introduction = request.form['introduction']
        # photopath = request.form['photopath']  # Added 'photopath' field
        phoneNUmber = request.form['phoneNUmber']  # Added 'phoneNUmber' field

        if 'photopath' in request.files:
            file = request.files['photopath']
            if file.filename != '':
                # Save the file to the desired directory
                upload_folder = 'scds/static/img'
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                file_path = os.path.join(upload_folder, file.filename)
                file.save(file_path)

        new_doctor = addDoctors(name=name, specialized=specialized, introduction=introduction, photopath=file_path, phoneNUmber=phoneNUmber)

        # Add the new instance to the database session
        db.session.add(new_doctor)

        # Commit the changes to the database
        db.session.commit()

    doctors = addDoctors.query.all()  # Fetch all doctors from the 'addDoctors' table
    return render_template("admin.html", doctors=doctors)  # Redirect to the desired page after adding the doctor


from flask import request, jsonify

@app.route('/addUser', methods=['POST'])
def addUser():
    if request.method == 'POST':
        try:
            # Extract JSON data
            data = request.get_json()
            name = data['name']
            email = data['email']
            password = data['password']
            phoneNumber = data['phoneNumber']
            profession = data['profession']

            existing_user = Signup.query.filter_by(email=email).first()
            if existing_user:
                return jsonify({'message': 'Email already exists', 'status': 'error'}), 400

            new_user = Signup(name=name, email=email, password=password, phoneNumber=phoneNumber, profession=profession,role=True)
            db.session.add(new_user)
            db.session.commit()
           

            return jsonify({'message': 'User added successfully', 'status': 'success'}), 200
        except KeyError as e:
            return jsonify({'message': f'Missing required field: {e.args[0]}', 'status': 'error'}), 400
        except Exception as e:
            return jsonify({'message': f'An error occurred: {str(e)}', 'status': 'error'}), 500
       



@app.route('/allBlogs')
def all_blogs():
    blogs = Blog.query.all()  # Fetch all blogs from the database
    return render_template('blog.html', blogs=blogs)

@app.route('/allfaqs')
def all_faqs():
    faqs = faq.query.all()  # Fetch all faq from the database
    return render_template('faq.html', faqs=faqs)

@app.route('/allMessage')
def allMessage():
    faqs = Contact.query.all()  # Fetch all faq from the database
    return render_template('message.html', faqs=faqs)

@app.route('/fetch_contact_data', methods=['GET'])
def fetch_contact_data():
    contacts = Contact.query.all()
    contact_data = [{'name': contact.name, 'email': contact.email, 'message': contact.message} for contact in contacts]
    return jsonify(contact_data)

@app.route('/addfaq', methods=['POST'])
def addfaq():
    if request.method == 'POST':
        try:
            print("okokoko")
            # Extract JSON data
            data = request.get_json()
            question = data['question']
            answer = data['answer']

        
            faqs = faq(question=question, answer=answer)
            db.session.add(faqs)
            db.session.commit()
           

            return jsonify({'message': 'Blog added successfully', 'status': 'success'}), 200
        except KeyError as e:
            return jsonify({'message': f'Missing required field: {e.args[0]}', 'status': 'error'}), 400
        except Exception as e:
            return jsonify({'message': f'An error occurred: {str(e)}', 'status': 'error'}), 500
       
    

@app.route('/addBlog', methods=['POST'])
def addBlog():
    if request.method == 'POST':
        try:
            # Extract JSON data
            data = request.get_json()
            heading = data['heading']
            blogdetail = data['blogdetail']
            profession = data['profession']

        
            new_user = Blog(heading=heading, blogdetail=blogdetail,profession=profession)
            db.session.add(new_user)
            db.session.commit()
           

            return jsonify({'message': 'Blog added successfully', 'status': 'success'}), 200
        except KeyError as e:
            return jsonify({'message': f'Missing required field: {e.args[0]}', 'status': 'error'}), 400
        except Exception as e:
            return jsonify({'message': f'An error occurred: {str(e)}', 'status': 'error'}), 500
       
    
# Create a new route to fetch all doctors
@app.route('/allDoctors')
def all_doctors():
    doctors = addDoctors.query.all()  # Fetch all doctors from the database
    return render_template('admin.html', doctors=doctors)

# # ...
@app.route('/fetchDoctors/<specialization>')
def fetch_doctors(specialization):
    doctors = addDoctors.query.filter_by(specialized=specialization).all()
    doctors_data = [{'name': doctor.name, 'introduction': doctor.introduction, 'photopath': doctor.photopath, 'phoneNumber': doctor.phoneNUmber} for doctor in doctors]
    return jsonify(doctors_data)

@app.route('/deleteBlog', methods=['POST'])
def delete_blog():
    if request.method == 'POST':
        try:
            data = request.get_json()
            blog_id = data.get('blogId')

            # Assuming you have a model named Blog and a corresponding database table
            blog = Blog.query.get(blog_id)
            print(blog,"blog")
            if blog:
                db.session.delete(blog)
                db.session.commit()
                return jsonify({'message': 'Blog deleted successfully', 'status': 'success'}), 200
            else:
                return jsonify({'message': 'Blog not found', 'status': 'error'}), 404
        except Exception as e:
            return jsonify({'message': f'An error occurred: {str(e)}','status': 'error'}), 500

if __name__ =='__main__':
    app.run(port=12000,debug=True)
