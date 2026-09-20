<template>
  <view class="cate-container">
    <view class="left-cate">
      <view class="cate-item" :class="{active: activeId === item.id}" v-for="item in cateList" :key="item.id" @click="changeCate(item.id)">
        {{ item.name }}
      </view>
    </view>

    <view class="right-list">
      <view class="phone-item" v-for="item in filterPhone" :key="item.id">
        <text class="name">{{ item.name }}</text>
        <text class="tel">{{ item.tel }}</text>
        <button class="call-btn" @click="makeCall(item.tel)">拨号</button>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { getPhoneAll } from '../../api/api.js'

const activeId = ref(0)
const phoneList = ref(getPhoneAll())

const cateList = ref([
  { id: 0, name: '全部' },
  { id: 1, name: '行政办公' },
  { id: 2, name: '后勤服务' },
  { id: 3, name: '教学院系' },
  { id: 4, name: '安保医疗' }
])

// 刷新数据
const refreshData = () => {
  phoneList.value = getPhoneAll()
}
onMounted(() => {
  uni.$on('phoneDataChange', refreshData)
})
onUnmounted(() => {
  uni.$off('phoneDataChange', refreshData)
})

const filterPhone = computed(() => {
  if (activeId.value === 0) return phoneList.value
  return phoneList.value.filter(item => item.cateId === activeId.value)
})

const changeCate = (id) => {
  activeId.value = id
}

const makeCall = (tel) => {
  uni.makePhoneCall({ phoneNumber: tel })
}
</script>

<style scoped>
.cate-container {
  display: flex;
  height: 100vh;
  background: #f7f8fc;
}

.left-cate {
  width: 200rpx;
  background: #ffffff;
  box-shadow: 2rpx 0 10rpx rgba(0,0,0,0.05);
}

.cate-item {
  height: 88rpx;
  line-height: 88rpx;
  text-align: center;
  font-size: 28rpx;
  color: #555;
}

.cate-item.active {
  background: linear-gradient(90deg, #6474ff, #818cf8);
  color: #fff;
}

.right-list {
  flex: 1;
  padding: 24rpx;
}

.phone-item {
  background: #fff;
  padding: 26rpx;
  border-radius: 24rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 6rpx 18rpx rgba(0,0,0,0.07);
}

.name {
  font-size: 32rpx;
  display: block;
  color: #222;
  font-weight: 500;
}

.tel {
  color: #6474ff;
  margin: 12rpx 0;
  display: block;
  font-size: 28rpx;
  font-weight: 500;
}

.call-btn {
  width: 150rpx;
  height: 56rpx;
  line-height: 56rpx;
  background: linear-gradient(90deg, #22c55e, #4ade80);
  color: #fff;
  font-size: 26rpx;
  padding: 0;
  margin: 0;
  border-radius: 18rpx;
  box-shadow: 0 4rpx 10rpx rgba(34,197,94,0.25);
}

.call-btn::after{border:none;}
</style>