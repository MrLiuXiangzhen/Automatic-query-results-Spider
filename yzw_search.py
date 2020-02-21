import re
import time
import requests
from send_email import SendMail


class Detection(object):
    def __init__(self, htmlname=None):
        """
        成绩探测 可以传入列表，网址已写死，其它学校可自行修改
        SCORE_URL:主登录地址，成绩查询地址
        RES_URL,RES_SCORE:备用地址
        URL,URL_login:发送邮件内容的地址，没有什么用
        SCORE_DATA:查询成绩需要输入验证的信息
        RES_DATA:学信网登录验证信息，用于登录另一个查询成绩的地址（备胎）
        @param htmlname: 保存到本地的成绩页面，默认为空
        """
        self.SCORE_URL = "https://yz.chsi.com.cn/apply/cjcx/cjcx.do"  # TODO 成绩页面地址
        self.RES_URL = "https://account.chsi.com.cn/passport/login?service=https://yz.chsi.com.cn/j_spring_cas_security_check"  # TODO 备用学信网登录安全验证地址
        self.RES_SCORE = "https://yz.chsi.com.cn/apply/cjcxa/"  # 备用成绩页面地址
        self.URL = "https://yz.chsi.com.cn/apply/cjcx/sch/11664.dhtml"  # TODO 学校页面地址
        self.URL_login = "https://yz.chsi.com.cn/apply/cjcx/t/11664.dhtml"  # TODO 成绩查询页面地址
        self.SCORE_DATA = {
            "xm": "刘向臻",  # TODO 姓名
            "zjhm": "666666200001010001",  # TODO 身份证号
            "ksbh": "116646666666666",  # TODO 考号
            "bkdwdm": "11664",  # TODO 学校编号
        }
        self.RES_DATA = {  # 备用学信网查询，部分学校可用
            "username": "18288888888",  # TODO 学信账号
            "password": "888888",  # TODO 学信账号密码
            "lt": "",  # TODO 可以通过浏览器开发人员工具查到,原字符串内容以删除，建议自行进开发人员工具查询添加
            # 这一行不知道干什么的，但是没有就登陆不了学信网
            "execution": "",  # TODO 这一行可以通过浏览器开发人员工具查到,原字符串内容以删除，建议自行进开发人员工具查询添加
            "_eventId": "submit",
        }
        self.HEADERS = {
            # 华为P40pro
            "User-Agent": "Mozilla/5.0 (Linux; Android 10.1.1; HUAWEI P40pro/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Mobile Safari/537.36",
        }
        self.htmlname = htmlname

    @staticmethod
    def local_time():
        """
        获取时间
        @return: 时间:年-月-日 时:分:秒
        """
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def writepage(self, data):
        """
        将网页写入本地文件
        @param data: 接收到解码之后的网页内容
        """
        if self.htmlname is not None:
            for i, name in enumerate(self.htmlname):
                with open("./" + name + ".html", 'w', encoding='utf-8') as f:
                    f.write(data[i])
                print(name + ".html", " 信息写入成功，即将打包成邮件为您发送！")

    def receive(self):
        """
        收发模块
        @return: str字符串,用于邮件发送正文内容，返回给调用方法进行处理
        """
        while True:
            # 主地址
            score = session.post(self.SCORE_URL, data=self.SCORE_DATA, headers=self.HEADERS)
            str = re.findall(r"请检查您报考的招生单位是否已开通初试成绩查询功能", score.content.decode())
            str2 = re.findall(r"请点选成绩查询省市|内蒙古|江西", score.content.decode())  # TODO 后面的省份随便写（可有可无），但是不要是报考省份
            print(str2)
            if not str:  # str没找到进入
                if str2:  # str2找到了进入
                    return None
                # TODO 这一行将作为邮件内容返回调用者，可改可不改
                string = "经系统检测研招网公布了成绩(见附件)，或者登录：" + self.URL + " ，查询成绩" + "\n链接2：" + self.URL_login
                # 备用地址,以备官方临时改地址
                session.post(self.RES_URL, data=self.RES_DATA, headers=self.HEADERS)
                score_res = session.get(self.RES_SCORE, headers=self.HEADERS, data=self.RES_DATA)

                self.writepage([score.content.decode(), score_res.content.decode()])
                return self.local_time() + ' ' + string
            session.post(self.URL_login, headers=self.HEADERS)
            time.sleep(10)  # TODO 每次查询间隔时间，单位：秒

    def run(self):
        """
        调用方法
        @return: str字符串,用于邮件发送正文内容
        """
        str = self.receive()
        if str is not None:
            print(str)
            return str
        return


if __name__ == '__main__':

    while True:
        session = requests.session()
        detection = Detection(htmlname=['yzw', 'yzw_res'])
        str = detection.run()
        if str is not None:
            break
        session.close()
        del detection
        # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " 失败一次")
        time.sleep(1)

    send = SendMail(username='123456@qq.com',  # TODO 发送邮箱号
                    passwd='jtguqerwadhsdfge',  # TODO smtp授权码 qq邮箱的一般16位
                    email_host='smtp.qq.com',
                    port=25,  # TODO port端口号
                    ssl_port=465,  # TODO ssl端口号
                    recv=['719903178@qq.com', ],  # TODO 接收邮箱地址
                    title='经系统检测研招网公布了成绩(见附件)，请查收',  # TODO 邮件标题
                    content=str,
                    file=[r'./yzw.html', r'./yzw_res.html'],
                    ssl=True, )
    print("正在发送邮件...(目标邮箱号：719903178@qq.com)")  # TODO 控制台输出，没有实际用处，可以自行修改或删除
    send.send_run()
    print("请注意查收QQ号:*07结尾的邮件！")  # TODO 控制台输出，没有实际用处，可以自行修改或删除
