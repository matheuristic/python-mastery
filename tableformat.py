from abc import ABC, abstractmethod


def print_table_ex3_2(objs, attrs):
    formatstr = ' '.join(['{:>10s}'] * len(attrs))
    divider = ' '.join(['{:->10s}'.format('')] * len(attrs))
    print(formatstr.format(*attrs))
    print(divider)
    for o in objs:
        print(formatstr.format(*[str(getattr(o, attr)) for attr in attrs]))


class TableFormatter(ABC):
    @abstractmethod
    def headings(self, headers):
        raise NotImplementedError()

    @abstractmethod
    def row(self, rowdata):
        raise NotImplementedError()


def print_table(records, fields, formatter):
    if not isinstance(formatter, TableFormatter):
        raise TypeError('Expected a TableFormatter')
    formatter.headings(fields)
    for r in records:
        rowdata = [getattr(r, fieldname) for fieldname in fields]
        formatter.row(rowdata)


class TextTableFormatter(TableFormatter):
    def headings(self, headers):
        print(' '.join('%10s' % h for h in headers))
        print(' '.join(['-'*10] * len(headers)))

    def row(self, rowdata):
        print(' '.join('%10s' % d for d in rowdata))


class CSVTableFormatter(TableFormatter):
    @staticmethod
    def clean(val):
        textval = str(val)
        if '"' in textval:
            textval = textval.replace('"', '""')
        if ',' in textval:
            textval = '"' + textval + '"'
        return textval

    def headings(self, headers):
        print(','.join(CSVTableFormatter.clean(h) for h in headers))

    def row(self, rowdata):
        self.headings(rowdata)


class HTMLTableFormatter(TableFormatter):
    def headings(self, headers):
        tokens = ['<tr>'] + ['<th>' + str(h) + '</th>' for h in headers] + ['</tr>']
        print(' '.join(tokens))

    def row(self, rowdata):
        tokens = ['<tr>'] + ['<td>' + str(r) + '</td>' for r in rowdata] + ['</tr>']
        print(' '.join(tokens))


def create_formatter_old(formatname):
    match formatname:
        case 'text':
            return TextTableFormatter()
        case 'csv':
            return CSVTableFormatter()
        case 'html':
            return HTMLTableFormatter()
        case _:
            raise ValueError(f'No formatter for format name {formatname}')


class ColumnFormatMixin:
    formats = []
    def row(self, rowdata):
        rowdata = [(fmt % d) for fmt, d in zip(self.formats, rowdata)]
        super().row(rowdata)

class UpperHeadersMixin:
    def headings(self, headers):
        super().headings([h.upper() for h in headers])


def create_formatter(formatname, upper_headers=False, column_formats=None):
    cls = None
    match formatname:
        case 'text':
            cls = TextTableFormatter
        case 'csv':
            cls = CSVTableFormatter
        case 'html':
            cls = HTMLTableFormatter
        case _:
            raise ValueError(f'No formatter for format name {formatname}')

    if upper_headers:
        class cls(UpperHeadersMixin, cls):
            pass

    if column_formats is not None:
        class cls(ColumnFormatMixin, cls):
            formats = column_formats

    return cls()
