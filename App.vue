<template>
  <div>
    <router-view />
  </div>
</template>

<script setup>
import { LOGIN_TYPE_KEY } from './api/api.js'
// 全局页面显示时校验登录状态
uni.onShow(() => {
  const loginType = uni.getStorageSync(LOGIN_TYPE_KEY)
  const pages = getCurrentPages()
  if (pages.length === 0) return
  const currentPage = pages[pages.length - 1].route

  // 管理员页面校验
  if (currentPage.startsWith('pages/adminManage')) {
    if (loginType !== 'admin') {
      uni.reLaunch({ url: '/pages/adminLogin/adminLogin' })
      return
    }
  }

  // 学生tab页面校验
  const studentPages = [
    'pages/index/index',
    'pages/category/category',
    'pages/collect/collect',
    'pages/my/my'
  ]
  if (studentPages.includes(currentPage)) {
    if (loginType !== 'student') {
      uni.reLaunch({ url: '/pages/login/login' })
    }
  }
})
</script>

<style lang="scss">
/* 全局样式初始化 */
page {
  font-size: 28rpx;
  background-color: #f5f5f5;
  margin: 0;
  padding: 0;
}
view, text, image, input {
  box-sizing: border-box;
}
/* 通用间距类 */
.p-20 {
  padding: 20rpx;
}
.mt-20 {
  margin-top: 20rpx;
}
</style>