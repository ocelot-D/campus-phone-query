<template>
  <view class="login-box">
    <view class="login-card">
      <view class="title">校园电话查询【学生登录】</view>
      <view class="subtitle">随时随地，一键直达</view>

      <!-- 学号 -->
      <view class="form-item">
        <text class="label">学号</text>
        <input 
          class="input-box" 
          v-model="stuId" 
          placeholder="请输入学号"
          @input="checkStu"
        />
        <text v-if="stuTip" class="err-tip">{{ stuTip }}</text>
      </view>

      <!-- 密码 -->
      <view class="form-item pwd-wrap">
        <text class="label">密码</text>
        <input
          class="input-box"
          v-model="password"
          :password="!pwdVisible"
          placeholder="请输入登录密码"
          @input="checkPwd"
        />
        <view class="pwd-btn" @click="togglePwd">
          {{ pwdVisible ? '隐藏' : '显示' }}
        </view>
        <text v-if="pwdTip" class="err-tip">{{ pwdTip }}</text>
      </view>

      <button class="login-btn" @click="handleLogin">登录</button>
      <view class="tip" @click="goRegister">还没有账号？去注册</view>
      <view class="split-line"></view>
      <view class="admin-entry" @click="goAdminLogin">管理员入口</view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { checkLogin, LOGIN_TYPE_KEY } from '../../api/api.js'

const stuId = ref('')
const password = ref('')
const pwdVisible = ref(false)

// 实时提示文本
const stuTip = ref('')
const pwdTip = ref('')

const stuReg = /^\d+$/
const pwdReg = /^(?=.*[0-9])(?=.*[a-zA-Z]).{6,18}$/

const togglePwd = () => {
  pwdVisible.value = !pwdVisible.value
}

// 实时校验学号
const checkStu = () => {
  if (!stuId.value) {
    stuTip.value = ''
    return
  }
  if(stuReg.test(stuId.value)){
    stuTip.value = ''
  }else{
    stuTip.value = '请输入纯数字！'
  }
}

// 实时校验密码
const checkPwd = () => {
  if (!password.value) {
    pwdTip.value = ''
    return
  }
  if(pwdReg.test(password.value)){
    pwdTip.value = ''
  }else{
    pwdTip.value = '密码6-18位，需同时包含数字和字母'
  }
}

onMounted(() => {
  const id = uni.getStorageSync('studentId')
  if (id) uni.switchTab({ url: '/pages/index/index' })
})

const handleLogin = () => {
  // 重新执行一次实时校验，同步清空合法输入的提示
  checkStu()
  checkPwd()

  // 空值判断
  if (!stuId.value || !password.value) {
    uni.showModal({ title:'提示',content:'学号密码不能为空',showCancel:false })
    return
  }
  // 只有存在错误提示才拦截登录
  if (stuTip.value || pwdTip.value) {
    uni.showModal({ title:'提示',content:'请修正输入格式',showCancel:false })
    return
  }
  // 校验全部通过，执行登录接口
  let res = checkLogin(stuId.value, password.value)
  if (res.success) {
    uni.showToast({ title: '登录成功', icon: 'success' })
    uni.setStorageSync('studentId', stuId.value)
    uni.setStorageSync('userName', res.user.userName)
    uni.setStorageSync(LOGIN_TYPE_KEY, 'student')
    setTimeout(() => uni.switchTab({ url: '/pages/index/index' }), 800)
  } else {
    uni.showModal({ title:'登录失败',content:res.msg,showCancel:false })
  }
}

const goRegister = () => uni.navigateTo({ url: '/pages/register/register' })
const goAdminLogin = () => uni.navigateTo({ url: '/pages/adminLogin/adminLogin' })
</script>

<style scoped>
.login-box {
  min-height: 100vh;
  background: linear-gradient(135deg, #f0f4ff 0%, #fff5f5 100%);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0 40rpx;
}
.login-card {
  width: 100%;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(10rpx);
  border-radius: 32rpx;
  padding: 80rpx 50rpx;
  box-shadow: 0 10rpx 30rpx rgba(100, 116, 255, 0.1);
}
.title {
  font-size: 44rpx;
  font-weight: 700;
  text-align: center;
  background: linear-gradient(90deg, #6474ff, #ff7eb6);
  -webkit-background-clip: text;
  color: transparent;
  margin-bottom: 12rpx;
}
.subtitle {
  font-size: 26rpx;
  color: #888;
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
  color: #666;
  margin-bottom: 10rpx;
  font-weight: 500;
}
.input-box {
  width: 100%;
  height: 90rpx;
  background: #f7f8fc;
  border-radius: 20rpx;
  padding: 0 110rpx 0 30rpx;
  font-size: 28rpx;
  border: 1rpx solid rgba(100, 116, 255, 0.1);
}
.pwd-btn {
  position: absolute;
  right: 30rpx;
  bottom: 24rpx;
  font-size: 26rpx;
  color: #6474ff;
  padding: 0 10rpx;
}
/* 输入框下方红色提示 */
.err-tip {
  display: block;
  font-size: 24rpx;
  color: #ef4444;
  margin-top: 10rpx;
  padding-left: 10rpx;
}
.login-btn {
  width: 100%;
  height: 90rpx;
  line-height: 90rpx;
  background: linear-gradient(90deg, #6474ff, #818cf8);
  color: #fff;
  border-radius: 20rpx;
  font-size: 30rpx;
  font-weight: 600;
  margin-top: 20rpx;
}
.login-btn::after { border: none; }
.tip {
  text-align: center;
  margin-top: 40rpx;
  color: #6474ff;
  font-size: 26rpx;
}
.split-line {
  height: 1rpx;
  background: #e2e8f0;
  margin: 40rpx 0 20rpx;
}
.admin-entry {
  text-align: center;
  color: #ef4444;
  font-size: 26rpx;
}
</style>