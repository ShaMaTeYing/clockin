import requests
import random
import json
import time
import schedule
import datetime


class CheckIn:
    def __init__(self):
        self.headers = {
            "Content-Type": "application/json",
            "Cookie": "PHPSESSID={}".format(self.get_random_str(32)),
            "User-Agent": "okhttp/3.10.0",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Accept-Encoding": "gzip"
        }

    def get_random_str(self, n):
        base_str = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        ans = ""
        for i in range(n):
            ans += base_str[random.randint(0, len(base_str) - 1)]
        return ans

    def login(self):
        url = "https://newoa.lierda.com/Webmall/Api/Index/login"
        data = {
            "clientId": self.get_random_str(32),
            "employeeNumber": "003981",
            "userPassword": "163235"
        }
        res = requests.post(url, headers=self.headers, data=json.dumps(data)).content
        res = json.loads(res.decode('utf-8'))
        return res['data']['token']

    def user_check_in(self):
        url = "https://newoa.lierda.com/webmall/api/attend/userSignIn"
        data = {
            "latitude": self.rand_latitude(),
            "location": self.rand_location(),
            "longitude": self.rand_longitude(),
            "mac": "292719C6-5C16-4093-A85D-33D0D0368BAF",
            "token": self.login()
        }
        time.sleep(random.randint(5, 15))
        res = requests.post(url, headers=self.headers, data=json.dumps(data)).content
        return res

    def rand_location(self):
        location = ["杭州市文一西路1326号利尔达物联网科技园1号楼", "西溪堂", "杭州市文一西路1326号利尔达物联网科技园6号楼", "杭州市文一西路1326号利尔达物联网科技园5号楼"]
        return location[random.randint(0, len(location) - 1)]

    def rand_latitude(self):
        return "{:.6f}".format(30.275119 + random.uniform(-0.0001, 0.0001))

    def rand_longitude(self):
        return "{:.6f}".format(119.992370 + random.uniform(-0.0001, 0.0001))


def job():
    # 如果当前不是工作日，则不打卡
    work_day = ['2020-01-14', '2020-01-15', '2020-01-16', '2020-01-17', '2020-01-18',
                '2020-01-19', '2020-01-20']
    print("今天是 {}".format(datetime.date.today()))
    if str(datetime.date.today()) not in work_day:
        print("{} 今天不是工作日哦".format(datetime.datetime.now()))
        return
    print("{} 开始准备打卡".format(datetime.datetime.now()))
    time.sleep(random.randint(60 * 1, 60 * 30))
    autocheck = CheckIn()
    autocheck.user_check_in()


def auto_check():
    schedule.every().day.at("08:00").do(job)
    schedule.every().day.at("17:40").do(job)
    # schedule.every(1).minutes.do(job)
    while True:
        try:
            schedule.run_pending()  # 运行所有可以运行的任务
            time.sleep(1)
        except:
            continue


if __name__ == "__main__":
    print("{} 开始运行程序".format(datetime.datetime.now()))
    auto_check()