
from datetime import date, datetime
from email.policy import default
from ensurepip import bootstrap
from turtle import title
from wsgiref.validate import validator
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy import desc
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_bootstrap import Bootstrap
app = Flask(__name__)

Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):   
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable = False)
    desc = db.Column(db.String(50))
    dated_create = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.id} - {self.title}"

@app.route("/", methods=['GET','POST'])
def index():
    return render_template('login.html')


@app.route("/signup", methods=['GET','POST'])
def signup():
    return render_template('signup.html')

@app.route("/todo", methods=['GET','POST'])
def todo():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)

@app.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(id=id).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo = Todo.query.filter_by(id=id).first()
    return render_template("update.html", todo=todo)

if __name__ == "__main__":
    app.run(debug=True)
