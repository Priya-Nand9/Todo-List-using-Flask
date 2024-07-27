from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    time = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
    
@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        todo_title = request.form['title']
        todo_desc = request.form['description']
        data = Todo(title=todo_title, description=todo_desc)
        db.session.add(data)
        db.session.commit()
    allTodo = Todo.query.all()
    
    return render_template("index.html",allTodo=allTodo)

@app.route("/delete/<int:sno>")
def delete(sno):
    delete_todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(delete_todo)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        todo_title = request.form['title']
        todo_desc = request.form['description']
        data =  Todo.query.filter_by(sno=sno).first()
        data.title = todo_title
        data.description = todo_desc
        db.session.add(data)
        db.session.commit()
        return redirect("/")
    
    update_todo = Todo.query.filter_by(sno=sno).first()
    return render_template("update.html",update_todo=update_todo)

if __name__ == "__main__":
    app.run(debug=True)

