<?php
/**
 * 电话接口
 * GET  /api/phones.php              获取全部电话列表
 * POST /api/phones.php?action=add    新增电话（管理员）
 * POST /api/phones.php?action=edit   编辑电话（管理员）
 * POST /api/phones.php?action=reset  恢复默认数据（管理员）
 */

require_once __DIR__ . '/../config/database.php';
require_once __DIR__ . '/../utils/response.php';

$action = $_GET['action'] ?? 'list';

// ========== 获取全部电话列表 ==========
if ($action === 'list') {
    $stmt = db()->query('SELECT id, cate_id, name, tel, `desc` FROM phones ORDER BY id ASC');
    $list = $stmt->fetchAll();
    // 转换键名匹配前端：cate_id → cateId
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

// ========== 新增电话 ==========
elseif ($action === 'add') {
    $body = get_request_body();
    require_params($body, ['cateId', 'name', 'tel']);

    $stmt = db()->prepare('INSERT INTO phones (cate_id, name, tel, `desc`) VALUES (?, ?, ?, ?)');
    $stmt->execute([
        (int)$body['cateId'],
        trim($body['name']),
        trim($body['tel']),
        trim($body['desc'] ?? ''),
    ]);
    echo json_encode(true);
    exit;
}

// ========== 编辑电话 ==========
elseif ($action === 'edit') {
    $body = get_request_body();
    require_params($body, ['id', 'cateId', 'name', 'tel']);

    $stmt = db()->prepare('UPDATE phones SET cate_id = ?, name = ?, tel = ?, `desc` = ? WHERE id = ?');
    $stmt->execute([
        (int)$body['cateId'],
        trim($body['name']),
        trim($body['tel']),
        trim($body['desc'] ?? ''),
        (int)$body['id'],
    ]);
    echo json_encode(true);
    exit;
}

// ========== 恢复默认数据 ==========
elseif ($action === 'reset') {
    // 清空并重新插入默认数据
    db()->exec('DELETE FROM phones');
    $defaults = [
        [1, 1, '教务处', '020-12345678', '学籍、选课、成绩咨询'],
        [2, 1, '学生处', '020-12345679', '奖助学金、违纪处分'],
        [3, 2, '宿管中心', '020-12345680', '宿舍报修、钥匙补办'],
        [4, 2, '食堂服务台', '020-12345681', '餐饮投诉、卫生建议'],
        [5, 3, '计算机学院', '020-12345682', '教学安排、实验室管理'],
        [6, 4, '校医务室', '020-12345683', '常见病就诊、药品领取'],
        [7, 4, '保卫处', '020-12345684', '校园安全、失物招领、门禁'],
    ];
    $stmt = db()->prepare('INSERT INTO phones (id, cate_id, name, tel, `desc`) VALUES (?, ?, ?, ?, ?)');
    foreach ($defaults as $d) {
        $stmt->execute($d);
    }
    echo json_encode(true);
    exit;
}

// ========== 删除电话 ==========
elseif ($action === 'delete') {
    $body = get_request_body();
    require_params($body, ['id']);

    $stmt = db()->prepare('DELETE FROM phones WHERE id = ?');
    $stmt->execute([(int)$body['id']]);
    echo json_encode(true);
    exit;
}

else {
    json_response(400, '未知操作，可选: list / add / edit / delete / reset');
}
