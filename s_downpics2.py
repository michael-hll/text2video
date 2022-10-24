import requests
import sys,os
from s_utility import Utility

# inputs: keyfile, keywords, [count=50], [outdir], [pic_name=bg{:02d}.jpg]
# outputs: ./tmp2

key_file = './d_apikeys.yaml'
keywords = 'microsoft apple'
count = 5
out_dir = './tmp2'
pic_name = 'img{:02d}.jpg'
if len(sys.argv) >= 3:
    key_file = sys.argv[1]
    keywords = sys.argv[2]
if len(sys.argv) >=4:
    count = int(sys.argv[3])
if len(sys.argv) >=5:
    out_dir = sys.argv[4]
if len(sys.argv) >=6:
    pic_name = sys.argv[5]

API_KEY = 'MICROSOFTY_API_KEY'

# https://portal.azure.com/?quickstart=true#home
# Advanced search keywords: https://support.microsoft.com/en-us/topic/advanced-search-keywords-ea595928-5d63-4a0b-9c6b-0b769865e78a
def search_image_by_keyword(keyword):
    subscription_key=Utility.get_api_key(key_file, API_KEY)
    search_url = "https://api.bing.microsoft.com/v7.0/images/search"
    search_term = keyword
    headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
    params  = {"q": search_term}

    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    if search_results:
        return search_results['value']
    else:
        return None

keywords = keywords.split(' ')
# download photos by keywords
i = 0
for j, key in enumerate(keywords):
    keyword_count = 0
    print('Searching with keyword: ' + key)
    for pic in search_image_by_keyword(key):  
        url = pic['contentUrl']
        width = pic['width']
        height = pic['height']
        if not int(pic['contentSize'].strip('B').strip()) > 0:
            continue
        print('Downloading: {0}'.format(url))
        try:
            r = requests.get(url, verify=False, timeout=3)
            with open(os.path.join(out_dir, pic_name.format(i)), 'wb') as f:
                f.write(r.content)
            i += 1
            keyword_count += 1
            if keyword_count >= count:
                break
        except Exception as e:
            print('Download picture fail:' + str(e))

''' resonpnse data format
{
  '_type': 'Images',
  'instrumentation': {
    '_type': 'ResponseInstrumentation'
  },
  'readLink': 'https://api.bing.microsoft.com/api/v7/images/search?q=puppies',
  'webSearchUrl': 'https://www.bing.com/images/search?q=puppies&FORM=OIIARP',
  'queryContext': {
    'originalQuery': 'puppies',
    'alterationDisplayQuery': 'puppies',
    'alterationOverrideQuery': '+puppies',
    'alterationMethod': 'AM_JustChangeIt',
    'alterationType': 'CombinedAlterationsChained'
  },
  'totalEstimatedMatches': 787,
  'nextOffset': 41,
  'currentOffset': 0,
  'value': [
    {
      'webSearchUrl': 'https://www.bing.com/images/search?view=detailv2&FORM=OIIRPO&q=puppies&id=9BFDBE19EB3643615F0D5B5575BD0331CA6F744F&simid=608030995802948338',
      'name': 'Three Assorted-colored Puppies · Free Stock Photo',
      'thumbnailUrl': 'https://tse4.explicit.bing.net/th?id=OIP.i7WwbKxcrvHlc_8qngEsxgHaE8&pid=Api',
      'datePublished': '2020-04-14T15:40:00.0000000Z',
      'isFamilyFriendly': False,
      'creativeCommons': 'PublicNoRightsReserved',
      'contentUrl': 'https://images.pexels.com/photos/3198019/pexels-photo-3198019.jpeg?cs=srgb&dl=three-assorted-colored-puppies-3198019.jpg&fm=jpg',
      'hostPageUrl': 'https://www.pexels.com/photo/three-assorted-colored-puppies-3198019/',
      'contentSize': '1543085 B',
      'encodingFormat': 'jpeg',
      'hostPageDisplayUrl': 'https://www.pexels.com/photo/three-assorted-colored-puppies-3198019',
      'width': 5472,
      'height': 3648,
      'hostPageFavIconUrl': 'https://www.bing.com/th?id=ODF.OTWJk1xWx9LlWBdoF478uA&pid=Api',
      'hostPageDomainFriendlyName': 'Pexels',
      'hostPageDiscoveredDate': '2019-11-24T00:00:00.0000000Z',
      'thumbnail': {
        'width': 474,
        'height': 316
      },
      'imageInsightsToken': 'ccid_i7WwbKxc*cp_818F4E303E2C3FDA78C238444D1DC0ED*mid_9BFDBE19EB3643615F0D5B5575BD0331CA6F744F*simid_608030995802948338*thid_OIP.i7WwbKxcrvHlc!_8qngEsxgHaE8',
      'insightsMetadata': {
        'pagesIncludingCount': 10,
        'availableSizesCount': 8
      },
      'imageId': '9BFDBE19EB3643615F0D5B5575BD0331CA6F744F',
      'accentColor': '8E5B3D'
    },
}
'''