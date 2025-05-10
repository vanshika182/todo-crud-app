from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY, title TEXT, description TEXT, done BOOLEAN)''')
    conn.commit()
    conn.close()

# CRUD API routes
@app.route('/')
def index():
    return render_template('index.html')  # Serve the HTML page

@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tasks')
    tasks = c.fetchall()
    conn.close()
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    title = request.json['title']
    description = request.json['description']
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('INSERT INTO tasks (title, description, done) VALUES (?, ?, ?)', (title, description, False))
    conn.commit()
    conn.close()
    return 'Task added', 201

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    title = request.json['title']
    description = request.json['description']
    done = request.json['done']
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('UPDATE tasks SET title = ?, description = ?, done = ? WHERE id = ?', (title, description, done, id))
    conn.commit()
    conn.close()
    return 'Task updated', 200

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return 'Task deleted', 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
