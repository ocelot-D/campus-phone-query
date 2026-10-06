<template>
  <view class="wrap">
    <scroll-view scroll-y class="scroll">
      <view class="empty" v-if="myFeedbackList.length === 0">
        你还没有提交过反馈，快去提交吧
        <button class="go-submit-btn" @click="goSubmitFeedback">前往提交反馈</button>
      </view>
      <view class="item" v-for="item in myFeedbackList" :key="item.id">
        <view class="line"><text>反馈内容：</text>{{ item.content }}</view>
        <view class="time">{{ item.time }}</view>
        <view class="status-tag" :class="getStatusClass(item.status)">
          当前处理状态：{{ item.status }}
        </view>
      </view>
    </scroll-view>
  </view>
</template>
<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { getFeedbackList } from '../../api/api.js'
const myFeedbackList = ref([])

const refreshMyFeedback = async () => {
  const stuId = uni.getStorageSync('studentId')
  // 直接传 stuId，后端只返回当前学生的反馈
  myFeedbackList.value = await getFeedbackList(stuId)
}

onMounted(() => {
  refreshMyFeedback()
  uni.$on('feedbackChange', refreshMyFeedback)
})
onUnmounted(() => {
  uni.$off('feedbackChange', refreshMyFeedback)
})

const goSubmitFeedback = () => {
  uni.navigateTo({ url: '/pages/feedback/feedback' })
}

const getStatusClass = (status) => {
  if (status === '等待解决') return 'tag-wait'
  if (status === '正在处理') return 'tag-doing'
  if (status === '已处理') return 'tag-done'
}
</script>
<style scoped>
.wrap {
  background: #f1f5f9;
  min-height: 100vh;
  padding: 24rpx;
}
.scroll {
  height: 100vh;
}
.empty {
  text-align: center;
  padding: 120rpx 20rpx;
  font-size: 30rpx;
  color: #666;
}
.go-submit-btn {
  margin-top: 40rpx;
  width: 60%;
  height: 76rpx;
  background: #1677ff;
  color: #fff;
  border-radius: 16rpx;
}
.go-submit-btn::after{border:none;}
.item {
  background: #fff;
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
}
.line {
  font-size: 28rpx;
  margin-bottom: 12rpx;
}
.line text {
  color: #6474ff;
  font-weight: 500;
}
.time {
  margin-top: 16rpx;
  font-size: 24rpx;
  color: #999;
}
.status-tag {
  margin-top: 20rpx;
  padding: 10rpx 20rpx;
  border-radius: 10rpx;
  font-size: 26rpx;
  width: fit-content;
}
.tag-wait {
  background: #fff3cd;
  color: #d97706;
}
.tag-doing {
  background: #dbeafe;
  color: #2563eb;
}
.tag-done {
  background: #dcfce7;
  color: #16a34a;
}
</style>
