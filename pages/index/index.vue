<template>
  <view class="container">
    <!-- 搜索栏 -->
    <view class="search-box">
      <input class="search-input" placeholder="输入名称/号码查询" v-model="searchVal" />
      <button class="search-btn" @click="searchPhone">搜索</button>
    </view>

    <!-- 分类标签 -->
    <view class="cate-wrap">
      <view class="cate-item" :class="{active: activeCate === item.id}" v-for="item in cateList" :key="item.id" @click="switchCate(item.id)">
        {{ item.name }}
      </view>
    </view>

    <!-- 电话列表 -->
    <view class="phone-list">
      <view class="phone-item" v-for="item in showList" :key="item.id">
        <view class="phone-info">
          <text class="name">{{ item.name }}</text>
          <text class="tel">{{ item.tel }}</text>
          <text class="desc">{{ item.desc }}</text>
        </view>
        <view class="btn-group">
          <button class="call-btn" @click="makeCall(item.tel)">拨号</button>
          <button class="collect-btn" @click="handleAddCollect(item)">收藏</button>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { getPhoneAll, addCollect as addCollectApi } from '../../api/api.js'

const searchVal = ref('')
const activeCate = ref(0)
const phoneList = ref(getPhoneAll())

const cateList = ref([
  { id: 0, name: '全部' },
  { id: 1, name: '行政办公' },
  { id: 2, name: '后勤服务' },
  { id: 3, name: '教学院系' },
  { id: 4, name: '安保医疗' }
])

// 刷新电话列表
const refreshPhone = () => {
  phoneList.value = getPhoneAll()
}

onMounted(() => {
  uni.$on('phoneDataChange', refreshPhone)
})
onUnmounted(() => {
  uni.$off('phoneDataChange', refreshPhone)
})

const showList = computed(() => {
  let list = phoneList.value
  if (activeCate.value !== 0) {
    list = list.filter(item => item.cateId === activeCate.value)
  }
  if (searchVal.value) {
    let key = searchVal.value.toLowerCase()
    list = list.filter(item =>
      item.name.toLowerCase().includes(key) ||
      item.tel.includes(key)
    )
  }
  return list
})

const switchCate = (id) => {
  activeCate.value = id
}

const makeCall = (tel) => {
  uni.makePhoneCall({ phoneNumber: tel })
}

const handleAddCollect = (item) => {
  let res = addCollectApi(item)
  if (res) {
    uni.showToast({ title: '收藏成功', icon: 'success' })
    uni.$emit('collectChange')
  } else {
    uni.showToast({ title: '已收藏', icon: 'none' })
  }
}
</script>

<style scoped>
.container {
  padding: 24rpx;
  background: #f7f8fc;
  min-height: 100vh;
}

/* 搜索栏 */
.search-box {
  display: flex;
  gap: 16rpx;
  margin-bottom: 24rpx;
}

.search-input {
  flex: 1;
  height: 84rpx;
  padding: 0 30rpx;
  background: #fff;
  border-radius: 24rpx;
  box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.06);
  font-size: 28rpx;
}

.search-btn {
  width: 130rpx;
  height: 84rpx;
  line-height: 84rpx;
  background: linear-gradient(90deg, #6474ff, #818cf8);
  color: #fff;
  font-size: 28rpx;
  border-radius: 24rpx;
  box-shadow: 0 4rpx 12rpx rgba(100,116,255,0.25);
}

.search-btn::after{border:none;}

/* 分类标签 */
.cate-wrap {
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx;
  margin-bottom: 24rpx;
}

.cate-item {
  padding: 12rpx 28rpx;
  background: #fff;
  border-radius: 30rpx;
  font-size: 26rpx;
  box-shadow: 0 4rpx 12rpx rgba(0,0,0,0.06);
  color: #666;
}

.cate-item.active {
  background: linear-gradient(90deg, #6474ff, #818cf8);
  color: #fff;
  box-shadow: 0 4rpx 12rpx rgba(100,116,255,0.25);
}

/* 电话列表项 */
.phone-item {
  background: #fff;
  border-radius: 24rpx;
  box-shadow: 0 6rpx 20rpx rgba(0,0,0,0.08);
  padding: 30rpx;
  margin-bottom: 20rpx;
  display: flex;
  justify-content: space-between;
}

.name {
  font-size: 32rpx;
  font-weight: 600;
  display: block;
  margin-bottom: 10rpx;
  color: #222;
}

.tel {
  color: #6474ff;
  display: block;
  margin-bottom: 10rpx;
  font-size: 28rpx;
  font-weight: 500;
}

.desc {
  color: #999;
  font-size: 24rpx;
}

.btn-group {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.call-btn,
.collect-btn {
  width: 106rpx;
  height: 54rpx;
  line-height: 54rpx;
  font-size: 24rpx;
  border-radius: 16rpx;
}

.call-btn::after,.collect-btn::after{border:none;}

.call-btn {
  background: linear-gradient(90deg, #22c55e, #4ade80);
  color: #fff;
  box-shadow: 0 4rpx 10rpx rgba(34,197,94,0.25);
}

.collect-btn {
  background: linear-gradient(90deg, #f43f5e, #fb7185);
  color: #fff;
  box-shadow: 0 4rpx 10rpx rgba(244,63,94,0.25);
}
</style>