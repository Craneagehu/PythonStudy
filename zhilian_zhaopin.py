import requests
import json

url = 'https://fe-api.zhaopin.com/c/i/similar-positions?number=CC340479015J00219702502'
# url_set = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
}


# 递归获取所有的api
def iter_url(urls):
    resp = requests.get(url=urls, headers=headers).text
    #number,职位，公司都在一个list下面，用json.loads获取到
    complex_lists = json.loads(resp)['data']['data']['list']
    #从list里面迭代找我们要的职位url和number
    for complex_list in complex_lists:
        # url_set.append(complex_list['positionURL'])
        # 这里url_set原本打算用set去重复的，先用str方便存入excel把
        url_set = ''.join(complex_list['positionURL'])
        number = ''.join(complex_list['number'])
        resp = requests.get('https://fe-api.zhaopin.com/c/i/similar-positions?number={0}'.format(number),
                            headers=headers)
        print(url_set)
        iter_url(resp.url)


iter_url(url)
