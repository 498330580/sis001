from flask import Flask, make_response, jsonify, request, abort
from mongo import *


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
                # print(request.json)
                if not mongo.get_xiaosuo(request.json["url"]):
                    mongo.create_xiaosuo(request.json)
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
