from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import sys

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/fsnd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<Todo ID: {self.id}, Description: {self.description}>'

db.create_all()

#----------------------------------------------------------------------------#
# Function needs to know.
#----------------------------------------------------------------------------#

# Insert.
#  ----------------------------------------------------------------
todo1 = Todo(description='Do a thing 1')
todo2 = Todo(description='Do a thing 2')
todo3 = Todo(description='Do a thing 3')

db.session.add(todo1)
db.session.add_all([todo2, todo3])

# Alter.
#  ----------------------------------------------------------------
todo3.name = 'Do a thing 3 and 4'

db.session.commit()

# Select.
#  ----------------------------------------------------------------

result = Todo.query.filter_by(id=1).all()  
Todo.query.all()  
Todo.query.filter_by(id=2).first()  
db.sessiom.query(Todo)

# Delete.
#  ----------------------------------------------------------------

db.session.delete(todo4)
Todo.query.filter_by(id=5).delete() 

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

# getting user data from a view to a controller
#  ----------------------------------------------------------------

@app.route('/')
def index():
  return render_template('index.html', data=[{
    'description': 'Todo 1'
  }, {
    'description': 'Todo 2'
  }, {
    'description': 'Todo 3'
  }])


# getting user data from a view to a controller using form
#  ----------------------------------------------------------------

@app.route('/todos/create', methods=['POST'])
def create_todo():
    description = request.form.get('description', '')
    todo = Todo(description=description)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.all())

# getting user data from a view to a controller using json
#  ----------------------------------------------------------------

@app.route('/todos/create', methods=['POST'])
def create_todo():
  error = False
  body = {}
  try:
    description = request.get_json()['description']
    todo = Todo(description=description)
    db.session.add(todo)
    db.session.commit()
    body['description'] = todo.description
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort (400)
  else:
    return jsonify(body)

@app.route('/')
def index2():
  return render_template('index2.html', data=Todo.query.all())

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

if __name__ == '__main__':
    app.run()
