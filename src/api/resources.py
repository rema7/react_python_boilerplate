from copy import deepcopy

import settings as app_settings
from db.session import open_db_session
from db.models import ToDo
from api.helpers import (
    raise_404,
    validate_schema
)

todo_post = open("api/schemas/todo-post.json").read()


class SettingsResource:
    def on_get(self, req, resp):
        business_logic_keys = (
            'offset',
        )
        resp.body = {key: getattr(app_settings, key.upper())
                     for key in business_logic_keys}


class ToDoResource(object):
    def on_get(self, req, resp, todo_id=None):
        with open_db_session() as session:
            todos = session.query(ToDo)
            if todo_id is not None:
                todo = todos.filter(ToDo._id == todo_id).first()
                if todo is None:
                    raise_404("ToDo reccord with id={} not found".format(todo_id))
                result = todo.as_dict()
            else:
                result = []
                for todo in todos.all():
                    result.append(todo.as_dict())
        resp.body = {
            'result': result
        }

    def post_body(self, title, description, todo_id=None):
        with open_db_session() as session:
            todo = session.query(ToDo).filter(ToDo._id == todo_id).first()
            if todo_id is not None and todo is None:
                raise_404("ToDo with id={} not found".format(todo_id))
            if todo is not None:
                todo.update(title, description)
            else:
                new_todo = ToDo(title=title, description=description)
                session.add(new_todo)
                session.flush()
                todo = deepcopy(new_todo)
                session.commit()
        return {
            'result': todo.as_dict()
        }

    def on_post(self, req, resp, todo_id=None):
        body = req.context['body']
        validate_schema(body, todo_post)

        resp.body = self.post_body(
            todo_id=body['id'] if 'id' in body else None,
            title=body['title'],
            description=body['description'],
        )

    def on_delete(self, req, resp, todo_id):
        if todo_id is not None:
            with open_db_session() as session:
                todo = session.query(ToDo).filter(
                    ToDo._id == todo_id).first()
                if todo is not None:
                    session.delete(todo)
                    session.commit()
                else:
                    raise_404("ToDo with id={} not found".format(todo_id))
        resp.body = {
            'result': todo_id
        }
