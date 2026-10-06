<?php
/**
 * 简易 Token 认证工具
 * 使用 session 或简单 token 机制，适合小程序场景
 * 生产环境建议替换为 JWT
 */

require_once __DIR__ . '/../config/database.php';

/**
 * 生成简单 token（基于用户ID + 时间戳 + 随机串）
 */
function generate_token($user_id) {
    $raw = $user_id . '|' . time() . '|' . bin2hex(random_bytes(8));
    return base64_encode($raw);
}

/**
 * 从请求头解析 token
 */
function get_bearer_token() {
    $headers = function_exists('getallheaders') ? getallheaders() : [];
    if (isset($headers['Authorization'])) {
        return str_replace('Bearer ', '', $headers['Authorization']);
    }
    if (isset($_SERVER['HTTP_AUTHORIZATION'])) {
        return str_replace('Bearer ', '', $_SERVER['HTTP_AUTHORIZATION']);
    }
    return null;
}

/**
 * 校验 token，返回用户ID；失败则返回 401
 */
function auth_user() {
    $token = get_bearer_token();
    if (!$token) {
        json_response(401, '未登录，请先登录');
    }

    // 简单方式：token 格式为 base64(user_id|timestamp|random)
    $decoded = base64_decode($token);
    $parts = explode('|', $decoded);
    if (count($parts) < 2 || !is_numeric($parts[0])) {
        json_response(401, 'token 无效');
    }

    $user_id = (int)$parts[0];

    // 检查用户是否存在
    $stmt = db()->prepare('SELECT id, student_no, nickname FROM users WHERE id = ?');
    $stmt->execute([$user_id]);
    $user = $stmt->fetch();

    if (!$user) {
        json_response(401, '用户不存在');
    }

    return $user;
}
