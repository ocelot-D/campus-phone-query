<?php
/**
 * 数据库连接配置
 */

define('DB_HOST', 'localhost');
define('DB_NAME', 'campus_phone');
define('DB_USER', 'root');
define('DB_PASS', 'root');        // PhpStudy 默认 root
define('DB_CHARSET', 'utf8mb4');

/**
 * 获取 PDO 数据库连接（单例）
 */
function db() {
    static $pdo = null;
    if ($pdo === null) {
        $dsn = 'mysql:host=' . DB_HOST . ';dbname=' . DB_NAME . ';charset=' . DB_CHARSET;
        try {
            $pdo = new PDO($dsn, DB_USER, DB_PASS, [
                PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
                PDO::ATTR_EMULATE_PREPARES => false,
            ]);
        } catch (PDOException $e) {
            json_response(500, '数据库连接失败: ' . $e->getMessage());
        }
    }
    return $pdo;
}
