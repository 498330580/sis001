<template>
	<view>
		<uni-list>
		    <uni-list-chat v-for="i in list" :key="i.id" :avatar-circle="true" :title="i.collection.name" avatar="/static/favicon.ico" clickable @click="todetail(i.collection.id)"></uni-list-chat>
			 <!-- <uni-list-chat  v-for="i in list" :key="i.id" :avatar-circle="true" :title="i.collection.name" avatar="/static/favicon.ico" clickable :note="'作者:'+i.collection.authur" @click="todetail(i.collection.id)" badge-positon="left" :badge-text="i.count?'':'dot'">
				<view class="chat-custom-right">
					<text class="chat-custom-text"></text>
					需要使用 uni-icons 请自行引入 
					<uni-icons type="star-filled" color="#999" size="18"></uni-icons>
				</view>
			</uni-list-chat> -->
		</uni-list>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				next: 'user_coll?yikan=false&collect=true',
				list: []
			}
		},
		onLoad() {
			this.getbook(this.next)
		},
		onPullDownRefresh(){
			this.next = "user_coll"
			this.Refreshgetbook();
			uni.stopPullDownRefresh();
		},
		onReachBottom(){
			if (this.next){
				this.getbook(this.next);
			} else {
				uni.showToast({
					title:"没有数据了噢"
				})
			}
		},
		methods: {
			getCollection(){
				console.log("我在运行")
			},
			getbook(url){
				uni.request({
					url:url,
					method: "GET",
					success:(res) => {
						// console.log(res.data["results"])
						this.next = res.data["next"]
						var d = res.data["results"]
						for (var i = 0; i < d.length; i++) {
							this.list.push(d[i])
						}
					}
				})
			},
			Refreshgetbook(){
				if (this.next == "user_coll"){
					this.list = []
					this.getbook("user_coll")
				}
			},
			todetail(id){
				uni.navigateTo({
					url:"../details/details?id="+id  // addbooktype  1为加入书架，0为未加入书架
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
