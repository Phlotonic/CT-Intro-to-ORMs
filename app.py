# Task 1: Setting Up Flask with Flask-SQLAlchemy

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:CapricornDog5!@localhost/gym_db'
db = SQLAlchemy(app)

# Define the Member model
class Member(db.Model):
    __tablename__ = 'members'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    join_date = db.Column(db.Date, nullable=False)


# Define the WorkoutSession model
class WorkoutSession(db.Model):
    __tablename__ = 'workoutsessions'
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    session_date = db.Column(db.Date, nullable=False)
    duration = db.Column(db.Integer, nullable=False)

    # Define the relationship to the Member model
    member = db.relationship('Member', backref=db.backref('workout_sessions', lazy=True))


# Task 2: Implementing CRUD Operations for Members Using ORM

# Route to add a new member
@app.route('/members', methods=['POST'])
def add_member():
    data = request.get_json()
    new_member = Member(name=data['name'], email=data['email'], join_date=data['join_date'])
    db.session.add(new_member)
    db.session.commit()
    return jsonify({'message': 'New member added!'}), 201

# Route to retrieve all members
@app.route('/members', methods=['GET'])
def get_members():
    members = Member.query.all()
    return jsonify([{'id': member.id, 'name': member.name, 'email': member.email, 'join_date': member.join_date} for member in members])

# Route to update a member
@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    data = request.get_json()
    member = Member.query.get(id)
    if not member:
        return jsonify({'message': 'Member not found!'}), 404
    member.name = data['name']
    member.email = data['email']
    member.join_date = data['join_date']
    db.session.commit()
    return jsonify({'message': 'Member updated!'})

# Route to delete a member
@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    member = Member.query.get(id)
    if not member:
        return jsonify({'message': 'Member not found!'}), 404
    db.session.delete(member)
    db.session.commit()
    return jsonify({'message': 'Member deleted!'})

# Task 3: Managing Workout Sessions with ORM

# Route to schedule a new workout session
@app.route('/workouts', methods=['POST'])
def add_workout():
    data = request.get_json()
    new_workout = WorkoutSession(member_id=data['member_id'], session_date=data['session_date'], duration=data['duration'])
    db.session.add(new_workout)
    db.session.commit()
    return jsonify({'message': 'New workout session added!'}), 201

# Route to retrieve all workout sessions for a specific member
@app.route('/members/<int:member_id>/workouts', methods=['GET'])
def get_workouts(member_id):
    workouts = WorkoutSession.query.filter_by(member_id=member_id).all()
    return jsonify([{'id': workout.id, 'session_date': workout.session_date, 'duration': workout.duration} for workout in workouts])

# Route to update a workout session
@app.route('/workouts/<int:id>', methods=['PUT'])
def update_workout(id):
    data = request.get_json()
    workout = WorkoutSession.query.get(id)
    if not workout:
        return jsonify({'message': 'Workout session not found!'}), 404
    workout.session_date = data['session_date']
    workout.duration = data['duration']
    db.session.commit()
    return jsonify({'message': 'Workout session updated!'})

# Route to delete a workout session
@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = WorkoutSession.query.get(id)
    if not workout:
        return jsonify({'message': 'Workout session not found!'}), 404
    db.session.delete(workout)
    db.session.commit()
    return jsonify({'message': 'Workout session deleted!'})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
