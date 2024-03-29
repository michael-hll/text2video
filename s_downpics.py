from pypexels import PyPexels
from s_utility import Utility
import requests, sys, os
import shutil
import time

def __pexels_api_description():
    #GET https://api.pexels.com/v1/search
    # query string | required
    # The search query. Ocean, Tigers, Pears, etc.

    # orientation string | optional
    # Desired photo orientation. The current supported orientations are: landscape, portrait or square.

    # size string | optional
    # Minimum photo size. The current supported sizes are: large(24MP), medium(12MP) or small(4MP).

    # color string | optional
    # Desired photo color. Supported colors: red, orange, yellow, green, turquoise, blue, violet, pink, brown, black, gray, white or any hexidecimal color code (eg. #ffffff).

    # locale string | optional
    # The locale of the search you are performing. The current supported locales are: 'en-US' 'pt-BR' 'es-ES' 'ca-ES' 'de-DE' 'it-IT' 'fr-FR' 'sv-SE' 'id-ID' 'pl-PL' 'ja-JP' 'zh-TW' 'zh-CN' 'ko-KR' 'th-TH' 'nl-NL' 'hu-HU' 'vi-VN' 'cs-CZ' 'da-DK' 'fi-FI' 'uk-UA' 'el-GR' 'ro-RO' 'nb-NO' 'sk-SK' 'tr-TR' 'ru-RU'.

    # page integer | optional
    # The page number you are requesting. Default: 1

    # per_page integer | optional
    # The number of results you are requesting per page. Default: 15 Max: 80
    
    #Do not abuse the API. By default, the API is rate-limited to 200 requests per hour 
    # and 20,000 requests per month. You may contact us to request a higher limit, but please include examples, 
    # or be prepared to give a demo, that clearly shows your use of the API with attribution. 
    # If you meet our API terms, you can get unlimited requests for free.
    pass

'''
Description: Download pictures from Pexels api
    Arg 1: Key file full path
    Arg 2: Searching keywords
    Arg 3: Numbers of downloading picturs count
    Arg 4: Output directory
    Arg 5: Picture name format eg: bg{:02d}.jpg
'''

key_file = './t_apikeys.yaml'
keywords = '英雄联盟 match scout CNMO League of Legends'
count = 15
out_dir = './tmp'
pic_name = 'bg{:02d}.jpg'
if len(sys.argv) >= 3:
    key_file = sys.argv[1]
    keywords = sys.argv[2]
if len(sys.argv) >=4:
    count = int(sys.argv[3])
if len(sys.argv) >=5:
    out_dir = sys.argv[4]
if len(sys.argv) >=6:
    pic_name = sys.argv[5]

# instantiate PyPexels object
py_pexel = PyPexels(api_key=Utility.get_api_key(key_file, 'PEXELS_API_KEY'))
search_pics_response = py_pexel.search(query=keywords, orientation='landscape', per_page=count)

# download photos by keywords
i = 0
for pic in search_pics_response.body['photos']:    
    url = pic['src']['original']
    width = pic['width']
    height = pic['height']
    if width < height:
        continue
    print('Downloading: {0}'.format(url))
    try:
        r = requests.get(url)
        with open(os.path.join(out_dir, pic_name.format(i)), 'wb') as default_f:
            default_f.write(r.content)
            i += 1
    except Exception as e:
        print('Download picture fail:' + str(e))
        
# check default photos     
default_dir = out_dir + '/default-bg'
j = 0
for filename in os.listdir(default_dir):
    
    if not filename.endswith('png'):
        continue
    
    # get the default pic file name
    default_f = os.path.join(default_dir, filename)    
    
    # get the target need to be replaced file name
    target_f = os.path.join(out_dir + '/' + pic_name.format(j))
    
    # move the target file to new    
    target_f_new = os.path.join(out_dir + '/' + pic_name.format(i))
    if(os.path.exists(target_f)):
        if(os.path.exists(target_f_new)):
            os.remove(target_f_new)
        shutil.move(target_f, target_f_new)
        i += 1
    
    # replace the target file with default background    
    if(os.path.exists(target_f)):
        os.remove(target_f)  
    shutil.copy(default_f, target_f)
    j += 1
 
  
