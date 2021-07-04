<template>
	<view>
	     <uni-list :border="true">
	         <!-- 显示圆形头像 -->
	         <uni-list-chat v-for="i in list" :key="i.id" :avatar-circle="true" :title="i.name" avatar="/static/favicon.ico" clickable @click="todetail(i.id)"></uni-list-chat>
	     </uni-list>
	</view>
</template>

<script>
	export default {
			data() {
				return {
					next: "book",
					list: []
				}
			},
			onLoad() {
				this.getbook(this.next);
			},
			onPullDownRefresh(){
				this.next = "book"
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
				getbook(url){
					uni.request({
						url:url,
						method: "GET",
						success:(res) => {
							this.next = res.data["next"]
							var d = res.data["results"]
							for (var i = 0; i < d.length; i++) {
								this.list.push(d[i])
							}
						}
					})
				},
				Refreshgetbook(){
					if (this.next == "book"){
						this.list = []
						this.getbook("book")
					}
				},
				todetail(id){
					uni.navigateTo({
						url:"../details/details?id="+id
					})
				}
			}
		}
</script>

<style>
</style>
