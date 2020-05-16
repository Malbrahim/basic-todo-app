# How to Setup a New Flask App on a Mac

#### MVC stands for Model-View-Controller
Layers
- Models: manage data and business logic for us. What happens inside models and database, capturing logical relationships and properties across the web app objects
- Views: handles display and representation logic. What the user sees (HTML, CSS, JS from the user's perspective)
- Controllers: routes commands to the models and views, containing control logic. Control how commands are sent to models and views, and how models and views wound up interacting with each other.


#### There are 3 methods of getting user data from a view to a controller. See the image below.
- URL query parameters: /hello?field1=value1 
``` 
value1 = request.args.get('field1')
```
- Form data
```
username = request.form.get('username')
password = request.form.get('password')
``` 
Note: defaults
request.args.get, request.form.get both accept an optional second parameter, e.g. request.args.get('foo', 'my default'), set to a default value, in case the result is empty.
- JSON
```
data_string = request.data
data_dictionary = json.load(data_string)
# or 
request.get_json()['name']
``` 

#### For each CRUD operation, there are corresponding SQL command

**1. CREATE**

CREATE TABLE table_name ( column1 datatype, column2 datatype,   ....);

```
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
```

INSERT INTO table () VALUES ();

```
todo1 = Todo(description='Do a thing 1')
todo2 = Todo(description='Do a thing 2')
todo3 = Todo(description='Do a thing 3')

db.session.add(todo1)
db.session.add_all([todo2, todo3])
db.session.commit()
```

**2. READ**

SELECT * FROM table_name WHERE condition;

```
result = Todo.query.filter_by(id=1).all()
Todo.query.all()
Todo.query.gt(1)
Todo.query.filter_by(id=2).first()
db.sessiom.query(Todo)

```

**3. UPDATE**

UPDATE table_name SET column1 = value1 WHERE condition;

```
todo = Todo.query.get(todo_id)
todo.name = 'new name'
db.session.commit()
```

**4. DELETE**

DELETE FROM table_name WHERE condition;

```
todo = Todo.query.get(todo_id)
db.session.delete(todo)
# or Todo.query.filter_by(id=todo_id).delete()
db.session.commit()
```


#### Modeling of relationship
**1- one-to-one**
```
children = db.relationship('ChildModel', backref='some_parent', lazy=True)
```
```ç
parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'), nullable=False)
```
note: parent_id only appear **once** in the child table
**2- many-to-many**
```
children = db.relationship('ChildModel', backref='some_parent', lazy=True)
```
```
parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'), nullable=False)
```
note: parent_id appear **many times** in the child table

**3- one-to-many**
- Define an association table using Table from SQLAlchemy
- Set the multiple foreign keys in the association table
- Map the association table to a parent model using the option secondary in db.relationship
```
order_items = db.Table('order_items',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)

class Order(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  status = db.Column(db.String(), nullable=False)
  products = db.relationship('Product', secondary=order_items,
      backref=db.backref('orders', lazy=True))

class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(), nullable=False)
```