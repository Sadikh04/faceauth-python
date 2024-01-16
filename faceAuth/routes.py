from io import BytesIO
from urllib.parse import urlparse
import cv2
import face_recognition
import numpy as np
from faceAuth import app, db, bcrypt
from flask import Response, current_app, render_template, request, redirect, url_for, flash
from faceAuth.modele import Utilisateur
from flask_login import current_user, login_user, logout_user, login_required
from flask import Flask



from .image_processor import ImageProcessor


image_processor = ImageProcessor()


@app.route("/")
def index():
    #return "<h1>HELLO WORLD!!!!!!!!!!</h1>"
    return render_template('landing.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Utilisateur.query.filter_by(email=email).first()

        if user is None or not user.check_password(password):
            flash('Email ou mot de passe invalide', 'error')
            return redirect(url_for('login'))


        login_user(user, remember=True)
        
        next_page = request.args.get('next')

        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('home')

        return redirect(next_page)

    return render_template('login.html')


@app.route("/inscription", methods=['GET', 'POST'])
def inscription():
    if current_user.is_authenticated:
        return redirect(url_for('home'))


    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        file = request.files['img']
        img_enBinaire = file.read()
        photo_personne = BytesIO(img_enBinaire)
        image = face_recognition.load_image_file(photo_personne)
        empreinte_fa = face_recognition.face_encodings(image)[0]

        users = Utilisateur.query.filter_by(email=email).first()
        print(users)
        if users == None :
            if password == confirm_password:
                hashed_password = bcrypt.generate_password_hash(password)
                hashed_confirmpassword = bcrypt.generate_password_hash(confirm_password)
                user = Utilisateur(username=username, email=email, photo = img_enBinaire, empreinte_facial = empreinte_fa, 
                    password = hashed_password, confirmpassword = hashed_confirmpassword)
     
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('home')) 
            else:
                erreur = 'Les mots de passe ne correspondent pas. Veuillez réessayer.'
                return render_template('inscription.html', erreur=erreur)

        elif  users :
            erreur = 'Cet adresse mail est déja existe déjà. Veuillez en choisir une autre.'
            return render_template('inscription.htm', erreur=erreur)
            
        else:
            erreur = 'Les mots de passe ne correspondent pas. Veuillez réessayer.'
            return render_template('inscription.html', erreur=erreur)
    return render_template('inscription.htm')

@app.route('/home')
@login_required
def home():
    return render_template('home.html', welcome_message=f"Bienvenue, {current_user.username}!")

@app.route('/auth-camera', methods=['GET', 'POST'])
def camera():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        return redirect(url_for("login"))

    return Response(image_processor.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/webcam', methods=['GET', 'POST'])
def webcam():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template('camera.html')
 
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

