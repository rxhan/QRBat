import datetime
import re
import enum

class checker():
    ProductionDateDay = {'0':0, '1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9,
                         'A':10, 'B':11, 'C':12, 'D':13, 'E':14, 'F':15, 'G':16, 'H':17, 'I':None,
                         'J':18, 'K':19, 'L':20, 'M':21, 'N':22, 'O':None, 'P':23, 'Q':None, 'R':24,
                         'S':25, 'T':26, 'U':None, 'V':27, 'W':28, 'X':29, 'Y':30, 'Z':31}
    def __init__(self, code, nr=None):
        self._vendor = None
        self._production_type = None
        self._cell_type = None
        self._model_code = None
        self._factory_trace_code = None
        self._factory_address = None
        self._production_date = None
        self._serialnumber = None
        self._code = None
        self._capacity = None
        self.nr = nr

        self.code = code.upper()

    def get_code(self):
        return self._code

    def set_code(self, value):
        if len(value) != 24:
            raise Exception(f'input length of QR-Code not equal 24 ({len(value)})')

        self.vendor = value[0:3]
        self.production_type = value[3:4]
        self.cell_type = value[4:5]
        self.model_code = value[5:7]
        self.factory_trace_code = value[7:13]
        self.factory_address = value[13:14]
        self.production_date = value[14:17]
        self.serialnumber = value[17:24]

        self._code = value

    code = property(get_code, set_code)

    def get_vendor(self):
        return self._vendor

    def set_vendor(self, value):
        if value == '04Q':
            self._vendor = 'EVE Power'
        elif value == '02Y':
            self._vendor = 'EVE'
        elif value == '001':
            self._vendor = 'CATL'
        elif value == '08B':
            self._vendor = 'LiShen'
        elif value == '081':
            self._vendor = 'REPT'
        elif value == '0B5':
            self._vendor = 'CALB'
        elif value == '0AL':
            self._vendor = 'Ganfeng'
        else:
            raise Exception(f'Vendor unknown: {value}')

    vendor = property(get_vendor, set_vendor)

    def get_production_type(self):
        return self._production_type

    def set_production_type(self, value):
        if value == 'C':
            self._production_type = 'Cell'
        elif value == 'P':
            self._production_type = 'Battery Pack'
        elif value == 'M':
            self._production_type = 'Battery Module'
        else:
            raise Exception(f'Production Type unknown: {value}')

    production_type = property(get_production_type, set_production_type)

    def get_cell_type(self):
        return self._cell_type

    def set_cell_type(self, value):
        if value == 'B':
            self._cell_type = 'LiFePO4'
        else:
            raise Exception(f'Cell Type unknown: {value}')

    cell_type = property(get_cell_type, set_cell_type)

    def get_capacity(self):
        return self._capacity

    def set_capacity(self, value: int):
        self._capacity = value

    capacity = property(get_capacity, set_capacity)

    def get_model_code(self):
        return self._model_code

    def set_model_code(self, value):
        if value == '76':
            self._model_code = 'LF280K'
            self.capacity = 280
        elif value == '71':
            self._model_code = 'LF280N'
            self.capacity = 280
        elif value == '72':
            self._model_code = 'LF230'
            self.capacity = 230
        elif value == '73':
            self._model_code = 'LF304'
            self.capacity = 304
        elif value == '75':
            self._model_code = 'LF105'
            self.capacity = 105
        elif value == '66':
            self._model_code = 'LF280'
            self.capacity = 280
        elif value == '68':
            self._model_code = 'LF50K'
            self.capacity = 50
        elif value == '24': # Only CATL?
            self._model_code = 'unknown'
            self.capacity = 302
        elif value == 'PB': # Only Lishen?
            self._model_code = 'unknown'
            self._capacity = 272
        else:
            raise Exception(f'Model Code unknown: {value}')

    model_code = property(get_model_code, set_model_code)

    def get_factory_trace_code(self):
        return self._factory_trace_code

    def set_factory_trace_code(self, value):
        tracecode = list()
        tracecode.append(f'Traceablity code {value[0:2]}')
        tracecode.append(f'Production Line {value[2:4]}')
        tracecode.append(f'Task order {value[4:6]}')

        self._factory_trace_code = ','.join(tracecode)

    factory_trace_code = property(get_factory_trace_code, set_factory_trace_code)

    def get_factory_address(self):
        return self._factory_address

    def set_factory_address(self, value):
        if value == 'J':
            self._factory_address = 'Jingmen'
        elif value == 'H':
            self._factory_address = 'Huizhou'
        elif value == '3': # CATL
            self._factory_address = 'unknown'
        elif value == '1':  # LiShen
            self._factory_address = 'unknown'
        else:
            raise Exception(f'Factory Address unknown: {value}')

    factory_address = property(get_factory_address, set_factory_address)

    def get_production_date_str(self):
        return self._production_date.strftime('%Y-%m-%d')

    production_date_str = property(get_production_date_str,)

    def get_production_date(self):
        return self._production_date

    def set_production_date(self, value):
        year = value[0:1].upper()
        if re.match('[A-Z]', year):
            year = 1955 + ord(year)
        elif re.match('[0-9]', year):
            year = 2010 + int(year)
        else:
            raise Exception(f'Year in production Date not readable: {year}')

        month = value[1:2]
        if re.match('[A-Z]', month):
            month = -55 + ord(month)
        elif re.match('[1-9]', month):
            month = int(month)
        else:
            raise Exception(f'Month in production Date not readable: {month}')

        day = value[2:3]
        if re.match(r'[\dA-Z]', day):
            calc_day = self.ProductionDateDay[day.upper()]
            if calc_day is None:
                raise Exception(f'Day in production Date not readable: {day} result: {calc_day}')
            day = calc_day
        else:
            raise Exception(f'Day in production Date not readable: {day}')

        try:
            self._production_date = datetime.datetime.strptime(f'{year}{str(month).zfill(2)}{str(day).zfill(2)}', '%Y%m%d')
        except Exception as e:
            raise Exception(f'Error in production Date: {e}')

    production_date = property(get_production_date, set_production_date)

    def get_serialnumber(self):
        return self._serialnumber

    def set_serialnumber(self, value):
        try:
            self._serialnumber = int(value)
        except Exception as e:
            raise Exception(f'Error in serialnumber: {e}')

    serialnumber = property(get_serialnumber, set_serialnumber)

    def __str__(self):
        return f'{self.code} - {self.vendor} - {self.production_type} - {self.cell_type} - {self.model_code} - {self.capacity} - {self.factory_trace_code} - {self.factory_address} - {self._production_date.strftime("%Y-%m-%d")} - S/N: {self._serialnumber}'

    def result(self):
        return {
                'code': self.code,
                'vendor': self.vendor,
                'production_type': self.production_type,
                'cell_type': self.cell_type,
                'model_code': self.model_code,
                'capacity': self.capacity,
                'factory_trace_code': self.factory_trace_code,
                'factory_address': self.factory_address,
                'production_date': self.production_date.strptime('%Y-%m-%d'),
                'serialnumber': self.serialnumber
                }
