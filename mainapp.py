from flask import Flask, jsonify, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Helper function for date validation
def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

@app.route('/habits', methods=['GET'])
def get_all():
    conn = sqlite3.connect('habits.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * from habits')
    rows = cursor.fetchall()
    conn.close()

    habits = []
    for row in rows:
        habit = {
            'id': row[0],
            'name': row[1],
            'date': row[2],
            'status': row[3],
            'note': row[4]
        }
        habits.append(habit)

    return jsonify(habits), 200

@app.route('/habits/<int:habit_id>', methods=['GET'])
def get_habit_by_id(habit_id):
    conn = sqlite3.connect('habits.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM habits WHERE id = ?', (habit_id,))
    habit = cursor.fetchone()
    conn.close()

    if habit is None:
        return jsonify({'error': 'Habit not found'}), 404
    
    result = {
        'id': habit[0],
        'name': habit[1],
        'date': habit[2],
        'status': habit[3],
        'note': habit[4]
    }
    return jsonify(result), 200

@app.route('/habits', methods=['POST'])
def add_new_habit():
    data = request.get_json()
    name = data.get('name')
    date = data.get('date')
    status = data.get('status')
    note = data.get('note', '')

    conn = sqlite3.connect('habits.db')
    cursor = conn.cursor()

    # Validations
    if not name:
        return jsonify({'error': 'Title is required'}), 400
    if not date:
        return jsonify({'error': 'Date is required'}), 400
    if not is_valid_date(date):
        return jsonify({'error': 'Date format is wrong'}), 400
    if not status:
        return jsonify({'error': 'Status is required'}), 400
    if status not in ['done', 'missed']:
        return jsonify({'error': 'Status is not expected value'}), 400
    
    cursor.execute(
      'INSERT INTO habits (name, date, status, note) VALUES (?, ?, ?, ?)',
        (name, date, status, note)
    )
    conn.commit()
    habit_id = cursor.lastrowid
    conn.close()

    new_habit = {
        'id': habit_id,
        'name': name,
        'date': date,
        'status': status,
        'note': note
    }
    return jsonify(new_habit), 201

if __name__ == "__main__":
    app.run(debug = True)