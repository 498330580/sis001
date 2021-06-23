import pymongo
import os
import sys

# 设定工作目录为当前脚本目录
jaoben_path = os.path.abspath(os.path.dirname(sys.argv[0])) # 当前脚本目录
os.chdir(jaoben_path)   # 设定工作目录为脚本目录

Download_path = os.path.join(jaoben_path, "download")    # 下载目录

def path_panduan(path_data):
    if not os.path.exists(path_data):  #判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path_data)


class Get_Xiaosuo:
    def __init__(self):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient["sis001"]
        self.xiaosuo = self.mydb["小说"]
        self.xiaosuojihe = self.mydb["小说书籍"]
        path_panduan(Download_path)

    def dow(self):
        for i in self.xiaosuojihe.find({"下载状态": "未下载"}):
            xiaosuo_path = os.path.join(Download_path, i["name"])
            for xs in self.xiaosuo.find({"book":i["name"]}):
                neirong = self.xiaosuo_txt(xs["内容"])
                with open(os.path.join(os.path.join(xiaosuo_path, xs["title"]), f"{str(xs['title']).replace(r'/', '')}.txt"), "w", encoding='utf-8') as f:
                    f.write(neirong)
                self.xiaosuo.update_many(i, {"$set": {"下载状态": "已下载"}})
            print(f"书籍《{i['book']}》————下载完成")

    def xiaosuo_txt(self, data):
        t = ""
        for i in data:
            t = t + i
        return t