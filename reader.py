from abc import ABC, abstractmethod
from collections.abc import Sequence
import csv
import logging  # ex5_5

from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence, Union

def read_csv_as_dicts_old(filename: List[str], convertfns: List[Callable]) -> List[Dict[str,Any]]:
    rows = []
    with open(filename, 'r') as f:
        rs = csv.reader(f)
        headers = next(rs)
        for r in rs:
            vals = (f(v) for f, v in zip(convertfns, r))
            d = {k: v for k, v in zip(headers, vals)}
            rows.append(d)
    return rows


class DataCollection(Sequence):
    def __init__(self, headers: List[str], dtypes: List[Callable]):
        assert len(headers) == len(dtypes), "DataCollection.__init__: len(headers) != len(dtypes)"
        self.headers = headers
        self.dtypes = dtypes
        self.columns = {k: [] for k in headers}

    def __len__(self):
        # Assume all columns are same length
        return len(self.columns[self.headers[0]])

    def append(self, row: Sequence):
        for k, f, v in zip(self.headers, self.dtypes, row):
            self.columns[k].append(f(v))

    def __getitem__(self, i: Any) -> Union[Dict[int,Any],List[Dict[int,Any]]]:
        match i:
            case int():
                return {k: self.columns[k][i] for k in self.headers}
            case slice():
                start = i.start if i.start is not None else 0
                stop = i.stop
                step = i.step if i.step is not None else 1
                return [self[ii] for ii in range(start, stop, step)]
            case _:
                return NotImplemented


def read_csv_as_columns(filename: str, types: List[Callable]) -> Dict[str,List[Any]]:
    rows = None
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = DataCollection(headers, types)
        for row in reader:
            rows.append(row)
    return rows


def read_csv_as_instances_old(filename: str, cls: Any) -> List[Any]:
    '''
    Read a CSV file into a list of instances
    '''
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)
        for row in rows:
            records.append(cls.from_row(row))
    return records


class CSVParser(ABC):
    def parse(self, filename: str) -> List[Any]:
        records = []
        with open(filename) as f:
            rows = csv.reader(f)
            headers = next(rows)
            for row in rows:
                record = self.make_record(headers, row)
                records.append(record)
        return records

    @abstractmethod
    def make_record(self, headers: List[str], row: List[str]) -> Any:
        pass


class DictCSVParser(CSVParser):
    def __init__(self, types: List[Callable]):
        self.types = types

    def make_record(self, headers: List[str], row: List[str]) -> Dict[str,Any]:
        return { name: func(val) for name, func, val in zip(headers, self.types, row) }


class InstanceCSVParser(CSVParser):
    def __init__(self, cls: Any):
        self.cls = cls

    def make_record(self, headers: List[str], row: List[str]) -> Any:
        return self.cls.from_row(row)


def read_csv_as_dicts_ex3_7(filename: str, types: List[Callable]) -> List[Dict[str,Any]]:
    parser = DictCSVParser(types)
    portfolio = parser.parse(filename)
    return portfolio


def read_csv_as_instances_ex3_7(filename: str, cls: Any) -> List[Any]:
    parser = InstanceCSVParser(cls)
    portfolio = parser.parse(filename)
    return portfolio

def read_csv_as_dicts(filename: str, types: List[Callable], *, headers: Optional[List[str]]=None) -> List[Dict[str,Any]]:
    '''
    Read CSV data into a list of dictionaries with optional type conversion
    '''
    with open(filename, 'r') as file:
        return csv_as_dicts(file, types, headers=headers)
    
def read_csv_as_instances(filename: str, cls: Any, *, headers: Optional[List[str]]=None) -> List[Any]:
    '''
    Read CSV data into a list of instances
    '''
    with open(filename, 'r') as file:
        return csv_as_instances(file, cls, headers=headers)
    
def csv_as_dicts_ex5_2(lines: Iterable, types: List[Callable], *, headers: Optional[List[str]]=None) -> List[Dict[str,Any]]:
    rows = csv.reader(lines)
    records = []
    if headers is None:
        headers = next(rows)
    for row in rows:
        record = { name:func(val) for name, func, val in zip(headers, types, row) }
        records.append(record)
    return records
    
def csv_as_instances_ex5_2(lines: Iterable, cls: Any, *, headers: Optional[List[str]]=None):
    rows = csv.reader(lines)
    records = []
    if headers is None:
        _ = next(rows)  # no need for headers
    for row in rows:
        record = cls.from_row(row)
        records.append(record)
    return records
    
# ex5_3

def convert_csv_nomap(lines, convertfn, *, headers=None):
    rows = csv.reader(lines)
    records = []
    if headers is None:
        headers = next(rows)
    for row in rows:
        record = convertfn(headers, row)
        records.append(record)
    return records
    
def csv_as_dicts(lines: Iterable, types: List[Callable], *, headers: Optional[List[str]]=None) -> List[Dict[str,Any]]:
    
    def convertfn(headers, row):
        return { name:func(val) for name, func, val in zip(headers, types, row) }

    return convert_csv(lines, convertfn, headers=headers)
    
def csv_as_instances(lines: Iterable, cls: Any, *, headers: Optional[List[str]]=None):
    
    def convertfn(headers, row):
        return cls.from_row(row)
        
    return convert_csv(lines, convertfn, headers=headers)
    
def convert_csv_map(lines, convertfn, *, headers=None):
    rows = csv.reader(lines)
    records = []
    if headers is None:
        headers = next(rows)
    records = list(
        map(lambda x: convertfn(headers, x), rows)
    )
    return records

# ex5_5

def convert_csv_try_except(lines, convertfn, *, headers=None):
    rows = csv.reader(lines)
    records = []
    for k, row in enumerate(rows):
        if headers is None:
            headers = row
        else:
            try:
                record = convertfn(headers, row)
                records.append(record)
            except:
                print(f'Row {k}: Bad row: {row}')
    return records


logger = logging.getLogger('reader')
    

def convert_csv(lines, convertfn, *, headers=None):
    rows = csv.reader(lines)
    records = []
    for k, row in enumerate(rows):
        if headers is None:
            headers = row
        else:
            try:
                record = convertfn(headers, row)
                records.append(record)
            except Exception as e:
                logger.warning(f'Row {k}: Bad row: {row}')
                logger.debug(str(e))
    return records
