from flask import Flask, redirect, render_template, request
from model import *

app = create_app()

@app.route('/')
def create_db():  
    # db.create_all()
    # User1 = User(name='dvir')
    # db.session.add(User1)
    # db.session.commit()

    userfound = User.query.all()
    return str(userfound[3].id)
if __name__ == "__main__":
    app.run(debug=True)