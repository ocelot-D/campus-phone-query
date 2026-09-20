<template>
  <view class="wrap">
    <button class="clear-btn" v-if="list.length>0" @click="clearAll">清空全部反馈</button>
    <scroll-view scroll-y class="scroll">
      <view class="empty" v-if="list.length === 0">暂无学生反馈</view>
      <view class="item" v-for="item in list" :key="item.id">
        <view class="line"><text>学号：</text>{{item.stuId}}</view>
        <view class="line"><text>标题：</text>{{item.title}}</view>
        <view class="line"><text>内容：</text>{{item.content}}</view>
        <view class="time">{{item.time}}</view>
        <!-- 新增状态展示 -->
        <view class="status-tag" :class="getStatusClass(item.status)">
          当前状态：{{ item.status }}
        </view>
        <!-- 快捷回复/状态切换按钮 -->
        <view class="status-btn-group">
          <button size="mini" class="btn-wait" @click="setState(item.id, '等待解决')">等待解决</button>
          <button size="mini" class="btn-doing" @click="setState(item.id, '正在处理')">正在处理</button>
          <button size="mini" class="btn-done" @click="setState(item.id, '已处理')">已处理</button>
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { getFeedbackList, clearAllFeedback, changeFeedbackStatus } from '../../api/api.js'

const list = ref([])

const refresh = () => {
  list.value = getFeedbackList()
}

onMounted(() => {
  refresh()
  uni.$on('feedbackChange', refresh)
})
onUnmounted(() => {
  uni.$off('feedbackChange', refresh)
})

// 修改反馈状态
const setState = (id, status) => {
  changeFeedbackStatus(id, status)
  uni.showToast({ title: `已标记为${status}` })
}

// 清空全部反馈
const clearAll = () => {
  uni.showModal({
    title: '确认清空',
    content: '所有反馈记录将全部删除，不可恢复，确定吗？',
    success: res => {
      if(res.confirm){
        clearAllFeedback()
        uni.showToast({title:'已清空反馈'})
      }
    }
  })
}

// 根据状态返回样式类
const getStatusClass = (status) => {
  if(status === '等待解决') return 'tag-wait'
  if(status === '正在处理') return 'tag-doing'
  if(status === '已处理') return 'tag-done'
}
</script>

<style scoped>
.wrap {
  background: #f1f5f9;
  min-height: 100vh;
  padding: 24rpx;
}
.clear-btn {
  width: 100%;
  height: 76rpx;
  background: #ef4444;
  color: #fff;
  border-radius: 16rpx;
  margin-bottom: 20rpx;
}
.clear-btn::after{border:none;}
.scroll {
  height: calc(100vh - 140rpx);
}
.empty {
  text-align: center;
  padding: 100rpx 0;
  font-size: 30rpx;
  color: #999;
}
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
/* 状态标签样式 */
.status-tag {
  margin: 20rpx 0;
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
/* 状态按钮组 */
.status-btn-group {
  display: flex;
  gap: 16rpx;
  margin-top: 16rpx;
}
.btn-wait {
  background: #f59e0b;
  color: #fff;
}
.btn-doing {
  background: #3b82f6;
  color: #fff;
}
.btn-done {
  background: #22c55e;
  color: #fff;
}
.btn-wait::after,.btn-doing::after,.btn-done::after{border:none;}
</style>