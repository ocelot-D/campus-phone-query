<script>
import { LOGIN_TYPE_KEY } from './api/api.js'

const STUDENT_PAGES = [
  'pages/index/index',
  'pages/category/category',
  'pages/collect/collect',
  'pages/my/my'
]

export default {
  onShow() {
    const loginType = uni.getStorageSync(LOGIN_TYPE_KEY)
    const pages = getCurrentPages()
    if (!pages.length) return

    const currentPage = pages[pages.length - 1].route

    if (currentPage.startsWith('pages/adminManage')) {
      if (loginType !== 'admin') {
        uni.reLaunch({ url: '/pages/adminLogin/adminLogin' })
        return
      }
    }

    if (STUDENT_PAGES.includes(currentPage) && loginType !== 'student') {
      uni.reLaunch({ url: '/pages/login/login' })
    }
  }
}
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
