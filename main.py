import requests, json, os

url = os.environ.get('URL')
EMAIL = os.environ.get('EMAIL')
PASSWD = os.environ.get('PASSWD')
SCKEY = os.environ.get('SCKEY')

login_url = url + '/api/v1/passport/auth/login'
check_url = url + '/api/v1/user/checkin'

# 前端域名（与浏览器请求保持一致）
frontend_url = 'https://pin.dianping.men'

def sign(order, user, pwd):
    session = requests.session()
    header = {
        'origin': frontend_url,
        'referer': frontend_url + '/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
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
        print(response['message'])

        # 使用 auth_data (JWT) 作为鉴权token，无需Bearer前缀
        auth_data = response['data']['auth_data']
        header['authorization'] = auth_data

        # 进行签到
        res2 = session.post(url=check_url, headers=header).text
        print(res2)
        result = json.loads(res2)
        print(result['message'])
        content = result['message']

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
