<template>
	<view>
		<uni-list>
		    <uni-list-item v-for="(item,index) in list" :key="index" :title="item.name" note="未看" link clickable to="/pages/book/book" @click="onClick($event,1)" />
		</uni-list>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				title: 'Hello',
				list: []
			}
		},
		onLoad() {
			this.getbook()
		},
		methods: {
			// getbook(){
			// 	uni.request({
			// 		url:"http://127.0.0.1:5000/xiaosuo?type=list",
			// 		method: "GET",
			// 		header:{"Content-Type": "application/json"},
			// 		success:(res) => {
			// 			var d = res.data.data
			// 			for (var i = 0; i < d.length; i++) {
			// 				this.list.push(d[i])
			// 			}
			// 		}
			// 	})
			// },
			getbook(){
				uni.request({
					url:"http://127.0.0.1:8000/api/lishi",
					method: "GET",
					header:{"Content-Type": "application/json", "Authorization": "Token 27171cc46f6bda2668ca755810635e577f600fa4"},
					success:(res) => {
						console.log(res.data)
						// var d = res.data.data
						// for (var i = 0; i < d.length; i++) {
						// 	// this.list.push(d[i])
						// 	console.log(d[i])
						// }
					}
				})
			}

		}
	}
</script>

<style>
	.content {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
	}

	.logo {
		height: 200rpx;
		width: 200rpx;
		margin-top: 200rpx;
		margin-left: auto;
		margin-right: auto;
		margin-bottom: 50rpx;
	}

	.text-area {
		display: flex;
		justify-content: center;
	}

	.title {
		font-size: 36rpx;
		color: #8f8f94;
	}
</style>
