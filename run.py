from myapp import create_app, db

app = create_app()

with app.app_context():
    db.create_all()  # Creates database tables

if __name__ == '__main__':
    app.run(debug=True)