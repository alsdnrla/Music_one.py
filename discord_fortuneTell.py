import erumyFortune
import datetime
import requests

def out(args):
    res_str = '```css\n'
    birth = args[0]
    if len(args) > 1:
        para = args[1]
    else:
        para = '오늘'

    if para == '오늘':
        data = f.today_tell(birth)
    elif para == '내일':
        data = f.tomorrow_tell(birth)
    else:
        todayob = datetime.datetime.today()
        tyear = str(todayob.year)
        para = tyear + para
        try:
            data = f.someday_tell(birth, para)
        except requests.exceptions.RequestException:
            return '올바른 날짜를 입력해주세요.'
    res_str += '[{} 당신의 운세]\n'.format(data['day'])
    res_str += '{}\n'.format(data['Fortune'])
    res_str += '```'
    return res_str


f = erumyFortune.Fortune()
