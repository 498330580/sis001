from flask import Flask, make_response, jsonify, request, abort
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

    # 小说书籍储存(检查是否存在，不存在则储存)
    def book(self, name):
        self.xiaosuojihe.update_many({"name": name}, {"$setOnInsert": {"name": name}},
                                     upsert=True)

    # 历史储存
    def get_lishi(self, url):
        if self.lishi.count_documents({"url": url}):
            return True
        return False

    def create_lishi(self, url):
        if self.lishi.insert_one({"url": url}).inserted_id:
            return True
        return False


# 后端
app = Flask(__name__)
mongo = Mongodb()


@app.route('/')
def hello_world():
    return 'sis001后端'


@app.route("/xiaosuo", methods=['GET', 'POST'])
def xiaosuo():
    type_data = request.args.get("type")

    if type_data == "list":
        "获取小说列表"
        data_dic = {"mess": "返回小说列表成功", "data": [x for x in mongo.get_xiaosuo_list()]}
        return jsonify(data_dic)

    if type_data == "xiaosuo":
        "查询小说是否存在"
        if request.method == "GET":
            url = request.args.get("url")
            if url:
                if mongo.get_xiaosuo(url):
                    return jsonify({"mess": "URL存在", "data": url})
                else:
                    return jsonify({"mess": "URL不存在"})
            else:
                return jsonify({"mess": "错误，未传递URL"})
        elif request.method == "POST":
            if request.json and "url" in request.json:
                if not mongo.get_xiaosuo(request.json["url"]):
                    data_json = request.json
                    data_json["index"] = int(data_json["index"])
                    mongo.create_xiaosuo(data_json)
                    mongo.book(str(data_json["book"]))
                    return jsonify({"mess": "创建成功", "data": request.json["url"]})
                else:
                    return jsonify({"mess": "URL已存在", "data": request.json["url"]})
            else:
                abort(400)
        else:
            return abort(404)

    if type_data == "xiaosuo-lishi":
        "查询小说与历史是否存在"
        if request.method == "GET":
            url = request.args.get("url")
            if url:
                xs = mongo.get_xiaosuo(url)
                ls = mongo.get_lishi(url)
                return jsonify({"mess": "查询成功", "data": {"xiaosuo": xs, "lishi": ls}})
            else:
                return jsonify({"mess": "错误，未传递URL"})
        else:
            return abort(404)

    if type_data == "lishi":
        "判断历史记录是否存在，不存在则添加历史记录"
        if request.method == "GET":
            url = request.args.get("url")
            if url:
                if mongo.get_lishi(url):
                    return jsonify({"mess": "URL存在"})
                else:
                    return jsonify({"mess": "URL不存在"})
            else:
                return jsonify({"mess": "错误，未传递URL"})
        elif request.method == "POST":
            if request.json and "url" in request.json:
                if not mongo.get_lishi(request.json["url"]):
                    mongo.create_lishi(request.json["url"])
                    return jsonify({"mess": "创建成功", "data": request.json["url"]})
                else:
                    return jsonify({"mess": "URL已存在", "data": request.json["url"]})
            else:
                abort(400)
        else:
            return abort(404)

    return "小说获取"


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'mess': '连接不存在'}), 404)


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'mess': '错误的请求'}), 404)


if __name__ == '__main__':
    app.run(debug=True)
