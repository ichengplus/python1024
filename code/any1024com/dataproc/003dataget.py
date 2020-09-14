import hashlib
import urllib
import requests

# 获取地图门店

KEY = '<YOUR KEY>'
SK_SIGN = '<YOUR SECRET KEY>'
url_tpl = 'https://apis.map.qq.com/ws/place/v1/search?boundary=region({region},0)&key={key}&keyword={kw}'
url = url_tpl.format(kw='喜茶', region='上海', key=KEY)
url_parse = urllib.parse.urlparse(url)
url_path = f'{url_parse.path}?{url_parse.query}'
print(url_path)
sign = hashlib.md5(f'{url_path}{SK_SIGN}'.encode('utf-8')).hexdigest()
print(sign)
url = f'{url}&sig={sign}'
print(url)
r = requests.get(url)
j = r.json()
print(j)
