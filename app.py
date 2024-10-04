from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# Connect to MongoDB
#client = MongoClient("mongodb://localhost:27017/")
client = MongoClient("mongodb://mongo:27017/")
db = client.todo_db  # Create database
todos_collection = db.todos  # Create collection

# Home route to display tasks and form
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get the task from form input
        task = request.form.get("task")
        if task:
            # Insert the task into MongoDB
            todos_collection.insert_one({"task": task})
            return redirect("/")
    
    # Fetch all tasks from the database
    todos = list(todos_collection.find())
    
    return render_template("index.html", todos=todos)

# Route to delete a task
@app.route("/delete/<task_id>")
def delete_task(task_id):
    # Delete task by its unique id
    todos_collection.delete_one({"_id": ObjectId(task_id)})
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)

