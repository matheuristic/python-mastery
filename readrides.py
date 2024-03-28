import csv
from collections import namedtuple
from collections.abc import Sequence


def read_rides_as_tuples(filename):
    '''
    Read the bus ride data as a list of tuples
    '''
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)     # Skip headers
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = (route, date, daytype, rides)
            records.append(record)
    return records


def read_rides_as_dicts(filename):
    # records = []  # ex2_2
    records = RideData()  # ex2_5
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)     # Skip headers
        for row in rows:
            route, date, daytype, rides = row[:]
            rides = int(rides)
            record = {
                'route': route,
                'date': date,
                'daytype': daytype,
                'rides': rides,
            }
            records.append(record)
    return records


class Row:
    def __init__(self, route, date, daytype, rides):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides


def read_rides_as_class(filename):
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)     # Skip headers
        for row in rows:
            route, date, daytype, rides = row[:]
            rides = int(rides)
            record = Row(route, date, daytype, rides)
            records.append(record)
    return records


RowTup = namedtuple('RowTup', ['route', 'date', 'daytype', 'rides'])


def read_rides_as_namedtuple(filename):
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)     # Skip headers
        for row in rows:
            route, date, daytype, rides = row[:]
            rides = int(rides)
            record = RowTup(route, date, daytype, rides)
            records.append(record)
    return records


class RowSlots:
    __slots__ = ['route', 'date', 'daytype', 'rides']

    def __init__(self, route, date, daytype, rides):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides


def read_rides_as_class_slots(filename):
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)     # Skip headers
        for row in rows:
            route, date, daytype, rides = row[:]
            rides = int(rides)
            record = RowSlots(route, date, daytype, rides)
            records.append(record)
    return records


# ex2_2
# 1. How many bus routes exist in Chicago?
#    >>> len(set(r['route'] for r in rows))
#    181
# 2. How many people rode the number 22 bus on February 2, 2011?  What about any route on any date of your choosing?
#    >>> sum(r['rides'] for r in rows if r['route'] == '22' and r['date'] == '02/02/2011')
#    5055
# 3. What is the total number of rides taken on each bus route?
#    >>> from collections import Counter
#    >>> c = Counter()
#    >>> for r in rows: c[r['route']] += r['rides']
# 4. What five bus routes had the greatest ten-year increase in ridership from 2001 to 2011?
#    >>> def get_rides_in_year(year):
#    ...     rs = (r for r in rows if r['date'][-4:] == str(year))
#    ...     c = Counter()
#    ...     for r in rs:
#    ...         c[r['route']] += r['rides']
#    ...     return c
#    ...
#    >>> c2001 = get_rides_in_year(2001)
#    >>> c2011 = get_rides_in_year(2011)
#    >>> routes = set(c2001) | set(c2011)
#    >>> growths = [(rt, c2011[rt] - c2001[rt]) for rt in routes]
#    >>> growths.sort(key=lambda x: x[1], reverse=True)
#    >>> growths[:5]  # [(route, increase), (route, increase), ...]
#    [('147', 2107910), ('66', 1612958), ('12', 1612067), ('14', 1351308), ('49', 1183191)]


def read_rides_as_columns(filename):
    '''
    Read the bus ride data into 4 lists, representing columns
    '''
    routes = []
    dates = []
    daytypes = []
    numrides = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)     # Skip headers
        for row in rows:
            routes.append(row[0])
            dates.append(row[1])
            daytypes.append(row[2])
            numrides.append(int(row[3]))
    return dict(routes=routes, dates=dates, daytypes=daytypes, numrides=numrides)


class RideData(Sequence):
    def __init__(self):
        # Columns
        self.routes = []
        self.dates = []
        self.daytypes = []
        self.numrides = []

    def __len__(self):
        # Assume all lists have the same length
        return len(self.routes)

    def __getitem__(self, index):
        match index:
            case int():
                return {
                    'route': self.routes[index],
                    'date': self.dates[index],
                    'daytypes': self.daytypes[index],
                    'numrides': self.numrides[index],
                }
            case slice():
                start = index.start if index.start is not None else 0
                stop = index.stop
                step = index.step if index.step is not None else 1
                return [self[i] for i in range(start, stop, step)]
            case _:
                raise NotImplemented

    def append(self, d):
        self.routes.append(d['route'])
        self.dates.append(d['date'])
        self.daytypes.append(d['daytype'])
        self.numrides.append(d['rides'])


def main22():
    import gc
    import tracemalloc

    read_fns = {
        'tuple': read_rides_as_tuples,
        'dict': read_rides_as_dicts,
        'class': read_rides_as_class,
        'namedtuple': read_rides_as_namedtuple,
        'class_slots': read_rides_as_class_slots,
    }

    for name, fn in read_fns.items():
        tracemalloc.start()
        rows = fn('Data/ctabus.csv')
        print(f'{name} -> Memory Use: Current %d, Peak %d' % tracemalloc.get_traced_memory())
        tracemalloc.stop()
        del rows
        gc.collect()


def main25():
    import gc
    import tracemalloc
    tracemalloc.start()
    columns = read_rides_as_columns('Data/ctabus.csv')
    print('read_rides_as_columns -> Memory Use: Current %d, Peak %d' % tracemalloc.get_traced_memory())
    tracemalloc.stop()
    del columns
    gc.collect()
    tracemalloc.start()
    rows = read_rides_as_dicts('Data/ctabus.csv')
    print('read_rides_as_dicts -> Memory Use: Current %d, Peak %d' % tracemalloc.get_traced_memory())
    tracemalloc.stop()


if __name__ == '__main__':
    #main22()
    main25()