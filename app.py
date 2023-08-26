from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/flask'  # Replace with your database URI
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    completed = db.Column(db.Boolean, default=False)

@app.route('/tasks', methods=['POST'])
def insert_task():
    try:
        data = request.get_json()

        if not data.get('title') or len(data.get('title')) == 0:
            return jsonify({'message': 'Title is required'}), 400
        
        if not data.get('description') or len(data.get('description')) == 0:
            return jsonify({'message': 'Description is required'}), 400

        new_task = Tasks(
            title=data.get('title'),
            description=data.get('description')
        )

        db.session.add(new_task)

        db.session.commit()

        return jsonify({'message': 'Task added successfully', 
                        'task': {
                            'id': new_task.id, 
                            'title': new_task.title, 
                            'description': new_task.description, 
                            'completed': new_task.completed
                            }})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        tasks = Tasks.query.all()

        result = [{'id': task.id, 'title': task.title, 'description': task.description, 'completed': task.completed} for task in tasks]

        return jsonify(tasks=result)

    except Exception as e:
        return str(e)

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        task = Tasks.query.get(task_id)

        if task is None:
            return jsonify({'error': 'Task not found'}), 404

        data = request.get_json()

        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'completed' in data:
            task.completed = data['completed']

        db.session.commit()

        return jsonify({'message': 'Task updated successfully', 
                        'task': {
                            'id': task.id, 
                            'title': task.title, 
                            'description': task.description,
                            'completed': task.completed
                            }})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task_by_id(task_id):
    try:
        task = Tasks.query.get(task_id)

        if task is None:
            return jsonify({'error': 'Task not found'}), 404

        result = {'id': task.id, 'title': task.title, 'description': task.description, 'completed': task.completed}

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task_by_id(task_id):
    try:
        task = Tasks.query.get(task_id)

        if task is None:
            return jsonify({'error': 'Task not found'}), 404

        db.session.delete(task)
        db.session.commit()

        return jsonify({'message': 'Task deleted successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
