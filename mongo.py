import pymongo


# 数据库连接
class Mongodb:
    def __init__(self):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.dblist = self.myclient.list_database_names()
        self.mydb = self.myclient["sis001"]
        self.lishi = self.mydb["历史"]
        self.xiaosuo = self.mydb["小说"]
        self.xiaosuojihe = self.mydb["小说书籍"]

    # 获取符合条件的所有小说
    def get_xiaosuo_list(self, tiaojian=None):
        if tiaojian is None:
            tiaojian = {}
        return self.xiaosuo.find(tiaojian, {"_id": 0})

    def get_xiaosuojihe_list(self):
        return self.xiaosuojihe.find({}, {"_id": 0, "name": 1})

    # 小说储存
    def get_xiaosuo(self, url):
        if self.xiaosuo.count_documents({"url": url}):
            return True
        return False

    def create_xiaosuo(self, data):
        if self.xiaosuo.insert_one(data).inserted_id:
            return True
        return False

    # 历史储存
    def get_lishi(self, url):
        if self.lishi.count_documents({"url": url}):
            return True
        return False

    def create_lishi(self, url):
        if self.lishi.insert_one({"url": url}).inserted_id:
            return True
        return False