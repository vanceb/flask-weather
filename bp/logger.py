from flask import Blueprint, request, g, abort, jsonify, render_template
from datetime import datetime

import pymongo
from models.logline import Logline


logger = Blueprint('logger', __name__, template_folder='templates')

@logger.route('/data', methods=['POST'])
def log():
    g.log.debug("Entered /data (POST) Blueprint handler")
    try:
        incoming = request.get_json()
    except:
        g.log.debug("Exception when trying request.get_json")
        abort(400)
    g.log.debug(incoming)
    # Register the schema
    g.connection.register([Logline])

    collection = g.connection['weather'].logs
    data = collection.Logline()
    for value in data.structure:
        if value in incoming:
            if value == 'logtime':
                data[value] = datetime.strptime(incoming[value], "%Y-%m-%dT%H:%M:%S.%f")
            else:
                data[value] = incoming[value]
    try:
        g.log.debug("About to save to MongoDB: " + str(data))
        data.save()
        return jsonify({'status': 'OK'})
    except:
        g.log.error("Data failed to validate")
        abort(400)

@logger.route('/data', methods=['GET'], defaults={'maxResults': 50})
@logger.route('/data/<int:maxResults>', methods=['GET'])
def latest(maxResults):
    g.log.debug("Entered /data (GET) Blueprint handler")

    # Perform the search and render results
    results = []
    for result in g.connection.weather.logs.find().sort([("_id", pymongo.DESCENDING)]).limit(maxResults):
        result['_id'] = str(result.pop('_id'))
        result['logtime'] = datetime.strftime(result.pop('logtime'), '%Y-%m-%dT%H:%M:%SZ')
        results.append(result)
    #return jsonify({'status': 'OK', 'results': results})
    display = {'headings': Logline.field_names, 'columns': Logline.display_fields}
    return render_template("list.html", entries=results, display=display)
