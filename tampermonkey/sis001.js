(function () {
    'use strict';   //严格模式

    var host = "http://127.0.0.1:5000/"

    // function dj(url) {
    //     alert(url);
    // }

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
                                    url:host + "xiaosuo?type=xiaosuo-lishi&url=" + get_url,
                                    method: "GET",
                                    headers: {
                                        "Content-type": "application/json"
                                    },
                                    onload:function(xhr){
                                        let data = JSON.parse(xhr.responseText)
                                        if (data["mess"]!= "错误，未传递URL") {
                                            let xs = data["data"]["xiaosuo"]
                                            let ls = data["data"]["lishi"]
                                            if (xs) {
                                                a_data.innerHTML += '<i class="iconfont icon-yikanwan" style="color:#43CD80;font-size:75%;" title="已保存"></i>';
                                            } else {
                                                a_data.innerHTML += '<i class="iconfont icon-bianzu24" style="color:#000000;font-size:75%;" title="未保存"></i>';
                                            }
                                            if (ls) {
                                                a_data.innerHTML += '<i class="iconfont icon-yikan"" style="color:#43CD80;font-size:75%;" title="已浏览"></i>';
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
            let th = tbody.getElementsByTagName("th")[0]
            let a = th.getElementsByTagName("a")[0]
            let url = a.href
            // let text = a.innerText
            // console.log(url, text);
            GM_xmlhttpRequest({
                url:host + "xiaosuo?type=xiaosuo-lishi&url=" + url,
                method: "GET",
                headers: {
                    "Content-type": "application/json"
                },
                onload:function(xhr){
                    let data = JSON.parse(xhr.responseText)
                    if (data["mess"]!= "错误，未传递URL") {
                        let xs = data["data"]["xiaosuo"]
                        let ls = data["data"]["lishi"]
                        if (xs) {
                            a.innerHTML += '<i class="iconfont icon-yikanwan" style="color:#43CD80;font-size:75%;" title="已保存"></i>';
                        } else {
                            a.innerHTML += '<i class="iconfont icon-bianzu24" style="color:#000000;font-size:75%;" title="未保存"></i>';
                        }
                        if (ls) {
                            a.innerHTML += '<i class="iconfont icon-yikan"" style="color:#43CD80;font-size:75%;" title="已浏览"></i>';
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

    // 详情页编辑
    function xiangqing() {
        let h1 = document.getElementsByName("modactions")[0].getElementsByTagName("h1")[0];
        let url = window.location.href;
        document.getElementById("foruminfo").innerHTML += `<br><div id="save" style="border: 2px solid lightblue;text-align:center;border-style: outset;background-color: lightblue;padding: 5px;">
        <i class="iconfont icon-leibie" title="保存的数据类别">类别：</i>
        <select name="public-choice" v-model="type" style="width:149px;height:25px;text-align:center;text-align-last:center;"><option :value="coupon.id" v-for="coupon in typelist">{{coupon.name}}</option></select>
        <i class="iconfont icon-xuhao" title="建议填写当前的开始章号">序号:</i>
        <input type="number" v-model="indexdata" style="text-align:center;text-align-last:center;">
        <i class="iconfont icon-book" title="想要收集到那本书下面">书籍：</i>
        <input type="text"v-model="book"style="width:200x;">
        <button class="iconfont icon-baocun" style="font-size:100%;" @click="savexiapsuo()">提交</button>
        </div>`
        GM_xmlhttpRequest({
            url:host + "xiaosuo?type=xiaosuo-lishi&url=" + url,
            method: "GET",
            headers: {
                "Content-type": "application/json"
            },
            onload:function(xhr){
                let data = JSON.parse(xhr.responseText)
                if (data["mess"]!= "错误，未传递URL") {
                    let xs = data["data"]["xiaosuo"]
                    let ls = data["data"]["lishi"]
                    if (xs) {
                        h1.innerHTML += '<i class="iconfont icon-yikanwan" style="color:#43CD80;font-size:75%;" title="已保存"></i>';
                        document.getElementById("save").remove();
                    } else {
                        h1.innerHTML += '<i class="iconfont icon-bianzu24" style="color:#000000;font-size:75%;" title="未保存"></i>';
                    }
                    if (ls) {
                        h1.innerHTML += '<i class="iconfont icon-yikan" style="color:#43CD80;font-size:75%;" title="已浏览"></i>';
                    } else {
                        GM_xmlhttpRequest({
                            url:host + "xiaosuo?type=lishi",
                            method :"POST",
                            data:JSON.stringify({"type": "小说", "title": title, "url": url}),
                            dataType: "json",
                            headers: {
                                "Content-type": "application/json"
                            },
                            onload:function(xhr){
                                console.log("浏览记录保存成功");
                                if (JSON.parse(xhr.responseText)["mess"] == "创建成功") {
                                    h1.innerHTML += '<i class="iconfont icon-yikan" style="color:#43CD80;font-size:75%;" title="已浏览"></i>';
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
        return document.getElementsByName("modactions")[0].getElementsByTagName("h1")[0].innerText
    }

    console.log("sis001脚本运行")
    var url = window.location.href;
    var title = "";
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
                {id: "小说", name: "小说"}
            ],
            type: "",
            book: "",
            indexdata: 1
        }, methods: {
            savexiapsuo(){
                // console.log({"type": this.type, "book": this.book, "index": this.indexdata, "title": title, "url": url});
                if (!this.type) {
                    alert("类型不能为空");
                } else if (!this.book){
                    alert("书籍不能为空");
                } else {
                    GM_xmlhttpRequest({
                        url:host + "xiaosuo?type=xiaosuo",
                        method :"POST",
                        data:JSON.stringify({"type": this.type, "book": this.book, "index": this.indexdata, "title": title, "url": url, "爬取状态": "未爬取", "下载状态": "未下载", "内容": ""}),
                        dataType: "json",
                        headers: {
                            "Content-type": "application/json"
                        },
                        onload:function(xhr){
                            // console.log(JSON.parse(xhr.responseText));
                            if (JSON.parse(xhr.responseText)["mess"] == "创建成功") {
                                alert("保存成功！");
                                document.getElementById("save").remove();
                                document.getElementsByClassName("iconfont icon-bianzu24")[0].remove()
                                document.getElementsByName("modactions")[0].getElementsByTagName("h1")[0].innerHTML += '<i class="iconfont icon-yikanwan" style="color:#43CD80;font-size:75%;" title="已保存"></i>';
                            } else {
                                alert("保存失败！");
                            }
                        }
                    });
                }
            }
        }
    });
    
})();