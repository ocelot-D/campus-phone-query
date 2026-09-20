<template>
  <view class="my-wrap">
    <view class="user-info">
      <image class="avatar" src="/static/tabbar/my.png"></image>
      <view class="text-box">
        <text class="name">{{ userName || '未登录' }}</text>
        <text class="stuId">学号：{{ studentId || '未登录' }}</text>
        <text class="login-type">登录身份：{{ loginType === 'student' ? '学生用户' : '管理员' }}</text>
      </view>
    </view>

    <view class="menu-list">
      <view class="menu-item" v-if="loginType === 'student'" @click="goFeedback">
        <text>提交意见反馈</text>
        <text class="arrow">›</text>
      </view>
      <view class="menu-item" v-if="loginType === 'student'" @click="goMyFeedback">
        <text>我的反馈记录</text>
        <text class="arrow">›</text>
      </view>
      <view class="menu-item" @click="showHelp">
        <text>使用说明</text>
        <text class="arrow">›</text>
      </view>
      <view class="menu-item" @click="showAbout">
        <text>关于系统</text>
        <text class="arrow">›</text>
      </view>
      <!-- 管理员专属入口 -->
      <view class="menu-item" v-if="loginType === 'admin'" @click="goAdminManage">
        <text>后台数据管理</text>
      </view>
    </view>

    <button class="logout-btn" @click="handleLogout">退出登录</button>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { LOGIN_TYPE_KEY } from '../../api/api.js'

const studentId = ref('')
const userName = ref('')
const loginType = ref('')

onMounted(() => {
  studentId.value = uni.getStorageSync('studentId') || ''
  userName.value = uni.getStorageSync('userName') || ''
  loginType.value = uni.getStorageSync(LOGIN_TYPE_KEY) || ''
  uni.$on('phoneDataChange', ()=>{})
})

const showHelp = () => {
  uni.showModal({
    title: '使用说明',
    content: '1. 首页可查看校园各部门电话，支持一键拨号和收藏；\n2. 收藏页可管理已收藏的电话；\n3. 个人中心可提交反馈、查看自己反馈处理状态；\n4. 管理员后台查看所有反馈并修改处理进度。',
    showCancel: false
  })
}

const showAbout = () => {
  uni.showModal({
    title: '关于系统',
    content: '校园电话查询小程序 v2.2\n新增学生反馈状态查看、管理员处理标记功能。',
    showCancel: false
  })
}

// 跳转提交反馈页面
const goFeedback = () => {
  uni.navigateTo({url:'/pages/feedback/feedback'})
}

// 跳转我的反馈记录页面
const goMyFeedback = () => {
  uni.navigateTo({url:'/pages/myFeedback/myFeedback'})
}

// 跳转管理后台
const goAdminManage = () => {
  uni.navigateTo({ url: '/pages/adminManage/adminManage' })
}

const handleLogout = () => {
  uni.showModal({
    title: '提示',
    content: '确定要退出登录吗？',
    success: (res) => {
      if (res.confirm) {
        uni.removeStorageSync('studentId')
        uni.removeStorageSync('userName')
        uni.removeStorageSync(LOGIN_TYPE_KEY)
        uni.reLaunch({
          url: '/pages/login/login'
        })
      }
    }
  })
}
</script>

<style scoped>
.my-wrap {
  background: #f7f8fc;
  min-height: 100vh;
}

.user-info {
  background: linear-gradient(135deg, #6474ff 0%, #818cf8 100%);
  color: #fff;
  padding: 50rpx 30rpx;
  display: flex;
  align-items: center;
  gap: 24rpx;
}

.avatar {
  width: 130rpx;
  height: 130rpx;
  border-radius: 50%;
  background: #fff;
  box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.15);
}

.text-box .name {
  font-size: 36rpx;
  display: block;
  margin-bottom: 12rpx;
  font-weight: 500;
}

.text-box .stuId {
  font-size: 28rpx;
  opacity: 0.9;
  display: block;
}
.text-box .login-type {
  font-size: 26rpx;
  margin-top: 8rpx;
  opacity: 0.8;
}

.menu-list {
  background: #fff;
  margin: 30rpx;
  border-radius: 24rpx;
  box-shadow: 0 6rpx 18rpx rgba(0,0,0,0.07);
  overflow: hidden;
}

.menu-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 36rpx 30rpx;
  border-bottom: 1rpx solid #f2f3f5;
  font-size: 30rpx;
}

.menu-item:last-child{border-bottom:none;}

.arrow {
  color: #b0b8c4;
  font-size: 36rpx;
}

.logout-btn {
  background: linear-gradient(90deg, #f43f5e, #fb7185);
  color: #fff;
  border: none;
  margin: 40rpx 30rpx;
  height: 88rpx;
  line-height: 88rpx;
  border-radius: 24rpx;
  font-size: 32rpx;
  box-shadow: 0 6rpx 16rpx rgba(244,63,94,0.25);
}

.logout-btn::after{border:none;}
</style>