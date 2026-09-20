<template>
  <view class="login-box">
    <view class="login-card">
      <view class="title">管理员后台登录</view>
      <view class="subtitle">校园电话数据管理系统</view>

      <view class="form-item">
        <text class="label">管理员账号</text>
        <input class="input-box" v-model="adminId" placeholder="请输入管理员账号" />
      </view>

      <view class="form-item pwd-wrap">
        <text class="label">登录密码</text>
        <input 
          class="input-box" 
          v-model="password" 
          :password="!pwdVisible" 
          placeholder="请输入登录密码" 
        />
        <view class="pwd-btn" @click="togglePwd">
          {{ pwdVisible ? '隐藏' : '显示' }}
        </view>
      </view>

      <button class="login-btn" @click="handleAdminLogin">登录后台</button>
      <view class="split-line"></view>
      <view class="tip" @click="goStudentLogin">学生用户？前往学生登录</view>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'
import { checkAdminLogin, LOGIN_TYPE_KEY } from '../../api/api.js'

const adminId = ref('')
const password = ref('')
const pwdVisible = ref(false)

const togglePwd = () => {
  pwdVisible.value = !pwdVisible.value
}

const handleAdminLogin = () => {
  if (!adminId.value || !password.value) {
    uni.showToast({ title: '请输入账号密码', icon: 'none' })
    return
  }
  let res = checkAdminLogin(adminId.value, password.value)
  if (res.success) {
    uni.showToast({ title: '管理员登录成功', icon: 'success' })
    // 存储登录身份为管理员
    uni.setStorageSync(LOGIN_TYPE_KEY, 'admin')
    setTimeout(() => {
      uni.reLaunch({ url: '/pages/adminManage/adminManage' })
    }, 800)
  } else {
    uni.showToast({ title: res.msg, icon: 'none' })
  }
}

// 跳转学生登录
const goStudentLogin = () => {
  uni.navigateTo({ url: '/pages/login/login' })
}
</script>

<style scoped>
.login-box {
  min-height: 100vh;
  background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0 40rpx;
}

.login-card {
  width: 100%;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10rpx);
  border-radius: 32rpx;
  padding: 80rpx 50rpx;
  box-shadow: 0 10rpx 30rpx rgba(0,0,0,0.3);
}

.title {
  font-size: 44rpx;
  font-weight: 700;
  text-align: center;
  color: #1e293b;
  margin-bottom: 12rpx;
}

.subtitle {
  font-size: 26rpx;
  color: #666;
  text-align: center;
  margin-bottom: 60rpx;
}

.form-item {
  margin-bottom: 30rpx;
}

.pwd-wrap {
  position: relative;
}

.label {
  display: block;
  font-size: 26rpx;
  color: #333;
  margin-bottom: 10rpx;
  font-weight: 500;
}

.input-box {
  width: 100%;
  height: 90rpx;
  background: #f1f5f9;
  border-radius: 20rpx;
  padding: 0 110rpx 0 30rpx;
  font-size: 28rpx;
  border: 1rpx solid #cbd5e1;
}

.pwd-btn {
  position: absolute;
  right: 30rpx;
  bottom: 24rpx;
  font-size: 26rpx;
  color: #1677ff;
  padding: 0 10rpx;
}

.login-btn {
  width: 100%;
  height: 90rpx;
  line-height: 90rpx;
  background: linear-gradient(90deg, #1e40af, #3b82f6);
  color: #fff;
  border-radius: 20rpx;
  font-size: 30rpx;
  font-weight: 600;
  margin-top: 20rpx;
  box-shadow: 0 6rpx 18rpx rgba(59,130,246,0.3);
}

.login-btn::after {
  border: none;
}

.split-line {
  height: 1rpx;
  background: #e2e8f0;
  margin: 40rpx 0;
}

.tip {
  text-align: center;
  color: #1677ff;
  font-size: 26rpx;
}
</style>