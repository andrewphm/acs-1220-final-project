from flaskbook_app.extensions import app, db
from flaskbook_app.main.routes import main
from flaskbook_app.auth.routes import auth

app.register_blueprint(main)
app.register_blueprint(auth)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
