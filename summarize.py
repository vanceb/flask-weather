
class Summarize():
    def __init__(self):
        self.data = {}

    def logData(self, key, data):
        if key in self.data:
            self.data[key].append(data)
        else:
            self.data[key] = [data]

    def delData(self, key):
        if key in self.data:
            self.data.pop(key)

    def readings(self, key):
        if key in self.data:
            return len(self.data)
        else:
            return None

    def max(self, key, field=None):
        if field:
            max = None
            for reading in self.data[key]:
                if not max:
                    max = reading[field]
                else:
                    if reading[field] > max:
                        max = reading[field]
            return max
        else:
            max = {}
            for reading in self.data[key]:
                if field not in max:
                    max[field] = reading[field]
                else:
                    if reading[field] > max[field]:
                        max[field] = reading[field]
            return max

    def min(self, key, field=None):
        if field:
            min = None
            for reading in self.data[key]:
                if not min:
                    min = reading[field]
                else:
                    if reading[field] < min:
                        min = reading[field]
            return min
        else:
            min = {}
            for reading in self.data[key]:
                if field not in min:
                    min[field] = reading[field]
                else:
                    if reading[field] < min[field]:
                        min[field] = reading[field]
            return min

    def avg(self, key, field=None):
        if field:
            sum = 0
            count = 0
            for reading in self.data[key]:
                if field in reading:
                    sum += self.data[key][field]
                    count += 1
            if count > 0:
                return sum/count
            else:
                return None
        else:
            sum = {}
            count = {}
            avg = {}
            for reading in self.data:
                for key in reading:
                    if key in sum:
                        sum[key] += reading[key]
                    else:
                        sum[key] = reading[key]
                    count[key] += 1
            for reading in sum:
                avg[reading] = sum[reading] / count[reading]
            return avg
