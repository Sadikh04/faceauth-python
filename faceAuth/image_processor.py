import cv2
import face_recognition
from faceAuth.modele import Utilisateur
from flask_login import login_user
import dlib

class ImageProcessor:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.face_detected = False  # Ajoutez cette ligne

        self.initialize_known_faces()

        self.face_detector = dlib.get_frontal_face_detector()
        self.tm = cv2.TickMeter()

    def initialize_known_faces(self):
        try:
            users = Utilisateur.query.all()
            for user in users:
                self.known_face_names.append(user.username)
                self.known_face_encodings.append(user.empreinte_facial)
            print("Données récupérées avec succès :", self.known_face_names, self.known_face_encodings)
        except Exception as erreur:
            print("Erreur lors de l'initialisation des visages connus :", erreur)
    
    def compare_face(self, input_encoding):
        for user in Utilisateur.query.all():
            matches = face_recognition.compare_faces([user.empreinte_facial], input_encoding, tolerance=0.45)
            if any(matches):
                login_user(user)  # Authentifier l'utilisateur
                return user.username

        return "Personne inconnue"

    def gen_frames(self):
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Erreur lors de l'ouverture de la caméra.")
            return

        with self.app.app_context():  # Créez un contexte d'application temporaire
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Pas d'image capturée")
                    break

                frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) ** 1.0)
                frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) ** 1.0)
                frame = cv2.resize(frame, (frameWidth, frameHeight))

                try:
                    # Convertir l'image en RGB pour l'utiliser avec face_recognition
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    # Redimensionner l'image avant de la passer à la fonction face_locations
                    face_locations = face_recognition.face_locations(cv2.resize(frame_rgb, (0, 0), fx=0.25, fy=0.25))

                    # Obtenir les encodages des visages détectés
                    face_encodings = face_recognition.face_encodings(frame_rgb, face_locations)

                    for face_encoding in face_encodings:
                        # Utiliser votre fonction compare_face pour obtenir le nom associé
                        name = self.compare_face(face_encoding)
                        print("{} se trouve dans la photo fournie".format(name))

                        if name != "Personne inconnue":
                            fichier = open("presence.txt", "a", encoding='utf-8')
                            fichier.write("\n" + name + ' ')
                            fichier.close()
                            #return redirect(url_for('home'))

                except cv2.error as e:
                    print(f"Erreur OpenCV : {e}")
                    break

                frame_bytes = self.process_frame(frame)
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')
