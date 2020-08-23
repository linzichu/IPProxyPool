from settings import MAX_SCORE


class Proxy(object):
    def __init__(self, ip=None, port=None, protocol=-1, nick_type=-1, speed=-1, area=None, score=MAX_SCORE,
                 disable_domains=[]):
        # ip：代理的IP地址
        self.ip = ip
        # port：代理Ip的端口号
        self.port = port
        # protocol：代理IP支持的协议类型，http是0，https是1，http和https都支持是2
        self.protocol = protocol
        # nick_type：代理IP的匿名程度，高匿：0，匿名：1，透明：2
        self.nick_type = nick_type
        # speed：代理IP的响应速速，单位是s
        self.speed = speed
        # area：代理IP所在的地区
        self.area = area
        # score：代理IP的评分，用于衡量代理的可用性
        self.score = score
        # 默认分值可以通过配置文件进行配置，在进行代理可用性检查的时候，没遇到一次请求失败就减1分，减到0从数据库剔除
        # disable_domains：不可用域名列表，有些代理IP在某些域名下不可用，但是在其他域名下可用
        self.disable_domains = disable_domains

    def __str__(self):
        # 返回数据的字符串
        return str(self.__dict__)


proxy = Proxy("192.169.31.40", 80)
if __name__ == '__main__':
    print(proxy.__dict__)
