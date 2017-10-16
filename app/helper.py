# -*- coding: utf-8 -*-
u"""helper functions.

    SX-SMSServer.helper
    ~~~~~~~~~~~~~~
    
    辅助函数
    
    :copyright: (c) 2015 by Fire.
    :license: BSD, see LICENSE for more details.
"""

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature


def url_decode(query):
    u"""解析url路径返回请求参数字典."""
    d = {}
    params_list = query.split('&')
    for i in params_list:
        if i.find('=') >= 0:
            k, v = i.split('=', 1)
            d[k] = v
    return d


def q_decode(q):
    u"""分解'+'字符返回字典.

    例如: L12345+hpzl:02+kkdd:441302
    返回{
          'q': 'L12345',
          'hpzl': '02',
          'kkdd': '441302'
        }
    第一个'+'前的值用key: q表示.
    """
    d = {}
    q_list = q.split('+')
    d['q'] = q_list[0]
    for i in q_list[1:]:
        if i.find(':') >= 0:
            k, v = i.split(':', 1)
            d[k] = v
    return d


def verify_auth_token(token, key):
    u"""验证token是否正常.

    :param token: 令牌
    :param key: flask的SECRET_KEY值
    """
    s = Serializer(key)
    try:
        return s.loads(token)
    except SignatureExpired:
        # valid token, but expired
        return 'expired'
    except BadSignature:
        # invalid token
        return None


def row2dict(row):
    u"""输入sqlalchemy一行返回字典."""
    d = {}
    for col in row.__table__.columns:
        d[col.name] = getattr(row, col.name)
    return d

def ip2num(ip):
    u"""IP地址转整数."""
    return sum([256**j*int(i) for j,i in enumerate(ip.split('.')[::-1])])

def num2ip(num):
    u"""整数转IP地址."""
    return '.'.join([str(num/(256**i)%256) for i in range(3,-1,-1)])

def hphm2hpzl(hphm, hpys, hpzl):
    if hphm is None:
	return '99'
    if len(hphm) <= 2:
	return '99'
    if hpzl == '7' or hpzl == '07':
	return '07'
    if hphm[-1] == u'领':
	return '04'
    if hphm[1] == u'使':
	return '03'
    if hphm[-1] == u'港':
	return '26'
    if hphm[-1] == u'澳':
	return '27'
    if hpys == 3:
	return '06'
    if hphm[-1] == u'学':
	return '16'
    if hpys == 1:
	return '01'
    if hphm[-1] == u'警':
	return '23'
    if hphm[:2] == u'WJ':
	return '31'
    if hpys == 0:
	return '32'
    if hpys == 2:
	return '02'
    return '99'

