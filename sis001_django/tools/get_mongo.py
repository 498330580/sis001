import pymongo
import requests


# Req
class Req:
    def __init__(self):
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/67.0.3396.99 Safari/537.36",
            "Authorization": "Token 27171cc46f6bda2668ca755810635e577f600fa4"}

    def get(self, url):
        return requests.get(url, headers=self.header, timeout=5).json()

    def post(self, url, data):
        return requests.post(url, headers=self.header, timeout=5, json=data).json()


# 获取数据并储存数据库
class Get_mongo:
    def __init__(self):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient["sis001"]
        self.xiaosuo = self.mydb["小说"]
        self.book = self.mydb["小说书籍"]
        self.lishi = self.mydb["历史"]
        self.req = Req()

    def lishi_data(self):
        print("开始获取历史消息")
        for i in self.lishi.find():
            r = self.req.post("http://127.0.0.1:8000/api/lishi", {"url": i["url"]})
            if r["url"] == i["url"]:
                print(f"正在转存：{i['url']}-----成功")
            else:
                print(f"正在转存：{i['url']}-----失败")
        print("历史消息获取完毕")

    def book_zhangjie_data(self):
        print("开始导入书籍、章节信息")
        for i in self.lishi.find():
            r = self.req.post("http://127.0.0.1:8000/api/lishi", {"url": i["url"]})
            if r["url"] == i["url"]:
                print(f"正在转存：{i['url']}-----成功")
            else:
                print(f"正在转存：{i['url']}-----失败")
        print("导入书籍、章节信息完毕")


if __name__ == "__main__":
    mongo = Get_mongo()
    # mongo.lishi_data()  # 已完成
