from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug = True)