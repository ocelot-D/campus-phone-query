<template>
  <view class="form-wrap">
    <view class="form-card">
      <view class="form-item">
        <text class="label">部门名称</text>
        <input v-model="form.name" placeholder="请输入部门名称" />
      </view>
      <view class="form-item">
        <text class="label">联系电话</text>
        <input v-model="form.tel" placeholder="020-xxxxxxx" />
      </view>
      <view class="form-item">
        <text class="label">分类ID(1行政/2后勤/3院系/4安保)</text>
        <input v-model.number="form.cateId" type="number" placeholder="输入数字1-4" />
      </view>
      <view class="form-item">
        <text class="label">简介描述</text>
        <textarea v-model="form.desc" placeholder="填写业务说明"></textarea>
      </view>

      <view class="btn-box">
        <button class="cancel-btn" @click="goBack">取消</button>
        <button class="submit-btn" @click="submitAdd">保存新增</button>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'
import { addNewPhone } from '../../api/api.js'

const form = ref({
  name: '',
  tel: '',
  cateId: 1,
  desc: ''
})

// 返回管理后台
const goBack = () => {
  uni.navigateBack()
}

// 提交新增
const submitAdd = () => {
  const data = form.value
  if (!data.name || !data.tel || !data.cateId || !data.desc) {
    uni.showToast({ title: '请填写完整信息', icon: 'none' })
    return
  }
  addNewPhone(data)
  uni.showToast({ title: '新增成功' })
  setTimeout(() => {
    uni.navigateBack()
  }, 800)
}
</script>

<style scoped>
.form-wrap {
  background: #f1f5f9;
  min-height: 100vh;
  padding: 30rpx;
}
.form-card {
  background: #fff;
  border-radius: 24rpx;
  padding: 40rpx 30rpx;
}
.form-item {
  margin-bottom: 30rpx;
}
.label {
  display: block;
  font-size: 28rpx;
  color: #333;
  margin-bottom: 12rpx;
}
.form-item input, .form-item textarea {
  width: 100%;
  height: 80rpx;
  background: #f7f8fc;
  border-radius: 14rpx;
  padding: 0 24rpx;
  font-size: 28rpx;
}
.form-item textarea {
  height: 140rpx;
}
.btn-box {
  display: flex;
  gap: 24rpx;
  margin-top: 60rpx;
}
.cancel-btn {
  flex: 1;
  height: 86rpx;
  background: #e5e7eb;
  color: #333;
  border-radius: 18rpx;
}
.submit-btn {
  flex: 1;
  height: 86rpx;
  background: #22c55e;
  color: #fff;
  border-radius: 18rpx;
}
.cancel-btn::after,.submit-btn::after{border:none;}
</style>