import hmac
from hashlib import sha256

push_info = '[{}:{}] {} new commit by {} {}:'
commit_message = '\n   {}:[{}]'
branch_info = '[{}:{}] {} {} this branch'


class Utils(object):
    '''工具类'''
    @staticmethod
    def isValid(token: str, payload: str, signature: str) -> bool:
        '''判断请求是否能通过验证'''
        my_sign = 'sha256=' + hmac.new(token.encode(
            'utf-8'), payload, digestmod=sha256).hexdigest()
        return hmac.compare_digest(my_sign, signature)

    @staticmethod
    def generate_message(payload: dict):
        '''通过payload生成需要发送的信息'''
        try:
            if payload['created'] or payload['deleted']:
                action = 'create' if payload['created'] else 'delete'
                return branch_info.format(payload['repository']['name'],
                                          payload['ref'].split('/')[-1],
                                          payload['pusher']['name'],
                                          action)
            else:
                is_forced = 'via force push' if payload['forced'] else ''
                tmp_result = push_info.format(payload['repository']['name'],
                                              payload['ref'].split('/')[-1],
                                              len(payload['commits']),
                                              payload['pusher']['name'],
                                              is_forced)
                for commit in payload['commits']:
                    # 取commit哈希前七位
                    tmp_result += commit_message.format(
                        commit['id'][0:7], commit['message'])
                return tmp_result
        except:
            print('invalid payload:\n{}\n'.format(payload))
            return 'error when handle payload, please check log...'