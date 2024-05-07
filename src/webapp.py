import requests
from flask import Flask, request, jsonify, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DINERS.db'
db = SQLAlchemy(app)


# WEB API PART
# ----------------------------------------------------------------------------------------------------------------------
class Canteen(db.Model):
    __tablename__ = 'CANTEEN'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    location = db.Column(db.String)
    time_open = db.Column(db.String)
    time_closed = db.Column(db.String)


@app.route('/api/canteens', methods=['GET'])
def get_canteens():
    canteens = []
    canteens_db = Canteen.query.all()
    for canteen in canteens_db:
        canteen_serialised = {'id': canteen.id, 'name': canteen.name, 'location': canteen.location,
                              'time_open': canteen.time_open, 'time_closed': canteen.time_closed}
        canteens.append(canteen_serialised)

    return jsonify(canteens), 200

@app.route('/api/canteens/open/<time>', methods=['GET'])
def get_canteens_by_open_time(time):
    filtered_canteens = []
    canteens_db = Canteen.query.all()
    date_format = '%H:%M'
    for canteen in canteens_db:
        if (datetime.strptime(canteen.time_open, date_format).time() <= datetime.strptime(time, date_format).time()
                <= datetime.strptime(canteen.time_closed, date_format).time()):
            filtered_canteens.append(canteen)

    canteens = []
    for canteen in filtered_canteens:
        canteen_serialised = {'id': canteen.id, 'name': canteen.name, 'location': canteen.location,
                              'time_open': canteen.time_open, 'time_closed': canteen.time_closed}
        canteens.append(canteen_serialised)

    return jsonify(canteens), 200


@app.route('/api/add_canteen', methods=['POST'])
def post_add_canteen():
    name = request.form['name'].strip()
    location = request.form['location'].strip()
    time_open = request.form['time_open'].strip()
    time_closed = request.form['time_closed'].strip()

    canteen = Canteen(name=name, location=location, time_open=time_open, time_closed=time_closed)

    db.session.add(canteen)
    db.session.commit()

    serialized_canteen = {
        'id': canteen.id,
        'name': canteen.name,
        'location': canteen.location,
        'time_open': canteen.time_open,
        'time_closed': canteen.time_closed
    }

    db.session.close()

    return jsonify(serialized_canteen), 201




@app.route('/api/canteens/update/<int:canteen_id>', methods=['GET'])
def get_canteen(canteen_id):
    canteen = Canteen.query.filter_by(id=canteen_id).first()
    serialized_canteen = {
        'id': canteen.id,
        'name': canteen.name,
        'location': canteen.location,
        'time_open': canteen.time_open,
        'time_closed': canteen.time_closed
    }
    return jsonify(serialized_canteen), 200




@app.route('/api/canteens/update/', methods=['PUT'])
def put_update_canteens():
    canteen = Canteen.query.filter_by(id=request.form['id']).first()
    canteen.name = request.form['name'].strip()
    canteen.location = request.form['location'].strip()
    canteen.time_open = request.form['time_open'].strip()
    canteen.time_closed = request.form['time_closed'].strip()

    serialized_canteen = {
        'id': canteen.id,
        'name': canteen.name,
        'location': canteen.location,
        'time_open': canteen.time_open,
        'time_closed': canteen.time_closed
    }

    db.session.commit()
    db.session.close()

    return jsonify(serialized_canteen), 200


@app.route('/api/canteens/delete/<int:canteen_id>', methods=['DELETE'])
def delete_api_canteen(canteen_id):
    canteen = Canteen.query.filter_by(id=canteen_id).first()
    if canteen is not None:
        db.session.delete(canteen)
        db.session.commit()
        db.session.close()

    return jsonify({'message': 'Deleted successfully'}), 200


