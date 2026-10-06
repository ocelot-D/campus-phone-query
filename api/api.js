// ============================================
// 校园电话查询接口封装（后端 API 版）
// 使用方法：替换项目中原有的 api/api.js 文件
// 使用前请修改下面的 BASE_URL 为你的后端地址
// ============================================

// TODO: 修改为你的后端地址（PhpStudy 部署后的路径）
const BASE_URL = 'http://localhost/campus-phone-backend/api'

// ===================== 底层请求封装 =====================

function request(path, method = 'GET', data = {}) {
  return new Promise((resolve, reject) => {
    uni.request({
      url: BASE_URL + path,
      method: method,
      data: data,
      header: { 'Content-Type': 'application/json' },
      success: (res) => {
        resolve(res.data)
      },
      fail: (err) => {
        console.error('请求失败:', path, err)
        uni.showToast({ title: '网络请求失败', icon: 'none' })
        reject(err)
      }
    })
  })
}

// ===================== 电话相关 =====================

/**
 * 获取全部校园电话
 * 返回：[{id, cateId, name, tel, desc}]
 */
export async function getPhoneAll() {
  return await request('/phones.php?action=list')
}

/**
 * 管理员：新增电话
 * 参数：{cateId, name, tel, desc}
 */
export async function addNewPhone(item) {
  return await request('/phones.php?action=add', 'POST', item)
}

/**
 * 管理员：编辑电话
 * 参数：{id, cateId, name, tel, desc}
 */
export async function editPhone(editItem) {
  return await request('/phones.php?action=edit', 'POST', editItem)
}

/**
 * 管理员：删除电话
 * 参数：id
 */
export async function deletePhone(id) {
  return await request('/phones.php?action=delete', 'POST', { id: id })
}

/**
 * 管理员：恢复默认数据
 */
export async function resetDefaultPhoneData() {
  return await request('/phones.php?action=reset', 'POST')
}

// ===================== 收藏相关 =====================

/**
 * 收藏电话
 * 参数 phone: {id, cateId, name, tel, desc}
 * 返回：true=收藏成功, false=已收藏过了
 */
export async function addCollect(phone) {
  const stuId = uni.getStorageSync('studentId')
  return await request('/favorites.php?action=add', 'POST', {
    stuId: stuId,
    phone: phone
  })
}

/**
 * 取消收藏
 * 参数 id: 电话ID
 */
export async function delCollect(id) {
  const stuId = uni.getStorageSync('studentId')
  return await request('/favorites.php?action=remove', 'POST', {
    stuId: stuId,
    id: id
  })
}

/**
 * 获取我的收藏列表
 */
export async function getCollectList() {
  const stuId = uni.getStorageSync('studentId')
  return await request('/favorites.php?action=list&stuId=' + stuId)
}

// ===================== 反馈相关 =====================

/**
 * 提交学生反馈
 * 参数 info: {stuId, content, contact}
 */
export async function submitFeedback(info) {
  return await request('/feedback.php?action=submit', 'POST', info)
}

/**
 * 获取反馈列表
 * 不传参数 = 管理员看全部；传 stuId = 学生只看自己的
 */
export async function getFeedbackList(stuId) {
  let url = '/feedback.php?action=list'
  if (stuId) url += '&stuId=' + stuId
  return await request(url)
}

/**
 * 修改反馈处理状态（管理员）
 */
export async function changeFeedbackStatus(feedbackId, newStatus) {
  return await request('/feedback.php?action=status', 'POST', {
    id: feedbackId,
    status: newStatus
  })
}

/**
 * 清空所有反馈（管理员）
 */
export async function clearAllFeedback() {
  return await request('/feedback.php?action=clear', 'POST')
}

// ===================== 学生注册、登录 =====================

/**
 * 学生注册
 * 参数 user: {stuId, password, userName}
 * 返回：{success: true/false, msg: '...'}
 */
export async function registerUser(user) {
  return await request('/auth.php?action=register', 'POST', user)
}

/**
 * 学生登录校验
 * 返回：{success: true/false, user: {stuId, userName}, msg: '...'}
 */
export async function checkLogin(stuId, password) {
  return await request('/auth.php?action=login', 'POST', {
    stuId: stuId,
    password: password
  })
}

// ===================== 管理员账户 =====================

/**
 * 管理员登录校验
 * 返回：{success: true/false, admin: {...}, msg: '...'}
 */
export async function checkAdminLogin(adminId, pwd) {
  return await request('/auth.php?action=adminLogin', 'POST', {
    adminId: adminId,
    pwd: pwd
  })
}

// ===================== 常量 =====================
export const LOGIN_TYPE_KEY = 'loginType' // student / admin
