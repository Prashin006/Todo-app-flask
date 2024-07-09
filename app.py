from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# Specifying /// is a relative path while //// is an absolute path
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///test.db"
db = SQLAlchemy(app)

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Task {self.id}>"

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = ToDo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return 'An error occurred while creating the task!'
    else:
        tasks = ToDo.query.order_by(ToDo.date_created).all()
        return render_template('index.html',tasks=tasks, db=db)
    
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = ToDo.query.filter_by(id=id).first()

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return 'An error occurred while deleting the task!'

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task_to_update = ToDo.query.filter_by(id=id).first()
    if request.method == 'POST':
        task_to_update.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'An error occurred while updating the task!'
    else:
        return render_template('update.html',task=task_to_update)

if __name__ == '__main__':
    app.run(debug=True)