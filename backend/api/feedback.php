<?php
/**
 * 意见反馈接口
 * GET  /api/feedback.php                    获取全部反馈（管理员）
 * GET  /api/feedback.php?stuId=xxx          获取某学生的反馈
 * POST /api/feedback.php?action=submit      提交反馈
 * POST /api/feedback.php?action=status      修改反馈状态（管理员）
 * POST /api/feedback.php?action=clear        清空所有反馈（管理员）
 */

require_once __DIR__ . '/../config/database.php';
require_once __DIR__ . '/../utils/response.php';

$action = $_GET['action'] ?? 'list';

// ========== 获取反馈列表 ==========
if ($action === 'list') {
    $stuId = trim($_GET['stuId'] ?? '');

    if ($stuId) {
        // 学生看自己的反馈
        $stmt = db()->prepare(
            'SELECT id, stu_id, content, contact, status, time FROM feedback WHERE stu_id = ? ORDER BY time DESC'
        );
        $stmt->execute([$stuId]);
    } else {
        // 管理员看全部
        $stmt = db()->query('SELECT id, stu_id, content, contact, status, time FROM feedback ORDER BY time DESC');
    }

    $list = $stmt->fetchAll();
    $result = array_map(function($item) {
        return [
            'id' => (int)$item['id'],
            'stuId' => $item['stu_id'],
            'content' => $item['content'],
            'contact' => $item['contact'],
            'status' => $item['status'],
            'time' => $item['time'],
        ];
    }, $list);
    echo json_encode($result, JSON_UNESCAPED_UNICODE);
    exit;
}

// ========== 提交反馈 ==========
elseif ($action === 'submit') {
    $body = get_request_body();
    require_params($body, ['stuId', 'content']);

    $stmt = db()->prepare('INSERT INTO feedback (stu_id, content, contact, status) VALUES (?, ?, ?, ?)');
    $stmt->execute([
        trim($body['stuId']),
        trim($body['content']),
        trim($body['contact'] ?? ''),
        '等待解决',
    ]);
    echo json_encode(true);
    exit;
}

// ========== 修改反馈状态 ==========
elseif ($action === 'status') {
    $body = get_request_body();
    require_params($body, ['id', 'status']);

    $stmt = db()->prepare('UPDATE feedback SET status = ? WHERE id = ?');
    $stmt->execute([trim($body['status']), (int)$body['id']]);
    echo json_encode(true);
    exit;
}

// ========== 清空所有反馈 ==========
elseif ($action === 'clear') {
    db()->exec('DELETE FROM feedback');
    echo json_encode(true);
    exit;
}

else {
    json_response(400, '未知操作');
}
