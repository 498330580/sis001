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
        book_int = 0
        xs_int = 0

        for b in self.book.find():
            book_int += 1
            print(f"{book_int}--正在转存书籍信息：{b['name']}")
            rb = self.req.get("http://127.0.0.1:8000/api/book?name=" + b['name'])
            if rb["count"] == 0:
                rb = self.req.post("http://127.0.0.1:8000/api/book", {"name": b["name"], "category": 1})
                rb_id = rb["id"]
            else:
                rb_id = rb["results"][0]["id"]

            for xs in self.xiaosuo.find({"book": b['name']}):
                xs_int += 1
                print(f"{xs_int}--正在转存章节信息{b['name']}--{xs['title']}")
                rxs = self.req.get("http://127.0.0.1:8000/api/zhangjie?url=" + xs["url"])
                if rxs["count"] == 0:
                    rb = self.req.post(
                        "http://127.0.0.1:8000/api/zhangjie",
                        {
                            "collection": rb_id,
                            "category": 1,
                            "name": xs["title"],
                            "url": xs["url"],
                            "content": xs["内容"],
                            "index": xs["index"]
                        }
                    )
                else:
                    pass
        print(f"共转存{book_int}本书--{xs_int}章节")



        # for i in self.lishi.find():
        #     r = self.req.post("http://127.0.0.1:8000/api/lishi", {"url": i["url"]})
        #     if r["url"] == i["url"]:
        #         print(f"正在转存：{i['url']}-----成功")
        #     else:
        #         print(f"正在转存：{i['url']}-----失败")
        print("导入书籍、章节信息完毕")


if __name__ == "__main__":
    mongo = Get_mongo()
    # mongo.lishi_data()  # 已完成
    mongo.book_zhangjie_data()
