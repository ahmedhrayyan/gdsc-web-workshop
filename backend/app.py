from flask import Flask, request
from flask_cors import CORS
from datetime import datetime
import sqlite3


def get_db():
  conn = sqlite3.connect("tutorial.db")
  # sets the row_factory attribute to sqlite3.Row so you can have name-based access to columns.
  conn.row_factory = sqlite3.Row
  return conn


app = Flask(__name__)
CORS(app)

@app.post("/api/tasks")
def create_post():
  data = request.json
  if 'content' not in data:
    return {"error": "content is required"}, 400
  
  db = get_db()
  cursor = db.execute("INSERT INTO tasks (content, date) VALUES (?, ?)", (data['content'], datetime.utcnow()))
  db.commit()
  task = db.execute("SELECT * FROM tasks WHERE id = ?", (cursor.lastrowid,)).fetchone()
  db.close()
  return {"task": dict(task)}

@app.get("/api/tasks")
def get_posts():
  db = get_db()
  tasks = db.execute("SELECT * FROM tasks").fetchall()
  db.close()
  return {"data": [dict(task) for task in tasks]}

@app.delete("/api/tasks/<id>")
def delete_post(id):
  db = get_db()
  task = db.execute("SELECT * FROM tasks WHERE id = ?", (id,)).fetchone() 
  if not task:
    return {"error": "task not found"}, 404

  db.execute("DELETE FROM tasks WHERE id = ?", (id,))
  db.commit()
  return {"message": "success"}

@app.patch("/api/tasks/<id>")
def update_task(id):
  data = request.json
  if 'is_done' not in data:
    return {"error": "is_done is required"}, 400

  if not isinstance(data['is_done'], int) or data['is_done'] not in (0, 1):
    return {"error": "is_done must be 0 or 1"}, 400

  db = get_db()
  task = db.execute("SELECT * FROM tasks WHERE id = ?", (id,)).fetchone() 
  if not task:
    return {"error": "task not found"}, 404

  db.execute("UPDATE tasks SET is_done = ? WHERE id = ?", (request.json['is_done'], id))
  db.commit()
  task = db.execute("SELECT * FROM tasks WHERE id = ?", (id,)).fetchone()
  return {"data": dict(task)}