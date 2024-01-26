from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods = ['GET', 'POST'])
def messages():
    messages = Message.query.order_by(Message.created_at).all()

    if request.method == 'GET':
        messages_list = [message.to_dict() for message in messages]

        response = make_response(
            jsonify(messages_list),
            200
        )

        return response

    elif request.method == 'POST':

        # using request.json.get() instead of request.form.get() because we want to take raw data as input instead of form.

        new_message = Message(
            body = request.json.get("body"),
            username = request.json.get("username"),
        )

        db.session.add(new_message)
        db.session.commit()

        new_message_dict = new_message.to_dict()

        response = make_response(
            jsonify(new_message_dict),
            201
        )

        return response


@app.route('/messages/<int:id>', methods = ['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()

    if request.method == 'GET':
        message_dict = message.to_dict()

        response = make_response(
            jsonify(message_dict),
            200
        )

        return response

    elif request.method == 'PATCH':
        message = Message.query.filter_by(id=id).first()

        # using request.json.get() instead of request.form.get() because we want to take raw data as input instead of form.

        for attr in request.json:
            setattr(message, attr, request.json.get(attr))

        db.session.add(message)
        db.session.commit()

        message_dict =message.to_dict()

        response = make_response(
            jsonify(message_dict),
            200
        )

        return response

    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()

        response_body = {
            "delete_successful": True,
            "message": "Review deleted."
        }

        response = make_response(
            jsonify(response_body),
            200
        )

        return response

if __name__ == '__main__':
    app.run(port=5555)
