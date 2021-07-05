import Vue from 'vue'
import App from './App'
// import request from 'uni.request'
import host from './common/config.js'


// 以下是页面跳转验证拦截器
uni.addInterceptor('navigateTo', {
    // 页面跳转前进行拦截, invoke根据返回值进行判断是否继续执行跳转
    invoke (args) {
		let Token = uni.getStorageSync('Authorization')
		if (!Token) {
			uni.showToast({
				title:"没有登录"
			})
			uni.reLaunch({
				url:"../login/login"
			})
			 return false
		}
		return true
    },
    success (args) {
        // console.log(e)
    }
})

// 以下是页面跳转验证拦截器
uni.addInterceptor('switchTab', {
    // tabbar页面跳转前进行拦截
    invoke (args) {
		let Token = uni.getStorageSync('Authorization')
		if (!Token) {
			uni.reLaunch({
				url:"../login/login"
			})
			 return false
		}
		return true
    },
    success (args) {
        // console.log(e)
    }
})

// 拦截器
uni.addInterceptor('request', {
  invoke(args) {
    // request 触发前拼接 url
	let Token = uni.getStorageSync('Authorization')
	if (!Token && args.url != "login") {
		uni.reLaunch({
			url:"../login/login"
		})
		 return false
	}
	let url = args.url.replace(host,"")
	args.url = host+url
	args.header = {"Content-Type": "application/json", "Authorization": Token}
	return true
  },
  success(args) {
    // 请求成功后，修改code值为1
    // console.log("拦截成功")
  }, 
  fail(err) {
    // console.log('interceptor-fail',err)
  }, 
  complete(res) {
    // console.log('interceptor-complete',res)
  }
})

Vue.config.productionTip = false

App.mpType = 'app'

const app = new Vue({
    ...App
})
app.$mount()
