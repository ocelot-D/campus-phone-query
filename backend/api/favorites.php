<?php
/**
 * 收藏接口
 * GET  /api/favorites.php?stuId=xxx     获取收藏列表
 * POST /api/favorites.php?action=add    收藏电话
 * POST /api/favorites.php?action=remove 取消收藏
 */

require_once __DIR__ . '/../config/database.php';
require_once __DIR__ . '/../utils/response.php';

$action = $_GET['action'] ?? 'list';

// ========== 获取收藏列表 ==========
if ($action === 'list') {
    $stuId = trim($_GET['stuId'] ?? '');
    if (!$stuId) json_response(400, '缺少 stuId 参数');

    $stmt = db()->prepare(
        'SELECT p.id, p.cate_id, p.name, p.tel, p.`desc`
         FROM favorites f
         JOIN phones p ON f.phone_id = p.id
         WHERE f.stu_id = ?
         ORDER BY f.created_at DESC'
    );
    $stmt->execute([$stuId]);
    $list = $stmt->fetchAll();

    $result = array_map(function($item) {
        return [
            'id' => (int)$item['id'],
            'cateId' => (int)$item['cate_id'],
            'name' => $item['name'],
            'tel' => $item['tel'],
            'desc' => $item['desc'],
        ];
    }, $list);
    echo json_encode($result, JSON_UNESCAPED_UNICODE);
    exit;
}

// ========== 添加收藏 ==========
elseif ($action === 'add') {
    $body = get_request_body();
    require_params($body, ['stuId', 'phone']);
    $stuId = trim($body['stuId']);
    $phone = $body['phone']; // phone 是整个电话对象 {id, cateId, name, tel, desc}
    $phoneId = (int)$phone['id'];

    // 检查是否已收藏
    $stmt = db()->prepare('SELECT id FROM favorites WHERE stu_id = ? AND phone_id = ?');
    $stmt->execute([$stuId, $phoneId]);
    if ($stmt->fetch()) {
        echo json_encode(false); // 已收藏，返回 false
        exit;
    }

    $stmt = db()->prepare('INSERT INTO favorites (stu_id, phone_id) VALUES (?, ?)');
    $stmt->execute([$stuId, $phoneId]);
    echo json_encode(true); // 收藏成功
    exit;
}

// ========== 取消收藏 ==========
elseif ($action === 'remove') {
    $body = get_request_body();
    require_params($body, ['stuId', 'id']);
    $stuId = trim($body['stuId']);
    $phoneId = (int)$body['id'];

    $stmt = db()->prepare('DELETE FROM favorites WHERE stu_id = ? AND phone_id = ?');
    $stmt->execute([$stuId, $phoneId]);
    echo json_encode(true);
    exit;
}

else {
    json_response(400, '未知操作，可选: list / add / remove');
}
