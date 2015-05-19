from flask import Blueprint, request, g, abort, jsonify, render_template
from datetime import datetime
import pymongo

from models.logline import Logline
from summarize import Summarize

summary = Blueprint('summary', __name__, template_folder='templates')

@summary.route('/summary', methods=['GET'], defaults={'maxResults': 3600, 'period': 'hour'})
@summary.route('/summary/<period>', methods=['GET'], defaults={'maxResults': 3600})
@summary.route('/summary/<period>/<int:maxResults>', methods=['GET'])
def latestSummary(period, maxResults):
    g.log.debug("Entered /summary (GET) Blueprint handler")

    data = Summarize()

    if period.lower() == 'min' or period.lower() == 'minute':
        tagBy = '%Y-%m-%dT%H:%M:00Z'
    else:
        tagBy = '%Y-%m-%dT%H:00:00Z'

    # Perform the search and render results
    for result in g.connection.weather.logs.find().sort([("_id", pymongo.DESCENDING)]).limit(maxResults):
        result['_id'] = str(result.pop('_id'))
        tag = datetime.strftime(result['logtime'], tagBy)
        result['logtime'] = datetime.strftime(result.pop('logtime'), '%Y-%m-%dT%H:%M:%SZ')
        data.logData(tag, result)
    #return jsonify({'status': 'OK', 'results': data.summarize()})
    display = {'headings': ["in T1", "In T2", "In T3", "Out T", "Pressure", "Humidity", "Light", "Battery Voltage", "Solar Voltage"], \
               'columns': ["inT1", "inT2", "inT3", "outT", "pressure", "humidity", "light", "battery", "solar"]}
    return render_template("summary-table.html", entries=data.summarize(), display=display)
