import requests
import datetime
from bs4 import BeautifulSoup

APIUrl = 'http://www.erumy.com/free/todayFortuneReport.aspx'


class Fortune:

    def make_dict(self, soup):
        tmpres = str(soup.select('label > ul')[0])
        today_fortune = tmpres[4:-5]
        tmpres = soup.select('div > font > label')[0]
        today = tmpres.get_text('label')
        return {'Fortune': today_fortune, 'day': today}

    def today_tell(self, birth):
        func_url = APIUrl + '?m=dummy&uday=' + birth + '&lunar=1'
        r = requests.get(func_url, auth=('user', 'pass'))
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        return self.make_dict(soup)

    def tomorrow_tell(self, birth):
        now = datetime.date.today()
        now = now + datetime.timedelta(days=1)
        tomorrow = '{0:02d}{1:02d}{2:02d}'.format(now.year, now.month, now.day)
        func_url = APIUrl + '?m=dummy&uday=' + birth + '&lunar=1' + '&NextDay=T&tday=' + tomorrow
        r = requests.get(func_url, auth=('user', 'pass'))
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        return self.make_dict(soup)

    def someday_tell(self, birth, inputday):
        func_url = APIUrl + '?m=dummy&uday=' + birth + '&lunar=1' + '&NextDay=T&tday=' + inputday
        r = requests.get(func_url, auth=('user', 'pass'))
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        return self.make_dict(soup)
