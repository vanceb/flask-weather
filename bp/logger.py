from flask import Blueprint, request, g, abort, jsonify
from datetime import datetime

from models.logline import Logline


logger = Blueprint('logger', __name__, template_folder='templates')

@logger.route('/data', methods=['POST'])
def log():
    g.log.debug("Entered /data Blueprint handler")
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
                data[value] = datetime.strptime(incoming[value], "%Y-%m-%dT%H:%M:%SZ")
            else:
                data[value] = incoming[value]
    try:
        data.save()
        return jsonify({'status': 'OK'})
    except:
        g.log.error("Data failed to validate")
        abort(400)

