// @require      https://cdn.jsdelivr.net/npm/jquery@3.4.1/dist/jquery.slim.min.js

(function () {
    // 'use strict';   //严格模式

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
        if (url_zz.test(url)) {
            return true
        } else {
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
                        console.log(url_bankuai)
                        if (xiaosuo(url_bankuai)) {
                            console.log("已识别")
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

    // 标签保存（返回章节ID）
    function biaoqiansave() {
        let biaoqian = document.getElementsByName("modactions")[0].getElementsByTagName("h1")[0].getElementsByTagName("a")[0].innerText
        biaoqian = biaoqian.replace('[', '')
        biaoqian = biaoqian.replace(']', '')
        console.log(biaoqian);
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
                                return JSON.parse(xhr.responseText)["id"]
                            } else {
                                console.log("标签", biaoqian, "保存失败");
                                return null
                            }
                        }
                    })
                } else {
                    console.log("标签", biaoqian, "已存在");
                    return JSON.parse(xhr.responseText)["results"][0]['id'];
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
                                return JSON.parse(xhr.responseText)["id"]
                            } else {
                                console.log("版块", bankuai, "保存失败");
                                return null
                            }
                        }
                    })
                } else {
                    console.log("版块", bankuai, "已存在");
                    return JSON.parse(xhr.responseText)["results"][0]['id'];
                }
            },
            // onerror: function(e) {
            //     console.log("标签错误：", e);
            //     return null;
            // }
        })
    }

    // 详情页编辑
    function xiangqing() {
        let h1 = document.getElementsByName("modactions")[0].getElementsByTagName("h1")[0];
        let url = window.location.href;
        let a = document.getElementById("nav").getElementsByTagName("a")
        let url_bankuai = a[a.length-1].href
        let bankuai = a[a.length-1].innerText
        
        bankuai_id = bankuaisave(bankuai)
        biaoqian_id = biaoqiansave()

        if (xiaosuo(url_bankuai)) {
        document.getElementById("foruminfo").innerHTML += `<br><div id="save" style="border: 2px solid lightblue;text-align:center;border-style: outset;background-color: lightblue;padding: 5px;">
        <i class="iconfont icon-leibie" title="保存的数据类别">类别：</i>
        <select name="public-choice" v-model="type" style="width:149px;height:25px;text-align:center;text-align-last:center;"><option :value="coupon.id" v-for="coupon in typelist">{{coupon.name}}</option></select>
        <i class="iconfont icon-xuhao" title="建议填写当前的开始章号">序号:</i>
        <input type="number" v-model="indexdata" style="text-align:center;text-align-last:center;">
        <i class="iconfont icon-book" title="想要收集到那本书下面">书籍：</i>
        <input type="text"v-model="book"style="width:200x;">
        <button class="iconfont icon-baocun" style="font-size:100%;" @click="savexiapsuo(`+biaoqian_id+','+bankuai_id+`)">提交</button>
        </div>`}
        // 浏览状态判断
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

                    if (xiaosuo(url_bankuai)) {
                        if (xs) {
                            h1.innerHTML += '<i class="iconfont icon-yikanwan" style="color:#43CD80;font-size:75%;" title="已保存"></i>';
                            document.getElementById("save").remove();
                        } else {
                            h1.innerHTML += '<i class="iconfont icon-bianzu24" style="color:#000000;font-size:75%;" title="未保存"></i>';
                        }
                    }

                    if (ls) {
                        h1.innerHTML += '<i class="iconfont icon-yikan" style="color:#43CD80;font-size:75%;" title="已浏览"></i>';
                        console.log("浏览记录已存在");
                    } else {
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
                                // console.log(JSON.parse(xhr.responseText));
                                // console.log(xhr.responseText);
                                if (JSON.parse(xhr.responseText)["url"] == url) {
                                    h1.innerHTML += '<i class="iconfont icon-yikan" style="color:#43CD80;font-size:75%;" title="已浏览"></i>';
                                    console.log("浏览记录保存成功");
                                } else {
                                    h1.innerHTML += '<i class="iconfont icon-weikan" style="color:#000000;font-size:75%;" title="未浏览"></i>';
                                }
                            }
                        });
                    }
                } else {
                    console.log("错误，未传递URL");
                }
            }
        });

        // console.log(document.getElementsByName("modactions")[0].getElementsByTagName("h1")[0].innerText);
        return document.getElementsByName("modactions")[0].getElementsByTagName("h1")[0]
    }

    // 章节储存
    function zhangjiesave(data) {
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
    // var book_id = 1;    //小说书籍储存ID
    var index_int = 0;  //小说章节索引
    var type_int = 0;   //小说章节类型
    var bankuai_id = null;  //版块ID
    var biaoqian_id = null;  //标签ID
    var url_zz = /^http.*?forum.*/ig;
    if (url_zz.test(url)) {
        document.getElementsByTagName("head")[0].innerHTML += '<link rel="stylesheet" href="//at.alicdn.com/t/font_2616980_8iw3dgaotf4.css">';
        // document.getElementsByTagName("head")[0].innerHTML += `<link rel="stylesheet" href="https://unpkg.com/element-plus/lib/theme-chalk/index.css">`;
        ad_del();
        let search_list_zz = /^http.*?search.*/ig
        if (search_list_zz.test(url)) {
            if (!document.getElementsByName("searchsubmit").length) {
                search();
            } else {
                console.log("当前是搜索页");
            }
        } else {
            let thread_zz = /^http.*?thread.*/
            if (!thread_zz.test(url)) {
                list();
            } else {
                title = xiangqing();
            }
            
        }
    }

    /*Vue操作*/
    var app = new Vue({
        el: "#save",
        data: {
            typelist: [
                {id: 0, name: "无"},
                {id: 1, name: "小说"},
                {id: 2, name: "图片"},
            ],
            type: 0,
            book: "",
            indexdata: 1
        }, methods: {
            // 保存按钮
            savexiapsuo(bq,bk){
                if (!this.type) {
                    alert("类型不能为空");
                } else if (!this.book){
                    alert("书籍不能为空");
                } else {
                    // 书籍保存
                    book = this.book;
                    index_int = this.indexdata;
                    type_int = this.type;
                    bankuai_id = bk;
                    biaoqian_id = bq;
                    console.log(bk, bq);
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
                                    data:JSON.stringify({"name": book, "category": type_int, "classification": biaoqian_id , "plate": bankuai_id}),
                                    dataType: "json",
                                    anonymous: true,
                                    headers: {
                                        "Content-type": "application/json",
                                        "Authorization": "Token " + token
                                    },
                                    onload:function(xhr){
                                        if (JSON.parse(xhr.responseText)['name']==book){
                                            console.log("Book",book, '储存成功');
                                            // book_id = JSON.parse(xhr.responseText)['id']
                                            zhangjiesave({"name": title.innerText, "index": index_int, "url": url, "collection": JSON.parse(xhr.responseText)['id'], "category": type_int, "classification": biaoqian_id , "plate": bankuai_id})
                                            
                                        } else {
                                            console.log("Book",book, '储存失败');
                                        }
                                    }
                                })
                            } else {
                                console.log("Book",book, "已存在");
                                // book_id = JSON.parse(xhr.responseText)["results"][0]['id']
                                zhangjiesave({"name": title.innerText, "index": index_int, "url": url, "collection": JSON.parse(xhr.responseText)['id'], "category": type_int, "classification": biaoqian_id , "plate": bankuai_id})
                            }
                        }
                    });
                }
            }
        }
    });
    
})();