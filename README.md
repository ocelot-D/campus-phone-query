# 校园电话查询小程序

一站式校园通讯录解决方案，解决校园各处电话零散、紧急查询不便的痛点。

## 项目架构

本项目是一个完整的全栈项目，包含四大模块：

```
campus-phone-query/
├── pages/          # 前端页面（UniApp + Vue 3）
├── api/            # 前端请求封装
├── backend/        # 后端 API（PHP + MySQL）
├── tests/          # 接口自动化测试（pytest）
└── monitor/        # 服务监控告警系统（Python）
```

## 技术栈

| 层级 | 技术 |
|---|---|
| 前端 | UniApp + Vue 3 + 微信小程序原生 + H5 |
| 后端 | PHP + MySQL + Apache |
| 测试 | Python + pytest + requests + Allure |
| 运维 | Python + requests + pymysql + 邮件告警 |

## 功能特性

### 用户端
- 📞 电话分类展示（行政办公 / 后勤服务 / 教学院系 / 安保医疗）
- 🔍 多维查询功能，快速定位目标联系方式
- ⭐ 常用电话收藏功能，一键拨号
- 📝 意见反馈提交

### 管理端
- ➕ 电话条目新增、编辑、删除
- 📊 学生反馈查看与处理
- 🔄 数据一键恢复默认

## 后端 API 文档

### 认证模块
| 接口 | 方法 | 说明 |
|---|---|---|
| `/auth.php?action=register` | POST | 学生注册 |
| `/auth.php?action=login` | POST | 学生登录 |
| `/auth.php?action=adminLogin` | POST | 管理员登录 |

### 电话模块
| 接口 | 方法 | 说明 |
|---|---|---|
| `/phones.php?action=list` | GET | 获取电话列表 |
| `/phones.php?action=add` | POST | 新增电话 |
| `/phones.php?action=edit` | POST | 编辑电话 |
| `/phones.php?action=delete` | POST | 删除电话 |
| `/phones.php?action=reset` | POST | 恢复默认数据 |

### 收藏模块
| 接口 | 方法 | 说明 |
|---|---|---|
| `/favorites.php?action=list` | GET | 获取收藏列表 |
| `/favorites.php?action=add` | POST | 添加收藏 |
| `/favorites.php?action=remove` | POST | 取消收藏 |

### 反馈模块
| 接口 | 方法 | 说明 |
|---|---|---|
| `/feedback.php?action=list` | GET | 获取反馈列表 |
| `/feedback.php?action=submit` | POST | 提交反馈 |

## 测试

```bash
cd tests
pip install -r requirements.txt
pytest
```

15 个测试用例，覆盖认证、电话、收藏三大模块。

## 监控

```bash
cd monitor
pip install -r requirements.txt
python monitor.py
```

定时监控 API 健康状态和数据库连通性，异常自动邮件告警。

## 本地部署

1. 导入 `backend/sql/init.sql` 到 MySQL
2. 配置 `backend/config/database.php` 数据库连接
3. 将 `backend/` 放入 Apache 网站目录
4. 前端使用 HBuilder X 打开，修改 `api/api.js` 中的 `BASE_URL`

![小程序预览图](./static/tabbar/preview.png)