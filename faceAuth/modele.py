from faceAuth import db,login_manager,bcrypt, app
from flask_login import UserMixin


class Utilisateur(UserMixin, db.Model):
    __tablename__ = 'utilisateurs'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), index=True)
    email = db.Column(db.String(120), index=True)
    photo = db.Column(db.BLOB(2048))
    empreinte_facial = db.Column(db.BLOB, nullable=False)
    password = db.Column(db.String(128))
    confirmpassword = db.Column(db.String(128))

    def __repr__(self):
        return '<Utilisateur {}>'.format(self.username)
    
    def get_id(self):
        return (self.id)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    


@login_manager.user_loader
def load_user(user_id):
    return Utilisateur.query.get(int(user_id))