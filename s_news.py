import requests
import sys

'''
    args:
        api_key: str # news api key  
        file: str    # save result to file
'''

news_api_key = '<key>'
file = 'd_news.txt'
if len(sys.argv) > 1:
    news_api_key = sys.argv[1]
if len(sys.argv) > 2:
    file = sys.argv[2]
url =  'https://newsapi.org/v2/top-headlines?country=cn&apiKey={0}'.format(news_api_key)
if __name__ == '__main__':
    news = requests.get(url).json()
    '''
    {
        "status": "ok",
        "totalResults": 0,
        "articles": [
            {
            "title": "英镑、英债暴涨，报道称英国官员在设法逆转首相特拉斯的减税计划 - 华尔街见闻",
            "author": null,
            "source": {
                "Id": null,
                "Name": "Wallstreetcn.com"
            },
            "publishedAt": "2022-10-13T11:48:31Z",
            "url": "https://wallstreetcn.com/articles/3672304"
            },
            ...
    }
    '''
    articles = news['articles']
    with open(file, 'w') as f:
        result = ''
        for i, article in enumerate(articles):
            title = article['title'].replace('Sina', '新浪').replace('- VOA Mandarin', '').replace('- People', '').replace('','')
            title = title.replace('"', '\\"').replace(':', '\\:').replace(',', '\\,')
            print(title)
            result += ('{0}. ' + title + '   ').format(i+1)
        f.write(result)