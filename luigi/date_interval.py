import re, datetime

class DateInterval(object):
    def __init__(self, date_a, date_b):
        # Represents all date d such that date_a <= d < date_b
        self.date_a = date_a
        self.date_b = date_b

    def dates(self):
        import datetime
        dates = []
        d = self.date_a
        while d < self.date_b:
            dates.append(d)
            d += datetime.timedelta(1)

        return dates

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.to_string()

    def prev(self): return self.from_date(self.date_a - datetime.timedelta(1))
    def next(self): return self.from_date(self.date_b)

    def to_stringe(self): raise NotImplementedError

    @classmethod
    def from_date(self, d): raise NotImplementedError

    @classmethod
    def parse(self, s): raise NotImplementedError

class Date(DateInterval):
    def __init__(self, y, m, d):
        a = datetime.date(y, m, d)
        b = datetime.date(y, m, d) + datetime.timedelta(1)
        super(Date, self).__init__(a, b)

    def to_string(self):
        return self.date_a.strftime('%Y-%m-%d')

    @classmethod
    def from_date(self, d):
        return Date(d.year, d.month, d.day)

    @classmethod
    def parse(self, s):
        if re.match(r'\d\d\d\d\-\d\d\-\d\d$', s):
            return Date(*map(int, s.split('-')))
        
class Week(DateInterval):
    def __init__(self, y, w):
        # Python datetime does not have a method to convert from ISO weeks!
        for d in xrange(-10, 370):
            date = datetime.date(y, 1, 1) + datetime.timedelta(d)
            if date.isocalendar() == (y, w, 1):
                date_a = date
                break
        else:
            raise ValueError('Invalid week')
        date_b = date_a + datetime.timedelta(7)
        super(Week, self).__init__(date_a, date_b)

    def to_string(self):
        return '%d-W%02d' % self.date_a.isocalendar()[:2]

    @classmethod
    def from_date(self, d):
        return Week(*d.isocalendar()[:2])

    @classmethod
    def parse(self, s):
        if re.match(r'\d\d\d\d\-W\d\d$', s):
            y, w = map(int, s.split('-W'))
            return Week(y, w)

class Month(DateInterval):
    def __init__(self, y, m):
        date_a = datetime.date(y, m, 1)
        date_b = datetime.date(y + m/12, 1 + m%12, 1)
        super(Month, self).__init__(date_a, date_b)

    def to_string(self):
        return self.date_a.strftime('%Y-%m')

    @classmethod
    def from_date(self, d):
        return Month(d.year, d.month)

    @classmethod
    def parse(self, s):
        if re.match(r'\d\d\d\d\-\d\d$', s):
            y, m = map(int, s.split('-'))
            return Month(y, m)
        
class Year(DateInterval):
    def __init__(self, y):
        date_a = datetime.date(y, 1, 1)
        date_b = datetime.date(y + 1, 1, 1)
        super(Year, self).__init__(date_a, date_b)
        
    def to_string(self):
        return self.date_a.strftime('%Y')

    @classmethod
    def from_date(self, d):
        return Year(d.year)

    @classmethod
    def parse(self, s):
        if re.match(r'\d\d\d\d$', s):
            return Year(int(s))

class Custom(DateInterval):
    def to_string(self):
        return '-'.join([d.strftime('%Y-%m-%d') for d in (self.date_a, self.date_b)])

    @classmethod
    def parse(self, s):
        if re.match('\d\d\d\d\-\d\d\-\d\d\-\d\d\d\d\-\d\d\-\d\d$', s):
            # Actually the ISO 8601 specifies <start>/<end> as the time interval format
            # Not sure if this goes for date intervals as well. In any case slashes will
            # most likely cause problems with paths etc.
            x = map(int, s.split('-'))
            date_a = datetime.date(*x[:3])
            date_b = datetime.date(*x[3:])
            return Custom(date_a, date_b)

