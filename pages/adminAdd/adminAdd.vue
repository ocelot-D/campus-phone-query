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
        <text class="label">分类</text>
        <picker mode="selector" :range="cateOptions" range-key="name" @change="onCateChange">
          <view class="picker-box">
            {{ currentCateName }}
          </view>
        </picker>
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
import { ref, computed } from 'vue'
import { addNewPhone } from '../../api/api.js'
const form = ref({
  name: '',
  tel: '',
  cateId: 1,
  desc: ''
})

// 分类选项
const cateOptions = [
  { id: 1, name: '行政办公' },
  { id: 2, name: '后勤服务' },
  { id: 3, name: '教学院系' },
  { id: 4, name: '安保医疗' }
]
const currentCateName = computed(() => {
  const item = cateOptions.find(c => c.id === form.value.cateId)
  return item ? item.name : '请选择分类'
})
const onCateChange = (e) => {
  form.value.cateId = cateOptions[e.detail.value].id
}

const goBack = () => {
  uni.navigateBack()
}

// 提交新增（加了 async）
const submitAdd = async () => {
  const data = form.value
  if (!data.name || !data.tel || !data.cateId || !data.desc) {
    uni.showToast({ title: '请填写完整信息', icon: 'none' })
    return
  }
  await addNewPhone(data)
  uni.showToast({ title: '新增成功' })
  uni.$emit('phoneDataChange')  // 通知管理后台刷新列表
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
.picker-box {
  width: 100%;
  height: 80rpx;
  line-height: 80rpx;
  background: #f7f8fc;
  border-radius: 14rpx;
  padding: 0 24rpx;
  font-size: 28rpx;
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
