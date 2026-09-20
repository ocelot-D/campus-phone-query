<template>
  <view class="content">
    <view class="empty" v-if="collectList.length === 0">
      <text class="empty-text">暂无收藏数据</text>
      <text class="empty-desc">去首页添加你需要的电话吧~</text>
    </view>
    <view class="list-item" v-for="item in collectList" :key="item.id">
      <view class="info">
        <view class="name">{{ item.name }}</view>
        <view class="tel">{{ item.tel }}</view>
        <view class="desc">{{ item.desc }}</view>
      </view>
      <view class="btn-group">
        <button size="mini" class="call-btn" @click="callPhone(item.tel)">拨号</button>
        <button size="mini" class="cancel-btn" @click="cancelCollect(item.id)">取消</button>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { getCollectList, delCollect } from '../../api/api.js'

const collectList = ref([])

const refreshList = () => {
  collectList.value = getCollectList()
}

onMounted(() => {
  refreshList()
  uni.$on('collectChange', refreshList)
})

onUnmounted(() => {
  uni.$off('collectChange', refreshList)
})

const callPhone = (tel) => {
  uni.makePhoneCall({ phoneNumber: tel })
}

const cancelCollect = (id) => {
  delCollect(id)
  refreshList()
  uni.showToast({ title: '已取消收藏' })
}
</script>

<style scoped>
.content {
  padding: 24rpx;
  background: #f7f8fc;
  min-height: 100vh;
}

.empty {
  text-align: center;
  padding: 120rpx 0;
}

.empty-text {
  font-size: 30rpx;
  color: #999;
  display: block;
  margin-bottom: 10rpx;
}

.empty-desc {
  font-size: 26rpx;
  color: #bbb;
}

.list-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #fff;
  padding: 30rpx;
  margin-bottom: 20rpx;
  border-radius: 24rpx;
  box-shadow: 0 6rpx 18rpx rgba(0,0,0,0.07);
}

.name {
  font-size: 32rpx;
  font-weight: 600;
  color: #222;
}

.tel {
  font-size: 28rpx;
  color: #6474ff;
  margin: 10rpx 0;
  font-weight: 500;
}

.desc {
  font-size: 24rpx;
  color: #999;
}

.btn-group {
  display: flex;
  gap: 16rpx;
}

.call-btn {
  background: linear-gradient(90deg, #22c55e, #4ade80);
  color: #fff;
  border-radius: 16rpx;
}

.cancel-btn {
  background: linear-gradient(90deg, #f43f5e, #fb7185);
  color: #fff;
  border-radius: 16rpx;
}
</style>