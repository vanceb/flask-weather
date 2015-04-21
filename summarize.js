var ONE_SECOND_MILLIS = 1000;
var ONE_MINUTE_MILLIS = 1000 * 60;
var ONE_HOUR_MILLIS = 1000 * 60 * 60;

function printResult(dataSet) {
	dataSet.result.forEach(function(document)  {
		printjson(document);
	});
}

function aggregateData(fromDate, toDate, groupDeltaMillis, enablePrintResult) {

	print("Aggregating from " + fromDate + " to " + toDate);

	var start = new Date();

	var groupBy = {
		"year" : {
			$year : "$logtime"
		},
		"dayOfYear" : {
			$dayOfYear : "$logtime"
		}
	};

	var sortBy = {
			"_id.year" : 1,
			"_id.dayOfYear" : 1
	};

	var appendSeconds = false;
	var appendMinutes = false;
	var appendHours = false;

	switch(groupDeltaMillis) {
		case ONE_SECOND_MILLIS :
			appendSeconds = true;
		case ONE_MINUTE_MILLIS :
			appendMinutes = true;
		case ONE_HOUR_MILLIS :
			appendHours = true;
	}

	if(appendHours) {
		groupBy["hour"] = {
			$hour : "$logtime"
		};
		sortBy["_id.hour"] = 1;
	}
	if(appendMinutes) {
		groupBy["minute"] = {
			$minute : "$logtime"
		};
		sortBy["_id.minute"] = 1;
	}
	if(appendSeconds) {
		groupBy["second"] = {
			$second : "$logtime"
		};
		sortBy["_id.second"] = 1;
	}

	var pipeline = [
		{
			$match: {
				"created_on" : {
					$gte: fromDate,
					$lt : toDate
				}
			}
		},
		{
			$project: {
				_id : 0,
				created_on : 1,
				value : 1
			}
		},
		{
			$group: {
					"_id": groupBy,
					"count": {
						$sum: 1
					},
					"avg": {
						$avg: "$value"
					},
					"min": {
						$min: "$value"
					},
					"max": {
						$max: "$value"
					}
				}
		},
		{
			$sort: sortBy
		}
	];

	var dataSet = db.weather.logs.aggregate(pipeline);
	var aggregationDuration = (new Date().getTime() - start.getTime())/1000;
	print("Aggregation took:" + aggregationDuration + "s");
	if(dataSet.result != null && dataSet.result.length > 0) {
		print("Fetched :" + dataSet.result.length + " documents.");
		if(enablePrintResult) {
			printResult(dataSet);
		}
	}
	var aggregationAndFetchDuration = (new Date().getTime() - start.getTime())/1000;
	if(enablePrintResult) {
		print("Aggregation and fetch took:" + aggregationAndFetchDuration + "s");
	}
	return {
		aggregationDuration : aggregationDuration,
		aggregationAndFetchDuration : aggregationAndFetchDuration
	};
}


function testFromDatesAggregation(matchDeltaMillis, groupDeltaMillis, type, enablePrintResult) {
	var aggregationTotalDuration = 0;
	var aggregationAndFetchTotalDuration = 0;
	testFromDates.forEach(function(testFromDate) {
		var timeInterval = calibrateTimeInterval(testFromDate, matchDeltaMillis);
		var fromDate = timeInterval.fromDate;
		var toDate = timeInterval.toDate;
		var duration = aggregateData(fromDate, toDate, groupDeltaMillis, enablePrintResult);
		aggregationTotalDuration += duration.aggregationDuration;
		aggregationAndFetchTotalDuration += duration.aggregationAndFetchDuration;
	});
	print(type + " aggregation took:" + aggregationTotalDuration/testFromDates.length + "s");
	if(enablePrintResult) {
		print(type + " aggregation and fetch took:" + aggregationAndFetchTotalDuration/testFromDates.length + "s");
	}
}