# WEB APP PART
# ----------------------------------------------------------------------------------------------------------------------
@app.route('/', methods=['GET'])
def show_canteens():

    response = requests.get(url_for('get_canteens', _external=True))

    if response.status_code == 200:

        canteens_json = response.json()
        deserialized_canteens = [Canteen(id=data['id'], name=data['name'],location=data['location'],
                        time_open=data['time_open'],time_closed=data['time_closed']) for data in canteens_json]

        return render_template('canteens.html', canteens=deserialized_canteens)
    else:
        return f"Error: Unable to retrieve canteens data. Status code: {response.status_code}"




@app.route('/canteens/open/', methods=['GET'])
def canteens_by_open_time():
    time = request.args.get('time')
    response = requests.get(url_for('get_canteens_by_open_time', time=time, _external=True))
    if response.status_code == 200:
        canteens_json = response.json()
        canteens = [Canteen(id=data['id'], name=data['name'],location=data['location'],
                            time_open=data['time_open'],time_closed=data['time_closed']) for data in canteens_json]

        return render_template('canteens_by_time.html', time=time, canteens=canteens)
    else:
        return f"Error: Unable to retrieve canteens data. Status code: {response.status_code} {time}"


@app.route('/add_canteen', methods=['GET', 'POST'])
def add_canteen():
    if request.method == 'POST':

        name = request.form['name']
        location = request.form['location']
        time_open = request.form['time_open']
        time_closed = request.form['time_closed']

        data = {
            'name': name,
            'location': location,
            'time_open': time_open,
            'time_closed': time_closed
        }

        response = requests.post(url_for('post_add_canteen', _external=True), data=data)
        if response.status_code == 201:
            return redirect(url_for('show_canteens', _external=True))
        else:
            return f"Error: Unable to add canteen. Status code: {response.status_code}"

    return render_template('add_canteen.html')


@app.route('/canteens/update/<int:canteen_id>', methods=['GET'])
def update_canteen(canteen_id):

    response = requests.get(url_for('get_canteen', canteen_id=canteen_id, _external=True))

    canteen_json = response.json()

    canteen = Canteen(id=canteen_json['id'], name=canteen_json['name'], location=canteen_json['location']
                       ,time_open=canteen_json['time_open'],time_closed=canteen_json['time_closed'])

    return render_template('update_canteen.html', canteen=canteen)


@app.route('/canteens/update/', methods=['POST'])
def post_update_canteens():
    c_id = request.form['id']
    name = request.form['name']
    location = request.form['location']
    time_open = request.form['time_open']
    time_closed = request.form['time_closed']

    data = {
        'id': c_id,
        'name': name,
        'location': location,
        'time_open': time_open,
        'time_closed': time_closed
    }

    response = requests.put(url_for('put_update_canteens', _external=True), data=data)

    if response.status_code == 200:
        return redirect(url_for('show_canteens', _external=True))
    else:
        return f"Error: Unable to update canteen. Status code: {response.status_code}"


@app.route('/canteens/validate/<int:canteen_id>', methods=['GET'])
def validate_canteen(canteen_id):
    response = requests.get(url_for('get_canteen', canteen_id=canteen_id, _external=True))
    if response.status_code == 200:
        canteen_json = response.json()

        canteen = Canteen(id=canteen_json['id'], name=canteen_json['name'], location=canteen_json['location'],
                          time_open=canteen_json['time_open'],time_closed=canteen_json['time_closed'])

        return render_template('delete_canteen.html', canteen=canteen, canteen_id=canteen_id)

    return redirect(url_for('show_canteens', _external=True))



@app.route('/canteens/delete/<int:canteen_id>', methods=['GET'])
def delete_canteen(canteen_id):
    response = requests.delete(url_for('delete_api_canteen', canteen_id=canteen_id, _external=True))
    if response.status_code == 200:
        return redirect(url_for('show_canteens', _external=True))
    else:
        return f"Error: Unable to delete canteen. Status code: {response.status_code}"


if __name__ == '__main__':

    app.run (debug=True)