<?php
/**
 * 统一 JSON 响应工具
 */

function json_response($code = 200, $message = 'success', $data = null) {
    http_response_code($code);
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode([
        'code' => $code,
        'message' => $message,
        'data' => $data,
    ], JSON_UNESCAPED_UNICODE);
    exit;
}

/**
 * 获取请求体 JSON 数据
 */
function get_request_body() {
    $raw = file_get_contents('php://input');
    return json_decode($raw, true) ?: [];
}

/**
 * 简单参数校验
 */
function require_params($params, $required) {
    $missing = [];
    foreach ($required as $field) {
        if (!isset($params[$field]) || $params[$field] === '') {
            $missing[] = $field;
        }
    }
    if (!empty($missing)) {
        json_response(400, '缺少必填参数: ' . implode(', ', $missing));
    }
}
