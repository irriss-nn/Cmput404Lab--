#!/usr/bin/env python3

#!/usr/bin/env python3

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument("task")

TODOs = {
    1: {"task": "build an API"},#parser read task as a key 
    2: {"task": "?????"},
    3: {"task": "profit"},
}

#help function send a404 if a specific entry is not exit (tell user)
def abort_if_todo_not_found(todo_id):
    if todo_id not in TODOs:
        abort(404, message="TODO {} does not exist".format(todo_id))

# 
def add_todo(todo_id):
    args = parser.parse_args() #parse the argument to send to the use by the body 
    todo = {"task": args["task"]}
    TODOs[todo_id] = todo
    return todo
# create resouse class for the todo item
class Todo(Resource):
    """
    Shows a single TODO item and lets you delete a TODO item.
    """

    def get(self, todo_id):
        abort_if_todo_not_found(todo_id)
        return TODOs[todo_id]#check if the todo exist

    def delete(self, todo_id):#if user wants to delete tofo
        abort_if_todo_not_found(todo_id)#check id exist first
        del TODOs[todo_id] #delete from the dictionary
        return "", 204

    def put(self, todo_id):# create a new todo item
        return add_todo(todo_id), 201


class TodoList(Resource):
    """
    Shows a list of all TODOs and lets you POST to add new tasks.
    """

    def get(self): #get a list of todos
        return TODOs

    def post(self):#add a new todo item
        todo_id = max(TODOs.keys()) + 1  # create always get a new key
        return add_todo(todo_id), 201


api.add_resource(Todo, "/todos/<int:todo_id>")#point to new created resources
api.add_resource(TodoList, "/todos")#
if __name__ == "__main__":
    app.run(debug=True)