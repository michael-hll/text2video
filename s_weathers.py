import requests
from datetime import datetime
import locale
import sys
import random

'''
    args:
        api_key: str # hefeng api key
        cities: str  # comma seperated city/location list        
        file: str    # save result to file
        count: int   # how many cities you want to show (1~30)
'''

hf_api_key = '<API KEY>'
cities = '北京,上海,深圳'
cities2 = '重庆,长春,呼和浩特,乌鲁木齐,西宁,银川,济南,合肥,武汉,成都,昆明,拉萨,南昌,福州,海口,澳门,天津,哈尔滨,沈阳,石家庄,兰州,西安,郑州,太原,长沙,南京,贵阳,南宁,杭州,广州,台北,香港'

weather_file = 'd_weathers.txt'
city_count = 10

argv_count = len(sys.argv)

class Weather(object):
    
    def __init__(self) -> None:
        self.update_time = None
        self.today = None

class HefengWeather(object):
    
    location_url = 'https://geoapi.qweather.com/v2/city/lookup?key={0}&location={1}'
    weather_url = 'https://devapi.qweather.com/v7/weather/3d?key={0}&location={1}&lang=zh'

    requests = requests
    today = datetime.today().day
    weekday = datetime.today().weekday()
    week = {0:"星期一",1:"星期二",2:"星期三",3:"星期四",4:"星期五",5:"星期六",6:"星期天"}

    def __getday(self)->str:
        day = str(self.today)+"日"+self.week.get(self.weekday)
        return day

    def get_location_info(self, location: str):
        url = self.location_url.format(hf_api_key, location)        
        '''
        "code": "200",
        "location": [
            {
            "name": "上海",
            "id": "101020100",
            "lat": "31.23170",
            "lon": "121.47264",
            "adm2": "上海",
            "adm1": "上海市",
            "country": "中国",
            "tz": "Asia/Shanghai",
            "utcOffset": "+08:00",
            "isDst": "0",
            "type": "city",
            "rank": "11",
            "fxLink": "http://hfx.link/2bc1"
            },
        '''
        l = requests.get(url).json()
        if l['code'] == '200':
            return l['location'][0]
        else:
            return None
    
    def get_weather_by_location_id(self, location_id: str):
        url = self.weather_url.format(hf_api_key, location_id)
        w = requests.get(url).json()
        '''
        weather return format:
            'code': '200',
            'updateTime': '2022-09-30T09:35+08:00',
            'fxLink': 'http://hfx.link/2bc1',
            'daily': [
                {
                'fxDate': '2022-09-30',
                'sunrise': '05:47',
                'sunset': '17:42',
                'moonrise': '09:59',
                'moonset': '20:27',
                'moonPhase': '峨眉月',
                'moonPhaseIcon': '801',
                'tempMax': '27',
                'tempMin': '24',
                'iconDay': '101',
                'textDay': '多云',
                'iconNight': '151',
                'textNight': '多云',
                'wind360Day': '135',
                'windDirDay': '东南风',
                'windScaleDay': '3-4',
                'windSpeedDay': '16',
                'wind360Night': '135',
                'windDirNight': '东南风',
                'windScaleNight': '1-2',
                'windSpeedNight': '3',
                'humidity': '96',
                'precip': '0.0',
                'pressure': '1013',
                'vis': '25',
                'cloud': '25',
                'uvIndex': '2'
                },
        '''

        if w['code'] == '200':
            weather = Weather()
            weather.update_time = w['updateTime']
            weather.today = w['daily'][0]
            return weather
        else:
            return None        
        
if __name__ == '__main__':    
    
    try:
        # deal with user inputs
        if argv_count >= 2:
            hf_api_key = sys.argv[1]
        if argv_count >= 3:
            cities = sys.argv[2]
        if argv_count >= 4:
            weather_file = sys.argv[3]
        if argv_count >= 5:
            city_count = int(sys.argv[4])
        
        # get weather by location list
        weather = HefengWeather()    
        city_list = cities.split(',')
        whole_list = random.sample(cities2.split(','),city_count)
        others_set = set()
        for city in whole_list:
            others_set.add(city)
        whole_list = list(others_set)
        whole_list.extend(city_list)
        print(whole_list)
        locale.setlocale(locale.LC_TIME, "zh_CN")
        out = ''
        for city in whole_list:
            try:
                city_detail = weather.get_location_info(city)
                w_detail = weather.get_weather_by_location_id(city_detail['id'])
                if len(out) == 0:
                    date_time_obj = datetime.now()
                    out = '[' + date_time_obj.strftime('%Y年%b月%d日 %A').replace(' ', '') + ']'
                out += ' ' + city_detail['name'] + ': ' + w_detail.today['tempMin'] + '-' + w_detail.today['tempMax'] + '℃  ' +  w_detail.today['textDay'] + ' ' + w_detail.today['windDirDay'] + ' ' + w_detail.today['windScaleDay'] + '级;'
            except Exception as e:
                print("ERROR: " + str(e))
        with open(weather_file, 'w') as f:
            f.write('weathers=' + out.replace(':', '\\:'))
    except Exception as e:
        print("ERROR: " + str(e))
        
        