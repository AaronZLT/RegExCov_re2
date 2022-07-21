from urllib.request import urlopen,HTTPError,URLError
import ssl
import json

tokens={'lab':'54bc79cb7af38b6da15bb192c0056ee628bce809','spark1':'d2a6a4204a2c03495541a02ab4b60fca0d8d2e7c','spark2':'9e1a0c0d621d9849fd637c06ff7a287e3b3b1c19','spark3':'c6f077fb144638ec0f77c41ad9268074a6f3d889','spark4':'a7ba4128d5059e6cfe877be5cd0c07f67e4748a7'}
access='?access_token='
access=access+tokens['lab']
context = ssl._create_unverified_context()

api_url='https://api.github.com/repos/srammya1/KPR'
api_url2='https://api.github.com/repos/jziub/HTRC-Random-Sampling'
api_url3='https://api.github.com/repos/caarlos0/spotify-api'
api_url4='https://api.github.com/repos/nystromb/PegPuzzle-Game'
api_url5='https://api.github.com/repos/rohitandrews/cellbots'
api_url6='https://api.github.com/repos/raingxm/Currency'
api_url7='https://api.github.com/repos/zhouxi01/jce'
api_url8='https://api.github.com/repos/UCLA-EASM/liferay-user-library'
string_url='https://github.com/nithishaoleti/bamoo_test'
# response=urlopen(api_url+access, context=context)
response=urlopen(string_url+access, context=context)
webContent = response.read().decode('utf-8') ##need .decode('utf-8') in python3
# is_private=json.loads(webContent)['private']
# valid_api= not is_private
print(webContent)
print(response.info())
##get rate limit remaining and sleep one hour if it is 0
# left_rate=int(response.info().get('X-RateLimit-Remaining'))
# print(left_rate)
