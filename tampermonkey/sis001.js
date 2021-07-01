// @require      https://cdn.jsdelivr.net/npm/jquery@3.4.1/dist/jquery.slim.min.js

(function () {
    // 'use strict';   //严格模式

    // import Vue from 'vue'

    var host = "http://127.0.0.1:8000/"     // 这里填写你后端的地址
    var token = "27171cc46f6bda2668ca755810635e577f600fa4"      // 这里填写你后端的token

    // function dj(url) {
    //     alert(url);
    // }

    // 判断是否为小说板块
    function xiaosuo(url) {
        // let url = window.location.href;
        // let url_zz = /^http.*?forum-(3|2|8|9)(1|2|3|6|7|8)(2|3|4|9|)-.*tml$/ig;
        let url_zz = /^http.*?forum-((322)|(383)|(334)|(279)|(359)|(31)|(83)|(96))-.*tml$/ig;
        let url_zz1 = /^http:.*?fid=((322)|(383)|(334)|(279)|(359)|(31)|(83)|(96))&.*/
        if (url_zz.test(url) || url_zz1.test(url)) {
            type_int = 1;
            return true
        } else {
            type_int = 0;
            return false
        }
    }

    // 列表页识别
    function list() {
        var content = document.getElementsByName("moderate");   //获取内容
        var tables = content[0].getElementsByTagName("table");  //获取所有table标签

        for (let i = 0; i < tables.length; i++) {
            if (tables[i].id) {
                let table = tables[i];
                let bs = table.getElementsByTagName("b");
                if (bs.length) {
                    if (bs[0].innerText == "推荐主题" || bs[0].innerText == "版块主题") {
                        let spans = tables[i].getElementsByTagName("span");
                        for (let index = 0; index < spans.length; index++) {
                            if (spans[index].id) {
                                let a_data = spans[index].getElementsByTagName("a")[0]
                                let get_url = a_data.href
                                GM_xmlhttpRequest({
                                    url:host + "panduan?type=xiaosuo&url=" + get_url,
                                    method: "GET",
                                    anonymous: true,
                                    headers: {
                                        "Content-type": "application/json",
                                        "Authorization": "Token " + token
                                    },
                                    onload:function(xhr){
                                        let data = JSON.parse(xhr.responseText)
                                        if (data["mess"]!= "错误，未传递URL") {
                                            let xs = data["data"]["xiaosuo"]
                                            let ls = data["data"]["lishi"]
                                            let url = window.location.href;
                                            // let url_zz = /^http.*?forum-(3|2|8|9)(2|3|6|7|8)(2|3|4|9|)-.*tml$/ig
                                            if (xiaosuo(url)) {
                                                if (xs) {
                                                    a_data.innerHTML += '<i class="iconfont icon-yikanwan" style="color:#43CD80;font-size:75%;" title="已保存"></i>';
                                                } else {
                                                    a_data.innerHTML += '<i class="iconfont icon-bianzu24" style="color:#000000;font-size:75%;" title="未保存"></i>';
                                                }
                                            }
                                            if (ls) {
                                                a_data.innerHTML += '<i class="iconfont icon-yikan" style="color:#43CD80;font-size:75%;" title="已浏览"></i>';
                                            } else {
                                                a_data.innerHTML += '<i class="iconfont icon-weikan" style="color:#000000;font-size:75%;" title="未浏览"></i>';
                                            }
                                        } else {
                                            console.log("错误，未传递URL");
                                        }
                                    }
                                });
                                // button = document.createElement("button");
                                // button.setAttribute("type", "button");
                                // button.setAttribute("onclick", "tanchuang(" + url + ")");
                                // button.appendChild(document.createTextNode("加入合集"));
                                // spans[index].appendChild(button);
    
                            }
                        }
                    }
                }
                
            }
        }
    }

    // 去除头顶广告
    function ad_del() {
        $(".ad_text").remove();
        // document.getElementById("ad_text").remove();
    }

    // 搜索页识别
    function search() {
        var tbodys = document.getElementsByTagName("tbody");
        for (let i = 0; i < tbodys.length; i++) {
            let tbody = tbodys[i];
            let a = tbody.getElementsByTagName("th")[0].getElementsByTagName("a")[0]
            let url = a.href
            let url_bankuai = tbody.getElementsByClassName("forum")[0].getElementsByTagName("a")[0].href
            GM_xmlhttpRequest({
                url:host + "panduan?type=xiaosuo&url=" + url,
                method: "GET",
                anonymous: true,
                headers: {
                    "Content-type": "application/json",
                    "Authorization": "Token " + token
                },
                onload:function(xhr){
                    let data = JSON.parse(xhr.responseText)
                    if (data["mess"]!= "错误，未传递URL") {
                        let xs = data["data"]["xiaosuo"]
                        let ls = data["data"]["lishi"]
                        // console.log(url_bankuai)
                        if (xiaosuo(url_bankuai)) {
                            // console.log("已识别")
                            if (xs) {
                                a.innerHTML += '<i class="iconfont icon-yikanwan" style="color:#43CD80;font-size:75%;" title="已保存"></i>';
                            } else {
                                a.innerHTML += '<i class="iconfont icon-bianzu24" style="color:#000000;font-size:75%;" title="未保存"></i>';
                            }
                        }
                        if (ls) {
                            a.innerHTML += '<i class="iconfont icon-yikan" style="color:#43CD80;font-size:75%;" title="已浏览"></i>';
                        } else {
                            a.innerHTML += '<i class="iconfont icon-weikan" style="color:#000000;font-size:75%;" title="未浏览"></i>';
                        }
                    } else {
                        console.log("错误，未传递URL");
                    }
                }
            });
        }
    }

    // 标签保存（返回标签ID）
    function biaoqiansave() {
        let biaoqian = document.getElementsByName("modactions")[0].getElementsByTagName("h1")[0].getElementsByTagName("a")[0].innerText
        biaoqian = biaoqian.replace('[', '')
        biaoqian = biaoqian.replace(']', '')
        GM_xmlhttpRequest({
            url: host + "api/fenlei?name=" + biaoqian,
            method :"GET",
            anonymous: true,
            headers: {
                "Content-type": "application/json",
                "Authorization": "Token " + token
            },
            onload:function(xhr){
                if (JSON.parse(xhr.responseText)["count"] == 0){
                    GM_xmlhttpRequest({
                        url: host + "api/fenlei",
                        method :"POST",
                        data:JSON.stringify({"name": biaoqian}),
                        dataType: "json",
                        anonymous: true,
                        headers: {
                            "Content-type": "application/json",
                            "Authorization": "Token " + token
                        },
                        onload:function(xhr){
                            if (JSON.parse(xhr.responseText)["name"] == biaoqian) {
                                console.log("标签", biaoqian, "保存成功");
                                biaoqian_id = JSON.parse(xhr.responseText)["id"]
                            } else {
                                console.log("标签", biaoqian, "保存失败");
                                return null
                            }
                        }
                    })
                } else {
                    console.log("标签", biaoqian, "已存在");
                    // console.log(typeof JSON.parse(xhr.responseText)["results"][0]['id']);
                    biaoqian_id = JSON.parse(xhr.responseText)["results"][0]['id'];
                }
            },
            // onerror: function(e) {
            //     console.log("标签错误：", e);
            //     return null;
            // }
        })
    }

    // 版块保存（返回版块ID）
    function bankuaisave(bankuai) {
        // var bankuai = document.getElementById("nav").getElementsByTagName("a")[-1].innerText
        // bankuai = bankuai.replace('[', '')
        // bankuai = biaoqian.replace(']', '')
        GM_xmlhttpRequest({
            url: host + "api/bankuai?name=" + bankuai,
            method :"GET",
            anonymous: true,
            headers: {
                "Content-type": "application/json",
                "Authorization": "Token " + token
            },
            onload:function(xhr){
                if (JSON.parse(xhr.responseText)["count"] == 0){
                    GM_xmlhttpRequest({
                        url: host + "api/bankuai",
                        method :"POST",
                        data:JSON.stringify({"name": bankuai}),
                        dataType: "json",
                        anonymous: true,
                        headers: {
                            "Content-type": "application/json",
                            "Authorization": "Token " + token
                        },
                        onload:function(xhr){
                            if (JSON.parse(xhr.responseText)["name"] == bankuai) {
                                console.log("版块", bankuai, "保存成功");
                                bankuai_id = JSON.parse(xhr.responseText)["id"]
                            } else {
                                console.log("版块", bankuai, "保存失败");
                                return null
                            }
                        }
                    })
                } else {
                    console.log("版块", bankuai, "已存在");
                    bankuai_id = JSON.parse(xhr.responseText)["results"][0]['id'];
                }
            },
            // onerror: function(e) {
            //     console.log("标签错误：", e);
            //     return null;
            // }
        })
    }

    // 浏览记录不存在的情况
    function addurl(html, url) {
        // 检查数据库中网址是否存在
        GM_xmlhttpRequest({
            url:host + "api/lishi?url=" + url,
            method :"GET",
            anonymous: true,
            headers: {
                "Content-type": "application/json",
                "Authorization": "Token " + token
            },
            onload:function(xhr){
                let data = JSON.parse(xhr.responseText)
                if (data["count"]) {
                    console.log("数据库中URL存在");
                    // url存在
                    
                    // 由于加载本函数的API已检查过该用户是否浏览过该url，此处不再做检查
                    console.log("用户未浏览过该url");
                    // 关联数据库url与用户（添加url到用户浏览）
                    GM_xmlhttpRequest({
                        url:host + "api/user_url",
                        method :"POST",
                        data:JSON.stringify({"lishi": data["results"][0]["id"]}),
                        dataType: "json",
                        anonymous: true,
                        headers: {
                            "Content-type": "application/json",
                            "Authorization": "Token " + token
                        },
                        onload:function(r){
                            if (JSON.parse(r.responseText)["lishi"] == data["results"][0]["id"]) {
                                console.log("插入用户url浏览记录成功");
                                html.innerHTML += '<i class="iconfont icon-yikan" style="color:#43CD80;font-size:75%;" title="已浏览"></i>';
                            } else {
                                html.innerHTML += '<i class="iconfont icon-weikan" style="color:#000000;font-size:75%;" title="未浏览"></i>';
                            }
                        }
                    });
                } else {
                    // url不存在
                    // 创建url
                    console.log("数据库中url不存在");
                    GM_xmlhttpRequest({
                        url:host + "api/lishi",
                        method :"POST",
                        data:JSON.stringify({"url": url}),
                        dataType: "json",
                        anonymous: true,
                        headers: {
                            "Content-type": "application/json",
                            "Authorization": "Token " + token
                        },
                        onload:function(xhr){
                            if (JSON.parse(xhr.responseText)["url"] == url) {
                                console.log("数据库URL记录保存成功");
                                // 关联数据库url与用户（添加url到用户浏览）
                                GM_xmlhttpRequest({
                                    url:host + "api/user_url",
                                    method :"POST",
                                    data:JSON.stringify({"lishi": JSON.parse(xhr.responseText)["id"]}),
                                    dataType: "json",
                                    anonymous: true,
                                    headers: {
                                        "Content-type": "application/json",
                                        "Authorization": "Token " + token
                                    },
                                    onload:function(r){
                                        if (JSON.parse(r.responseText)["lishi"] == JSON.parse(xhr.responseText)["id"]) {
                                            console.log("插入用户url记录成功");
                                            html.innerHTML += '<i class="iconfont icon-yikan" style="color:#43CD80;font-size:75%;" title="已浏览"></i>';
                                        } else {
                                            html.innerHTML += '<i class="iconfont icon-weikan" style="color:#000000;font-size:75%;" title="未浏览"></i>';
                                        }
                                    }
                                });
                            } else {
                                html.innerHTML += '<i class="iconfont icon-weikan" style="color:#000000;font-size:75%;" title="未浏览"></i>';
                            }
                        }
                    });
                }
            }
        })

        
    }

    // 获取当前详情页的章节对应书籍，并将书籍加入用户收藏
    function add_book_user(url) {
        GM_xmlhttpRequest({})
    }

    // 判断book是否已存在于数据库中
    function addbook(url) {
        //检查数据库中该章节记录是否存在
        GM_xmlhttpRequest({
            url:host +"api/zhangjie?url=" + url,
            method :"GET",
            anonymous: true,
            headers: {
                "Content-type": "application/json",
                "Authorization": "Token " + token
            },
            onload:function(xhr){
                if (JSON.parse(xhr.responseText)["count"] == 0){
                    // 数据库中该章节记录不存在
                    console.log("数据库中不存在章节记录");
                    document.getElementById("book").remove();
                } else {
                    // 数据库中该章节记录存在
                    console.log("数据库中已存在章节记录");
                    // zhangjie_data = false;
                    document.getElementById("zhangjie").remove();
                    book_id = JSON.parse(xhr.responseText)["results"][0]["collection"]
                }
            }
        })
    }

    // 详情页编辑
    function xiangqing() {
        let h1 = document.getElementsByName("modactions")[0].getElementsByTagName("h1")[0];
        let url = window.location.href;
        let a = document.getElementById("nav").getElementsByTagName("a")
        let url_bankuai = a[a.length-1].href
        let bankuai = a[a.length-1].innerText
        // introduction = document.getElementsByName("description")[0].content.replace(/ SiS001! Board  - \[第一会所 邀请注册\]/ig,"")
        // console.log(introduction);
        
        bankuaisave(bankuai)
        biaoqiansave()

        if (xiaosuo(url_bankuai)) {
            document.getElementById("foruminfo").innerHTML += `<br><div id="save" style="border: 2px solid lightblue;text-align:center;border-style: outset;background-color: lightblue;padding: 5px;">
            <div id="zhangjie">
            <i class="iconfont icon-leibie" title="保存的数据类别">类别：</i>
            <select name="public-choice" v-model="type" style="width:149px;height:25px;text-align:center;text-align-last:center;"><option :value="coupon.id" v-for="coupon in typelist">{{coupon.name}}</option></select>
            <i class="iconfont icon-xuhao" title="建议填写当前的开始章号">序号:</i>
            <input type="number" v-model="indexdata" style="text-align:center;text-align-last:center;">
            <i class="iconfont icon-book" title="想要收集到那本书下面">书籍：</i>
            <input id="book1" type="text" v-model="book_vue" style="width:200x;">
            <button class="iconfont icon-baocun" style="font-size:100%;" @click="savexiapsuo()">提交</button>
            </div>
            <div id="book">
            <i class="iconfont icon-book" title="想要收集到那本书下面">书籍：</i>
            <input id="book2" type="text" v-model="book_vue" style="width:200x;" disabled="disabled">
            <button class="iconfont icon-baocun" style="font-size:100%;" @click="shouchang()">提交</button>
            </div>
            </div>`}

        // 浏览状态判断与书籍状态
        GM_xmlhttpRequest({
            url:host + "panduan?type=xiaosuo&url=" + url,
            method: "GET",
            anonymous: true,
            headers: {
                "Content-type": "application/json",
                "Authorization": "Token " + token
            },
            onload:function(xhr){
                let data = JSON.parse(xhr.responseText)
                if (data["mess"]!= "错误，未传递URL") {
                    let xs = data["data"]["xiaosuo"]
                    let ls = data["data"]["lishi"]

                    // 判断url是否为小说栏目
                    if (xiaosuo(url_bankuai)) {
                        // 判断当前账户是否收藏过该书籍
                        if (xs) {
                            console.log("书籍已收藏");
                            h1.innerHTML += '<i class="iconfont icon-yikanwan" style="color:#43CD80;font-size:75%;" title="已保存"></i>';
                            document.getElementById("save").remove();
                        } else {
                            console.log("书籍未收藏");
                            h1.innerHTML += '<i class="iconfont icon-bianzu24" style="color:#000000;font-size:75%;" title="未保存"></i>';
                            addbook(url);
                        }
                    }

                    // 判断当前账户是否已浏览过该网址
                    if (ls) {
                        h1.innerHTML += '<i class="iconfont icon-yikan" style="color:#43CD80;font-size:75%;" title="已浏览"></i>';
                        console.log("浏览记录已存在");
                    } else {
                        console.log("浏览记录不存在");
                        addurl(h1, url)
                    }
                } else {
                    console.log("错误，未传递URL");
                }
            }
        });

        // console.log(document.getElementsByName("modactions")[0].getElementsByTagName("h1")[0].innerText);
        // return document.getElementsByName("modactions")[0].getElementsByTagName("h1")[0].childNodes[1].nodeValue.trim()    //获取标题，不包含标签
        title = document.getElementsByName("modactions")[0].getElementsByTagName("h1")[0].childNodes[1].nodeValue.trim()    //获取标题，不包含标签
        // return document.getElementsByName("modactions")[0].getElementsByTagName("h1")[0]
        if (/【(.*?)】/ig.exec(title)){
            book = /【(.*?)】/ig.exec(title)[1];
            // console.log(book);
            // // console.log(document.getElementById("book1"))
            // console.log("我在执行");
        } else {
            book = ""
        }
        if (/【作者：(.*?)】/ig.exec(title)) {
            zuozhe = /【作者：(.*?)】/ig.exec(title)[1]
        } else {
            zuozhe = "无"
        }
        if (/（(\d+.*?)(-|）)/ig.exec(title)) {
            index_int = parseInt(/（(\d+.*?)(-|）)/ig.exec(title)[1])
        } else {
            index_int = 1
        }

        

    }

    // 章节储存
    function zhangjiesave(data, b_id) {
        // 书籍加入用户收藏
        GM_xmlhttpRequest({
            url: host+"api/user_coll",
            method :"POST",
            data:JSON.stringify({"collection": b_id, "collect": true}),
            dataType: "json",
            anonymous: true,
            headers: {
                "Content-type": "application/json",
                "Authorization": "Token " + token
            },
            onload:function(xhr){
                if (JSON.parse(xhr.responseText)['collection']==b_id){
                    console.log("书籍", book, "加入收藏成功");
                } else {
                    console.log("书籍", book, "加入收藏失败");
                }
            }
        })

        // 章节储存
        GM_xmlhttpRequest({
            url:host +"api/zhangjie?url=" + url,
            method :"GET",
            anonymous: true,
            headers: {
                "Content-type": "application/json",
                "Authorization": "Token " + token
            },
            onload:function(xhr){
                if (JSON.parse(xhr.responseText)["count"] == 0){
                GM_xmlhttpRequest({
                    url:host+"api/zhangjie",
                    method :"POST",
                    // data:JSON.stringify({"name": title.innerText, "index": this.indexdata, "url": url, "collection": book_id}),
                    data:JSON.stringify(data),
                    dataType: "json",
                    anonymous: true,
                    headers: {
                        "Content-type": "application/json",
                        "Authorization": "Token " + token
                    },
                    onload:function(xhr){
                        if (JSON.parse(xhr.responseText)['url']==data["url"]){
                            console.log("章节：", data["name"], "保存成功");
                            alert("保存成功！");
                            document.getElementById("save").remove();
                            document.getElementsByClassName("iconfont icon-bianzu24")[0].remove()
                            document.getElementsByName("modactions")[0].getElementsByTagName("h1")[0].innerHTML += '<i class="iconfont icon-yikanwan" style="color:#43CD80;font-size:75%;" title="已保存"></i>';
                        } else {
                            console.log("章节：", data["name"], "保存失败");
                            alert("保存失败！");
                        }
                    }
                })
                } else {
                    console.log("章节已存在");
                }
            }
        })
    }

    

    console.log("sis001脚本运行")
    var url = window.location.href;
    var title = "";     //小说章节标题
    var book = "";      //小说书籍标题
    var zuozhe = "";      //作者
    // var introduction = "";  //简介
    var book_id = 1;    //小说书籍储存ID
    var index_int = 0;  //小说章节索引
    var type_int = 0;   //小说章节类型
    var bankuai_id = null;  //版块ID
    var biaoqian_id = null;  //标签ID
    // var zhangjie_data = true; // 判断章节在数据库中是否存在
    var url_zz = /^http.*?forum.*/ig;
    if (url_zz.test(url)) {
        document.getElementsByTagName("head")[0].innerHTML += '<link rel="stylesheet" href="//at.alicdn.com/t/font_2616980_8iw3dgaotf4.css">';
        // document.getElementsByTagName("head")[0].innerHTML += `<link rel="stylesheet" href="https://unpkg.com/element-plus/lib/theme-chalk/index.css">`;
        ad_del();
        let search_list_zz = /^http.*?search.*/ig
        if (search_list_zz.test(url)) {
            if (!document.getElementsByName("searchsubmit").length) {
                console.log("搜索结果页");
                search();
            } else {
                console.log("当前是搜索开始页");
            }
        } else {
            let list_zz = /^http.*?forum\/forum.*?html/ig
            let thread_zz = /^http.*?thread.*/ig

            if (list_zz.test(url)){
                console.log("列表页");
                list();
            }

            if (thread_zz.test(url)) {
                console.log("详情页");
                xiangqing();
            }
        }
    }

    /*Vue操作*/
    var vm = new Vue({
    // window.$vm = new Vue({
        el: "#save",
        data: {
            typelist: [
                {id: 0, name: "无"},
                {id: 1, name: "小说"},
                {id: 2, name: "图片"},
            ],
            type: type_int,
            book_vue: book,
            indexdata: index_int
            // zj: false
        }, methods: {
            // 保存按钮
            savexiapsuo(){
                if (!this.type) {
                    alert("类型不能为空");
                } else if (!this.book_vue){
                    alert("书籍不能为空");
                } else {
                    // 书籍保存
                    book = this.book_vue;
                    index_int = this.indexdata;
                    type_int = this.type;
                    GM_xmlhttpRequest({
                        url: host+"api/book?name=" + book,
                        method :"GET",
                        anonymous: true,
                        headers: {
                            "Content-type": "application/json",
                            "Authorization": "Token " + token
                        },
                        onload:function(xhr){
                            if (JSON.parse(xhr.responseText)["count"] == 0){
                                GM_xmlhttpRequest({
                                    url: host+"api/book",
                                    method :"POST",
                                    data:JSON.stringify({"name": book, "category": type_int, "classification": biaoqian_id ,"authur":zuozhe, "plate": bankuai_id}),
                                    dataType: "json",
                                    anonymous: true,
                                    headers: {
                                        "Content-type": "application/json",
                                        "Authorization": "Token " + token
                                    },
                                    onload:function(xhr){
                                        if (JSON.parse(xhr.responseText)['name']==book){
                                            console.log("Book",book, '储存成功');
                                            book_id = JSON.parse(xhr.responseText)["id"]
                                            zhangjiesave({"name": title, "authur":zuozhe, "index": index_int, "url": url, "collection": JSON.parse(xhr.responseText)['id'], "category": type_int, "classification": biaoqian_id , "plate": bankuai_id}, book_id)
                                            
                                        } else {
                                            console.log("Book",book, '储存失败');
                                        }
                                    }
                                })
                            } else {
                                console.log("Book",book, "已存在");
                                book_id = JSON.parse(xhr.responseText)["results"][0]["id"]
                                zhangjiesave({"name": title, "authur":zuozhe, "index": index_int, "url": url, "collection": JSON.parse(xhr.responseText)['results'][0]["id"], "category": type_int, "classification": biaoqian_id , "plate": bankuai_id}, book_id)
                            }
                        }
                    });
                }
            },
            // 收藏按钮
            shouchang(){
                GM_xmlhttpRequest({
                    url: host+"api/user_coll",
                    method :"POST",
                    data:JSON.stringify({"collection": book_id, "collect": true}),
                    dataType: "json",
                    anonymous: true,
                    headers: {
                        "Content-type": "application/json",
                        "Authorization": "Token " + token
                    },
                    onload:function(xhr){
                        if (JSON.parse(xhr.responseText)['collection']==book_id){
                            console.log("书籍", book, "加入收藏成功");
                            document.getElementById("save").remove();
                            document.getElementsByClassName("iconfont icon-bianzu24")[0].remove()
                            document.getElementsByName("modactions")[0].getElementsByTagName("h1")[0].innerHTML += '<i class="iconfont icon-yikanwan" style="color:#43CD80;font-size:75%;" title="已保存"></i>';
                        } else {
                            console.log("书籍", book, "加入收藏失败");
                        }
                    }
                })
            }
        }
    });    
    
})();