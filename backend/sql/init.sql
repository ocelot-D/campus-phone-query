-- ============================================
-- 校园电话查询小程序 - 数据库初始化脚本
-- 字段名完全匹配前端 api/api.js 的数据结构
-- 使用方法：phpMyAdmin 导入本文件
-- ============================================

CREATE DATABASE IF NOT EXISTS `campus_phone` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `campus_phone`;

-- ----------------------------
-- 学生用户表
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `stu_id` VARCHAR(20) NOT NULL UNIQUE COMMENT '学号',
  `user_name` VARCHAR(50) DEFAULT '' COMMENT '昵称',
  `password` VARCHAR(255) NOT NULL COMMENT '密码',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- 电话条目表（字段名对齐前端：cate_id / name / tel / desc）
-- ----------------------------
DROP TABLE IF EXISTS `phones`;
CREATE TABLE `phones` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `cate_id` INT NOT NULL DEFAULT 1 COMMENT '分类ID：1行政办公 2后勤服务 3教学院系 4安保医疗',
  `name` VARCHAR(100) NOT NULL COMMENT '单位名称',
  `tel` VARCHAR(30) NOT NULL COMMENT '电话号码',
  `desc` VARCHAR(500) DEFAULT '' COMMENT '描述说明',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- 收藏表
-- ----------------------------
DROP TABLE IF EXISTS `favorites`;
CREATE TABLE `favorites` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `stu_id` VARCHAR(20) NOT NULL COMMENT '收藏学生学号',
  `phone_id` INT NOT NULL COMMENT '电话ID',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY `uk_stu_phone` (`stu_id`, `phone_id`),
  FOREIGN KEY (`phone_id`) REFERENCES `phones`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- 意见反馈表
-- ----------------------------
DROP TABLE IF EXISTS `feedback`;
CREATE TABLE `feedback` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `stu_id` VARCHAR(20) NOT NULL COMMENT '提交学生学号',
  `content` TEXT NOT NULL COMMENT '反馈内容',
  `contact` VARCHAR(100) DEFAULT '' COMMENT '联系方式',
  `status` VARCHAR(20) DEFAULT '等待解决' COMMENT '处理状态',
  `time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '提交时间',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- 管理员表
-- ----------------------------
DROP TABLE IF EXISTS `admin`;
CREATE TABLE `admin` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `admin_id` VARCHAR(50) NOT NULL UNIQUE COMMENT '管理员账号',
  `pwd` VARCHAR(255) NOT NULL COMMENT '密码',
  `name` VARCHAR(50) DEFAULT '系统管理员'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 初始化数据
-- ============================================

-- 默认管理员
INSERT INTO `admin` (`admin_id`, `pwd`, `name`) VALUES ('admin', '123456', '系统管理员');

-- 默认电话数据（对齐前端 DEFAULT_PHONE_DATA）
INSERT INTO `phones` (`id`, `cate_id`, `name`, `tel`, `desc`) VALUES
(1, 1, '教务处', '020-12345678', '学籍、选课、成绩咨询'),
(2, 1, '学生处', '020-12345679', '奖助学金、违纪处分'),
(3, 2, '宿管中心', '020-12345680', '宿舍报修、钥匙补办'),
(4, 2, '食堂服务台', '020-12345681', '餐饮投诉、卫生建议'),
(5, 3, '计算机学院', '020-12345682', '教学安排、实验室管理'),
(6, 4, '校医务室', '020-12345683', '常见病就诊、药品领取'),
(7, 4, '保卫处', '020-12345684', '校园安全、失物招领、门禁');
