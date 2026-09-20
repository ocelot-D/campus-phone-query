// 校园电话查询接口封装

// 原始默认基础数据（恢复默认使用）
const DEFAULT_PHONE_DATA = [{
  id: 1,
  cateId: 1,
  name: '教务处',
  tel: '020-12345678',
  desc: '学籍、选课、成绩咨询'
},
{
  id: 2,
  cateId: 1,
  name: '学生处',
  tel: '020-12345679',
  desc: '奖助学金、违纪处分'
},
{
  id: 3,
  cateId: 2,
  name: '宿管中心',
  tel: '020-12345680',
  desc: '宿舍报修、钥匙补办'
},
{
  id: 4,
  cateId: 2,
  name: '食堂服务台',
  tel: '020-12345681',
  desc: '餐饮投诉、卫生建议'
},
{
  id: 5,
  cateId: 3,
  name: '计算机学院',
  tel: '020-12345682',
  desc: '教学安排、实验室管理'
},
{
  id: 6,
  cateId: 4,
  name: '校医务室',
  tel: '020-12345683',
  desc: '常见病就诊、药品领取'
},
{
  id: 7,
  cateId: 4,
  name: '保卫处',
  tel: '020-12345684',
  desc: '校园安全、失物招领、门禁'
}]

// 电话本地存储key
const PHONE_STORAGE_KEY = 'phoneDataList'

// 反馈存储key
const FEEDBACK_KEY = 'feedbackList'

// 获取全部校园电话数据（优先读取本地缓存，无则加载默认）
export function getPhoneAll() {
  let local = uni.getStorageSync(PHONE_STORAGE_KEY)
  if (!local || local.length === 0) {
    uni.setStorageSync(PHONE_STORAGE_KEY, DEFAULT_PHONE_DATA)
    return DEFAULT_PHONE_DATA
  }
  return local
}

// 保存电话数据到本地缓存（所有增改操作统一调用）
function savePhoneData(list) {
  uni.setStorageSync(PHONE_STORAGE_KEY, list)
  // 全局广播数据变更，所有页面自动刷新
  uni.$emit('phoneDataChange')
}

// 管理员：恢复默认原始数据
export function resetDefaultPhoneData() {
  savePhoneData(DEFAULT_PHONE_DATA)
  return true
}

// 管理员：新增电话
export function addNewPhone(item) {
  let list = getPhoneAll()
  // 自动生成最大id
  const maxId = list.length > 0 ? Math.max(...list.map(i => i.id)) : 0
  item.id = maxId + 1
  list.push(item)
  savePhoneData(list)
  return true
}

// 管理员：编辑修改已有电话
export function editPhone(editItem) {
  let list = getPhoneAll()
  list = list.map(item => {
    if (item.id === editItem.id) return editItem
    return item
  })
  savePhoneData(list)
  return true
}

// 收藏电话（保存到本地）
export function addCollect(phone) {
  let list = uni.getStorageSync('collectList') || []
  // 避免重复收藏
  let has = list.some(item => item.id === phone.id)
  if (!has) {
    list.push(phone)
    uni.setStorageSync('collectList', list)
    uni.$emit('collectChange')
    return true
  }
  return false
}

// 取消收藏
export function delCollect(id) {
  let list = uni.getStorageSync('collectList') || []
  list = list.filter(item => item.id !== id)
  uni.setStorageSync('collectList', list)
  uni.$emit('collectChange')
}

// 获取我的收藏
export function getCollectList() {
  return uni.getStorageSync('collectList') || []

}

// ===================== 反馈相关接口 =====================
// 提交学生反馈
export function submitFeedback(info) {
  let list = uni.getStorageSync(FEEDBACK_KEY) || []
  const maxId = list.length > 0 ? Math.max(...list.map(i => i.id)) : 0
  info.id = maxId + 1
  info.time = new Date().toLocaleString()
  // 新增默认状态：等待解决
  info.status = "等待解决"
  list.push(info)
  uni.setStorageSync(FEEDBACK_KEY, list)
  uni.$emit('feedbackChange')
  return true
}

// 获取全部反馈（管理员查看）
export function getFeedbackList() {
  return uni.getStorageSync(FEEDBACK_KEY) || []
}

// 修改反馈处理状态
export function changeFeedbackStatus(feedbackId, newStatus) {
  let list = getFeedbackList()
  list = list.map(item => {
    if(item.id === feedbackId){
      item.status = newStatus
    }
    return item
  })
  uni.setStorageSync(FEEDBACK_KEY, list)
  uni.$emit('feedbackChange')
}

// 清空所有反馈（管理员功能）
export function clearAllFeedback() {
  uni.removeStorageSync(FEEDBACK_KEY)
  uni.$emit('feedbackChange')
}
// ===================== 用户注册、登录相关接口（学生） =====================
const USER_KEY = 'userInfoList'

// 获取已注册学生用户列表
export function getUserList() {
  return uni.getStorageSync(USER_KEY) || []
}

// 学生注册
export function registerUser(user) {
  let userList = getUserList()
  let isExist = userList.some(item => item.stuId === user.stuId)
  if (isExist) {
    return {
      success: false,
      msg: '该学号已注册，请直接登录'
    }
  }
  userList.push(user)
  uni.setStorageSync(USER_KEY, userList)
  return {
    success: true,
    msg: '注册成功，请前往登录'
  }
}

// 学生登录校验
export function checkLogin(stuId, password) {
  let userList = getUserList()
  let user = userList.find(item => item.stuId === stuId && item.password === password)
  if (user) {
    return {
      success: true,
      user: user
    }
  }
  return {
    success: false,
    msg: '学号或密码错误'
  }
}

// ===================== 管理员账户接口（独立体系） =====================
const ADMIN_STORAGE_KEY = 'adminAccount'

// 默认管理员账号：admin / 123456
export function getAdminAccount() {
  let admin = uni.getStorageSync(ADMIN_STORAGE_KEY)
  if (!admin) {
    const defaultAdmin = { adminId: 'admin', pwd: '123456', name: '系统管理员' }
    uni.setStorageSync(ADMIN_STORAGE_KEY, defaultAdmin)
    return defaultAdmin
  }
  return admin
}

// 管理员登录校验
export function checkAdminLogin(adminId, pwd) {
  const admin = getAdminAccount()
  if (admin.adminId === adminId && admin.pwd === pwd) {
    return { success: true, admin }
  }
  return { success: false, msg: '管理员账号或密码错误' }
}

// 存储登录身份标识
export const LOGIN_TYPE_KEY = 'loginType' // student / admin