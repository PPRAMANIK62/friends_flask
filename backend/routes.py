from app import app, db
from flask import request, jsonify
from models import Friend

# get all friends
@app.route('/api/friends', methods=['GET'])
def get_friends():
    friends = Friend.query.all()
    return jsonify([friend.to_json() for friend in friends])

# create a friend
@app.route('/api/friends', methods=['POST'])
def create_friend():
    try:
        data = request.json

        # validations
        required_fields = ['name', 'role', 'description', 'gender']
        for field in required_fields:
            if field not in data or not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400

        name = data.get('name')
        role = data.get('role')
        description = data.get('description')
        gender = data.get('gender')

        first_name = name.split(' ')[0]
        last_name = name.split(' ')[-1]

        # fetch avatar image base on gender from https://avatar-placeholder.iran.liara.run
        if gender == "male":
            img_url = f"https://avatar.iran.liara.run/public/boy?username={first_name}_{last_name}"
        elif gender == "female":
            img_url = f"https://avatar.iran.liara.run/public/girl?username={first_name}_{last_name}"
        else:
            img_url = None

        new_friend = Friend(name=name, role=role, description=description, gender=gender, img_url=img_url)

        # to staging state
        db.session.add(new_friend)
        # commit the changes
        db.session.commit()

        return jsonify(new_friend.to_json()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# update a friend
@app.route('/api/friends/<int:id>', methods=['PUT'])
def update_friend(id):
    try:
        data = request.json

        friend = Friend.query.get(id)
        if not friend:
            return jsonify({'error': 'Friend not found'}), 404

        # validations
        required_fields = ['name', 'role', 'description', 'gender']
        for field in required_fields:
            if field not in data or not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400

        name = data.get('name', friend.name)
        role = data.get('role', friend.role)
        description = data.get('description', frinend.description)
        gender = data.get('gender', friend.gender)

        first_name = name.split(' ')[0]
        last_name = name.split(' ')[-1]

        # fetch avatar image base on gender from https://avatar-placeholder.iran.liara.run
        if gender == "male":
            img_url = f"https://avatar.iran.liara.run/public/boy?username={first_name}_{last_name}"
        elif gender == "female":
            img_url = f"https://avatar.iran.liara.run/public/girl?username={first_name}_{last_name}"
        else:
            img_url = None

        friend.name = name
        friend.role = role
        friend.description = description
        friend.gender = gender
        friend.img_url = img_url

        # commit the changes
        db.session.commit()

        return jsonify(friend.to_json()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# delete a friend
@app.route('/api/friends/<int:id>', methods=['DELETE'])
def delete_friend(id):
    try:
        friend = Friend.query.get(id)
        if not friend:
            return jsonify({'error': 'Friend not found'}), 404

        # to staging state
        db.session.delete(friend)
        # commit the changes
        db.session.commit()

        return jsonify({'message': 'Friend deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
