import requests, json, re, os

url = os.environ.get('URL')
EMAIL = os.environ.get('EMAIL')
PASSWD = os.environ.get('PASSWD')
SCKEY = os.environ.get('SCKEY')

login_url = url + '/api/v1/passport/auth/login'
check_url = url + '/api/v1/user/checkin'

def sign(order, user, pwd):
    session = requests.session()
    header = {
        'origin': url,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }
    data = {
        'email': user,
        'password': pwd
    }
    try:
        print(f'===账号{order}进行登录...===')
        print(f'账号：{user}')
        res = session.post(url=login_url, headers=header, data=data).text
        print(res)
        response = json.loads(res)
        print(response['msg'])
        res2 = session.post(url=check_url, headers=header).text
        print(res2)
        result = json.loads(res2)
        print(result['msg'])
        content = result['msg']
        if SCKEY:
            push_url = 'https://sctapi.ftqq.com/{}.send?title=机场签到&desp={}'.format(SCKEY, content)
            requests.post(url=push_url)
            print('推送成功')
    except Exception as ex:
        content = '签到失败'
        print(content)
        print("出现如下异常%s" % ex)
        if SCKEY:
            push_url = 'https://sctapi.ftqq.com/{}.send?title=机场签到&desp={}'.format(SCKEY, content)
            requests.post(url=push_url)
            print('推送成功')
    print(f'===账号{order}签到结束===\n')

if __name__ == '__main__':
    if not EMAIL or not PASSWD:
        print('配置文件格式错误')
        exit()
    sign(0, EMAIL, PASSWD)
