# 接口自动化测试框架

基于 **Python + pytest + requests + Allure** 的接口自动化测试框架，用于测试校园电话查询小程序后端 API。

## 技术栈

| 组件 | 作用 |
|---|---|
| Python 3.9+ | 测试语言 |
| pytest | 测试运行框架 |
| requests | HTTP 请求库 |
| Allure | 可视化测试报告 |
| Faker | 生成随机测试数据 |
| GitHub Actions | CI 自动执行 |

## 快速开始

### 1. 安装依赖

```bash
cd api-testing-framework
pip install -r requirements.txt
```

### 2. 配置后端地址

复制 `config/env.yaml`，修改 `base_url` 为你的后端地址：

```yaml
dev:
  base_url: "http://localhost/campus-phone-backend/api"
```

### 3. 运行测试

```bash
# 运行全部测试
pytest

# 只跑冒烟用例
pytest -m smoke

# 只跑认证相关
pytest -m auth

# 生成 Allure 报告（需要先安装 allure 命令行）
allure serve reports/allure-results
```

## 项目结构

```
api-testing-framework/
├── common/
│   ├── config.py          # 环境配置加载
│   └── api_client.py      # HTTP 请求封装
├── config/
│   └── env.yaml           # 环境配置（dev/test）
├── data/                  # 测试数据（YAML）
├── tests/
│   ├── test_auth.py       # 认证接口测试
│   ├── test_phones.py     # 电话查询测试
│   └── test_favorites.py  # 收藏功能测试
├── conftest.py            # pytest fixtures
├── pytest.ini             # pytest 配置
├── requirements.txt       # Python 依赖
├── .github/workflows/
│   └── ci.yml             # GitHub Actions CI
└── reports/               # 测试报告输出目录
```

## 框架特性

- **数据驱动**：使用 `@pytest.mark.parametrize` 实现参数化测试
- **环境隔离**：dev/test 环境配置分离，切换只需改一行
- **自动登录**：`auth_client` fixture 自动注册登录并携带 token
- **Allure 报告**：每个请求/响都会记录到报告中，可视化展示
- **CI 集成**：push 代码自动跑测试，不需要手动触发
- **用例标记**：`smoke` / `regression` / `auth` / `phone` / `favorite` 分组管理

## 测试覆盖范围

| 模块 | 用例数 | 覆盖场景 |
|---|---|---|
| 认证 | 5 | 注册成功、重复注册、密码过短、登录成功、密码错误 |
| 电话查询 | 6 | 列表、分页、关键词搜索、分类筛选、详情、404 |
| 收藏 | 5 | 收藏成功、重复收藏、收藏列表、取消收藏、未登录拦截 |
| **合计** | **16** | |
