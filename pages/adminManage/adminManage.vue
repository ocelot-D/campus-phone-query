<template>
  <view class="admin-wrap">
    <!-- 顶部操作按钮区 -->
    <view class="operate-box">
      <button class="btn-add" @click="goAddPage">新增电话</button>
      <button class="btn-reset" @click="handleResetData">恢复默认数据</button>
    </view>
    <view class="operate-box" style="margin-top:20rpx">
      <button class="btn-feedback" @click="goFeedbackList">查看学生反馈</button>
      <button class="btn-logout" @click="adminLogout">退出登录</button>
    </view>

    <!-- 电话列表 -->
    <scroll-view scroll-y class="phone-scroll">
      <view class="phone-item" v-for="item in phoneList" :key="item.id">
        <view class="info">
          <text class="name">{{ item.name }}</text>
          <text class="tel">{{ item.tel }}</text>
          <text class="cate">分类ID：{{ item.cateId }}</text>
          <text class="desc">{{ item.desc }}</text>
        </view>
        <view class="btn-group">
          <button size="mini" class="edit-btn" @click="goEditPage(item)">编辑</button>
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { getPhoneAll, resetDefaultPhoneData, LOGIN_TYPE_KEY } from '../../api/api.js'

let phoneList = ref([])

// 刷新列表
const refreshList = () => {
  phoneList.value = getPhoneAll()
}

// 监听全局数据变更，自动刷新
onMounted(() => {
  refreshList()
  uni.$on('phoneDataChange', refreshList)
})
onUnmounted(() => {
  uni.$off('phoneDataChange', refreshList)
})

// 跳转到新增页面
const goAddPage = () => {
  uni.navigateTo({
    url: '/pages/adminAdd/adminAdd'
  })
}

// 跳转到编辑页面，携带当前电话id
const goEditPage = (item) => {
  uni.navigateTo({
    url: `/pages/adminEdit/adminEdit?id=${item.id}`
  })
}

// 跳转反馈列表
const goFeedbackList = () => {
  uni.navigateTo({url:'/pages/adminFeedback/adminFeedback'})
}

// 管理员退出登录
const adminLogout = () => {
  uni.showModal({
    title: '退出提示',
    content: '确定退出管理员账号？',
    success: res=>{
      if(res.confirm){
        uni.removeStorageSync(LOGIN_TYPE_KEY)
        uni.reLaunch({url:'/pages/adminLogin/adminLogin'})
      }
    }
  })
}

// 恢复默认数据
const handleResetData = () => {
  uni.showModal({
    title: '警告',
    content: '确定恢复系统默认电话数据？所有新增/修改内容将被清空，不可撤销！',
    success: res => {
      if (res.confirm) {
        resetDefaultPhoneData()
        uni.showToast({ title: '已恢复默认数据' })
      }
    }
  })
}
</script>

<style scoped>
.admin-wrap {
  background: #f1f5f9;
  min-height: 100vh;
  padding: 24rpx;
}

.operate-box {
  display: flex;
  gap: 20rpx;
  margin-bottom: 30rpx;
}

.btn-add {
  flex: 1;
  height: 80rpx;
  background: #22c55e;
  color: #fff;
  border-radius: 16rpx;
}
.btn-reset {
  flex: 1;
  height: 80rpx;
  background: #ef4444;
  color: #fff;
  border-radius: 16rpx;
}
.btn-feedback {
  flex: 1;
  height: 80rpx;
  background: #1677ff;
  color: #fff;
  border-radius: 16rpx;
}
.btn-logout {
  flex: 1;
  height: 80rpx;
  background: #666;
  color: #fff;
  border-radius: 16rpx;
}
.btn-add::after,.btn-reset::after,.btn-feedback::after,.btn-logout::after{border:none;}

.phone-scroll {
  height: calc(100vh - 300rpx);
}

.phone-item {
  background: #fff;
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.name {
  font-size: 32rpx;
  font-weight: 600;
  display: block;
}
.tel {
  color: #1677ff;
  font-size: 28rpx;
  margin: 8rpx 0;
  display: block;
}
.cate {
  font-size: 24rpx;
  color: #666;
  display: block;
}
.desc {
  font-size: 24rpx;
  color: #999;
  margin-top: 8rpx;
  display: block;
}

.edit-btn {
  background: #3b82f6;
  color: #fff;
  border-radius: 12rpx;
}
</style>