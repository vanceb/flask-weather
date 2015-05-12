import operator

class Summarize():
    def __init__(self):
        self.data = {}

    def getData(self):
        return self.data

    def logData(self, key, dataDict):
        if key in self.data:
            for field in dataDict:
                if field in self.data[key]:
                    self.data[key][field].append(dataDict[field])
                else:
                    self.data[key][field] = [dataDict[field]]
        else:
            self.data[key] = {}
            for field in dataDict:
                self.data[key][field] = [dataDict[field]]

    def summarize(self, key=None, field=None):
        result = {}
        if key == None:
            for k in self.data:
                result[k] = {}
                if field == None:
                    for f in self.data[k]:
                        summary = self._summarizeArray(k,f)
                        if summary != None:
                            result[k][f] = summary
                else:
                    if field in self.data[k]:
                        summary = self._summarizeArray(k,field)
                        if summary != None:
                            result[k][field] = summary
        else:
            if key in self.data:
                result[key] = {}
                if field == None:
                    for f in self.data[key]:
                        summary = self._summarizeArray(key,f)
                        if summary != None:
                            result[key][f] = summary
                else:
                    if field in self.data[key]:
                        summary = self._summarizeArray(key,field)
                        if summary != None:
                            result[key][field] = summary
        return sorted(result.items(), key=operator.itemgetter(0))

    def _summarizeArray(self, key, field):
        anyData = self._countNumArray(key, field)
        if anyData:
            result = {}
            result['count'] = anyData
            result['max'] = self._maxArray(key,field)
            result['min'] = self._minArray(key,field)
            result['avg'] = self._avgArray(key,field)
            return result
        else:
            return None

    def max(self, key=None, field=None):
        result = {}
        if key == None:
            for k in self.data:
                result[k] = {}
                if field == None:
                    for f in self.data[k]:
                        result[k][f] = self._maxArray(k,f)
                else:
                    if field in self.data[k]:
                        result[k][field] = self._maxArray(k,field)
        else:
            if key in self.data:
                result[key] = {}
                if field == None:
                    for f in self.data[key]:
                        result[key][f] = self._maxArray(key,f)
                else:
                    if field in self.data[key]:
                        result[key][field] = self._maxArray(key,field)
        return result

    def min(self, key=None, field=None):
        result = {}
        if key == None:
            for k in self.data:
                result[k] = {}
                if field == None:
                    for f in self.data[k]:
                        result[k][f] = self._minArray(k,f)
                else:
                    if field in self.data[k]:
                        result[k][field] = self._minArray(k,field)
        else:
            if key in self.data:
                result[key] = {}
                if field == None:
                    for f in self.data[key]:
                        result[key][f] = self._minArray(key,f)
                else:
                    if field in self.data[key]:
                        result[key][field] = self._minArray(key,field)
        return result

    def avg(self, key=None, field=None):
        result = {}
        if key == None:
            for k in self.data:
                result[k] = {}
                if field == None:
                    for f in self.data[k]:
                        result[k][f] = self._avgArray(k,f)
                else:
                    if field in self.data[k]:
                        result[k][field] = self._avgArray(k,field)
        else:
            if key in self.data:
                result[key] = {}
                if field == None:
                    for f in self.data[key]:
                        result[key][f] = self._avgArray(key,f)
                else:
                    if field in self.data[key]:
                        result[key][field] = self._avgArray(key,field)
        return result

    def count(self, key=None, field=None):
        result = {}
        if key == None:
            for k in self.data:
                result[k] = {}
                if field == None:
                    for f in self.data[k]:
                        result[k][f] = len(self.data(k,f))
                else:
                    if field in self.data[k]:
                        result[k][field] = len(self.data(k,field))
        else:
            if key in self.data:
                result[key] = {}
                if field == None:
                    for f in self.data[key]:
                        result[key][f] = len(self.data[key][f])
                else:
                    if field in self.data[key]:
                        result[key][field] = len(self.data[key][field])
        return result

    def getNumeric(self, key=None, field=None):
        result = {}
        if key == None:
            for k in self.data:
                result[k] = {}
                if field == None:
                    for f in self.data[k]:
                        result[k][f] = self._numArray(k,f)
                else:
                    if field in self.data[k]:
                        result[k][field] = self._numArray(k,field)
        else:
            if key in self.data:
                result[key] = {}
                if field == None:
                    for f in self.data[key]:
                        result[key][f] = self._numArray(key,f)
                else:
                    if field in self.data[key]:
                        result[key][field] = self._numArray(key,field)
        return result


    def countNumeric(self, key, field=None):
        result = {}
        if field == None:
            if key in self.data:
                for field in self.data[key]:
                    result[field] = len(self.data[key][field])
        else:
            result[field] = len(self.data[key][field])
        return result


    def _getNumber(self, value):
        try:
            return float(value)
        except:
            pass
        return None

    def _numArray(self, key, field):
        result = []
        if key in self.data:
            if field != None:
                if field in self.data[key]:
                    for value in self.data[key][field]:
                        v = self._getNumber(value)
                        if v != None:
                            result.append(v)
        return result

    def _countNumArray(self, key, field):
        return len(self._numArray(key, field))


    def _maxArray(self, key, field):
        result = None
        if key in self.data:
            if field != None:
                if field in self.data[key]:
                    for value in self.data[key][field]:
                        v = self._getNumber(value)
                        if v != None:
                            if result == None:
                                result = v
                            else:
                                if v > result:
                                    result = v
        return result

    def _minArray(self, key, field):
        result = None
        if key in self.data:
            if field != None:
                if field in self.data[key]:
                    for value in self.data[key][field]:
                        v = self._getNumber(value)
                        if v != None:
                            if result == None:
                                result = v
                            else:
                                if v < result:
                                    result = v
        return result

    def _avgArray(self, key, field):
        sum = 0
        count = 0
        if key in self.data:
            if field != None:
                if field in self.data[key]:
                    for value in self.data[key][field]:
                        v = self._getNumber(value)
                        if v != None:
                            count += 1
                            sum += v
        if count > 0:
            return sum/count
        else:
            return None
