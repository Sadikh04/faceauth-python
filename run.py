from faceAuth import app, db
from flask_migrate import Migrate

migrate = Migrate(app, db)

if __name__ == '__main__':
    with app.app_context():
         db.create_all()
    app.run(host='0.0.0.0', port=3000, debug=True)

# if __name__ == '__main__':
#     db.create_all()
#     app.run(host='0.0.0.0', port=3000, debug=True)