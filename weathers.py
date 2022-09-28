import json
import urllib.request
import sys

file_name = 'weathers.txt'
if len(sys.argv) >= 2:
    file_name = sys.argv[1]

# 北上广深
cityList_bsgs = [
    {'code': "101010100", 'name': "北京", 'name_en': "Beijing"},
    {'code': "101020100", 'name': "上海", 'name_en': "Shanghai"},
    {'code': "101280101", 'name': "广州", 'name_en': "Guangzhou"},
    {'code': "101280601", 'name': "深圳", 'name_en': "Shenzhen"}
]

def getCityWeather_RealTime(cityID):
    url = "http://www.weather.com.cn/data/sk/" + str(cityID) + ".html"
    try:
        stdout = urllib.request.urlopen(url)
        weatherInfomation = stdout.read().decode('utf-8')

        jsonDatas = json.loads(weatherInfomation)

        city = jsonDatas["weatherinfo"]["city"]
        temp = jsonDatas["weatherinfo"]["temp"]
        fx = jsonDatas["weatherinfo"]["WD"]  # 风向
        fl = jsonDatas["weatherinfo"]["WS"]  # 风力
        sd = jsonDatas["weatherinfo"]["SD"]  # 相对湿度
        tm = jsonDatas["weatherinfo"]["time"]

        content = "#" + city + "#" + " " + temp + "℃ " + \
            fx + fl + " " + "相对湿度" + sd + " " + "发布时间:" + tm
        twitter = {'image': "", 'message': content}

    except (SyntaxError) as err:
        print(">>>>>> SyntaxError: " + err.args)
    except:
        print(">>>>>> OtherError: ")
    else:
        return twitter
    finally:
        None

def getCityWeather_AllDay(cityID):
    url = "http://www.weather.com.cn/data/cityinfo/" + str(cityID) + ".html"
    try:
        stdout = urllib.request.urlopen(url)
        weatherInfomation = stdout.read().decode('utf-8')
        jsonDatas = json.loads(weatherInfomation)

        city        = jsonDatas["weatherinfo"]["city"]
        temp1       = jsonDatas["weatherinfo"]["temp1"]
        temp2       = jsonDatas["weatherinfo"]["temp2"]
        weather     = jsonDatas["weatherinfo"]["weather"]
        img1        = jsonDatas["weatherinfo"]["img1"]
        img2        = jsonDatas["weatherinfo"]["img2"]
        ptime        = jsonDatas["weatherinfo"]["ptime"]

        content = city + "," + weather + ",最高气温:" + temp2 + ",最低气温:"  + temp1 + ",发布时间:" + ptime
        twitter = {'image': "icon\d" + img1, 'message': content}

    except (SyntaxError) as err:
        print(">>>>>> SyntaxError: " + err.args)
    except:
        print(">>>>>> OtherError: ")
    else:
        return twitter
    finally:
        None

with open(file_name, 'w') as f:
    for item in cityList_bsgs:
        #print(getCityWeather_RealTime(item['code'])['message'])
        line = item['name_en'] + '=' + getCityWeather_AllDay(item['code'])['message'].replace(':', '\\:') + '\n'
        f.write(line)
