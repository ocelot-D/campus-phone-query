<?php
/**
 * 认证接口：学生注册、学生登录、管理员登录
 * POST /api/auth.php?action=register     学生注册
 * POST /api/auth.php?action=login       学生登录
 * POST /api/auth.php?action=adminLogin  管理员登录
 */

require_once __DIR__ . '/../config/database.php';
require_once __DIR__ . '/../utils/response.php';

$action = $_GET['action'] ?? '';
$body = get_request_body();

// ========== 学生注册 ==========
if ($action === 'register') {
    require_params($body, ['stuId', 'password']);
    $stuId = trim($body['stuId']);
    $password = $body['password'];
    $userName = trim($body['userName'] ?? '同学');

    // 检查是否已注册
    $stmt = db()->prepare('SELECT id FROM users WHERE stu_id = ?');
    $stmt->execute([$stuId]);
    if ($stmt->fetch()) {
        echo json_encode(['success' => false, 'msg' => '该学号已注册，请直接登录']);
        exit;
    }

    // 插入用户（密码明文存储，与前端原逻辑一致；生产环境建议加密）
    $stmt = db()->prepare('INSERT INTO users (stu_id, user_name, password) VALUES (?, ?, ?)');
    $stmt->execute([$stuId, $userName, $password]);

    echo json_encode(['success' => true, 'msg' => '注册成功，请前往登录']);
    exit;
}

// ========== 学生登录 ==========
elseif ($action === 'login') {
    require_params($body, ['stuId', 'password']);
    $stuId = trim($body['stuId']);
    $password = $body['password'];

    $stmt = db()->prepare('SELECT id, stu_id, user_name, password FROM users WHERE stu_id = ?');
    $stmt->execute([$stuId]);
    $user = $stmt->fetch();

    if ($user && $user['password'] === $password) {
        echo json_encode([
            'success' => true,
            'user' => [
                'stuId' => $user['stu_id'],
                'userName' => $user['user_name'],
            ]
        ]);
    } else {
        echo json_encode(['success' => false, 'msg' => '学号或密码错误']);
    }
    exit;
}

// ========== 管理员登录 ==========
elseif ($action === 'adminLogin') {
    require_params($body, ['adminId', 'pwd']);
    $adminId = trim($body['adminId']);
    $pwd = $body['pwd'];

    $stmt = db()->prepare('SELECT id, admin_id, pwd, name FROM admin WHERE admin_id = ?');
    $stmt->execute([$adminId]);
    $admin = $stmt->fetch();

    if ($admin && $admin['pwd'] === $pwd) {
        echo json_encode([
            'success' => true,
            'admin' => [
                'adminId' => $admin['admin_id'],
                'name' => $admin['name'],
            ]
        ]);
    } else {
        echo json_encode(['success' => false, 'msg' => '管理员账号或密码错误']);
    }
    exit;
}

else {
    json_response(400, '未知操作，可选: register / login / adminLogin');
}
