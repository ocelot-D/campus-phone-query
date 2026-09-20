<template>
  <view class="register-wrap">
    <view class="register-card">
      <view class="title">注册新账号</view>
      <view class="subtitle">加入校园电话查询</view>

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

      <!-- 姓名 -->
      <view class="form-item">
        <text class="label">姓名</text>
        <input class="input-box" v-model="userName" placeholder="请输入姓名" />
      </view>

      <!-- 密码 -->
      <view class="form-item pwd-wrap">
        <text class="label">密码</text>
        <input
          class="input-box"
          v-model="password"
          :password="!pwdVisible"
          placeholder="请设置登录密码"
          @input="checkPwd"
        />
        <view class="pwd-btn" @click="togglePwd">
          {{ pwdVisible ? '隐藏' : '显示' }}
        </view>
        <text v-if="pwdTip" class="err-tip">{{ pwdTip }}</text>
      </view>

      <!-- 确认密码 -->
      <view class="form-item pwd-wrap">
        <text class="label">确认密码</text>
        <input
          class="input-box"
          v-model="confirmPwd"
          :password="!confirmPwdVisible"
          placeholder="再次输入密码"
          @input="checkConfirmPwd"
        />
        <view class="pwd-btn" @click="toggleConfirmPwd">
          {{ confirmPwdVisible ? '隐藏' : '显示' }}
        </view>
        <text v-if="confirmTip" class="err-tip">{{ confirmTip }}</text>
      </view>

      <button class="register-btn" @click="handleRegister">完成注册</button>
      <view class="tip" @click="goLogin">已有账号？返回登录</view>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'
import { registerUser } from '../../api/api.js'

const stuId = ref('')
const userName = ref('')
const password = ref('')
const confirmPwd = ref('')

const pwdVisible = ref(false)
const confirmPwdVisible = ref(false)

// 错误提示文字
const stuTip = ref('')
const pwdTip = ref('')
const confirmTip = ref('')

// 正则
const stuReg = /^\d+$/
const pwdReg = /^(?=.*[0-9])(?=.*[a-zA-Z]).{6,18}$/

const togglePwd = () => {
  pwdVisible.value = !pwdVisible.value
}
const toggleConfirmPwd = () => {
  confirmPwdVisible.value = !confirmPwdVisible.value
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
  // 同步校验确认密码
  checkConfirmPwd()
}

// 实时校验确认密码
const checkConfirmPwd = () => {
  if (!confirmPwd.value) {
    confirmTip.value = ''
    return
  }
  if(confirmPwd.value === password.value){
    confirmTip.value = ''
  }else{
    confirmTip.value = '两次输入密码不一致'
  }
}

// 提交注册兜底校验
const handleRegister = () => {
  // 重新执行校验，清空合法输入的提示
  checkStu()
  checkPwd()
  checkConfirmPwd()

  // 存在错误直接拦截
  if (stuTip.value || pwdTip.value || confirmTip.value) {
    uni.showModal({ title:'提示',content:'请修正输入错误后再提交',showCancel:false })
    return
  }
  if (!stuId.value || !userName.value || !password.value || !confirmPwd.value) {
    uni.showModal({ title:'提示',content:'请填写完整信息',showCancel:false })
    return
  }

  let res = registerUser({
    stuId: stuId.value,
    userName: userName.value,
    password: password.value
  })
  if (res.success) {
    uni.showToast({ title: res.msg, icon: 'success' })
    setTimeout(() => uni.navigateBack(), 1000)
  } else {
    uni.showModal({ title:'注册失败',content:res.msg,showCancel:false })
  }
}

const goLogin = () => {
  uni.navigateBack()
}
</script>

<style scoped>
.register-wrap {
  min-height: 100vh;
  background: linear-gradient(135deg, #f0f4ff 0%, #fff5f5 100%);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0 40rpx;
}
.register-card {
  width: 100%;
  /* 背景：纯白色半透明 */
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
/* 输入框下方红色错误提示 */
.err-tip {
  display: block;
  font-size: 24rpx;
  color: #ef4444;
  margin-top: 10rpx;
  padding-left: 10rpx;
}
.register-btn {
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
.register-btn::after { border: none; }
.tip {
  text-align: center;
  margin-top: 40rpx;
  color: #6474ff;
  font-size: 26rpx;
}
</style>