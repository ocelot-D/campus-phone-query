<template>
  <view class="wrap">
    <view class="card">
      <view class="form-item">
        <text class="label">你的学号</text>
        <input v-model="stuId" disabled placeholder="自动填充登录学号" />
      </view>
      <view class="form-item">
        <text class="label">反馈标题</text>
        <input v-model="title" placeholder="简要描述问题" />
      </view>
      <view class="form-item">
        <text class="label">详细反馈内容</text>
        <textarea v-model="content" placeholder="请详细描述你的建议或问题" />
      </view>
      <button class="submit-btn" @click="submit">提交反馈</button>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { submitFeedback } from '../../api/api.js'

const stuId = ref('')
const title = ref('')
const content = ref('')

onMounted(() => {
  // 自动读取当前登录学号
  stuId.value = uni.getStorageSync('studentId')
})

const submit = () => {
  if (!title.value || !content.value) {
    uni.showToast({ title: '标题和内容不能为空', icon: 'none' })
    return
  }
  submitFeedback({
    stuId: stuId.value,
    title: title.value,
    content: content.value
  })
  uni.showToast({ title: '反馈提交成功！' })
  setTimeout(() => uni.navigateBack(), 1000)
}
</script>

<style scoped>
.wrap {
  background: #f1f5f9;
  min-height: 100vh;
  padding: 30rpx;
}
.card {
  background: #fff;
  border-radius: 24rpx;
  padding: 40rpx 30rpx;
}
.form-item {
  margin-bottom: 36rpx;
}
.label {
  display: block;
  font-size: 28rpx;
  color: #333;
  margin-bottom: 12rpx;
}
input, textarea {
  width: 100%;
  background: #f7f8fc;
  border-radius: 14rpx;
  padding: 0 24rpx;
  font-size: 28rpx;
}
input {
  height: 80rpx;
}
textarea {
  height: 200rpx;
  padding-top: 20rpx;
}
.submit-btn {
  width: 100%;
  height: 86rpx;
  background: #1677ff;
  color: #fff;
  border-radius: 18rpx;
  font-size: 30rpx;
}
.submit-btn::after {border:none;}
</style>