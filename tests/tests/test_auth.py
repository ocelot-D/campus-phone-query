"""
认证接口测试：学生注册、学生登录、管理员登录
"""
import pytest
import allure
from faker import Faker

fake = Faker('zh_CN')


@allure.epic("校园电话查询小程序")
@allure.feature("认证模块")
class TestAuth:

    @allure.story("学生注册")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.auth
    def test_register_success(self, anon_client):
        """正常注册：新学号 + 密码"""
        stu_id = f"REG{fake.unique.random_number(digits=6)}"
        code, body = anon_client.post('/auth.php?action=register', json={
            "stuId": stu_id,
            "password": "abc123456",
            "userName": "测试同学"
        })
        assert body['success'] is True
        assert '注册成功' in body['msg']

    @allure.story("学生注册")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.auth
    def test_register_duplicate(self, anon_client):
        """重复注册：同一学号再次注册应失败"""
        stu_id = f"DUP{fake.unique.random_number(digits=6)}"
        anon_client.post('/auth.php?action=register', json={
            "stuId": stu_id, "password": "abc123456"
        })
        # 再次注册
        code, body = anon_client.post('/auth.php?action=register', json={
            "stuId": stu_id, "password": "abc123456"
        })
        assert body['success'] is False
        assert '已注册' in body['msg']

    @allure.story("学生登录")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.auth
    def test_login_success(self, anon_client):
        """正常登录：注册后用正确账号密码登录"""
        stu_id = f"LOG{fake.unique.random_number(digits=6)}"
        anon_client.post('/auth.php?action=register', json={
            "stuId": stu_id, "password": "abc123456"
        })
        code, body = anon_client.post('/auth.php?action=login', json={
            "stuId": stu_id, "password": "abc123456"
        })
        assert body['success'] is True
        assert body['user']['stuId'] == stu_id

    @allure.story("学生登录")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.auth
    def test_login_wrong_password(self, anon_client):
        """登录失败：密码错误"""
        stu_id = f"WRONG{fake.unique.random_number(digits=6)}"
        anon_client.post('/auth.php?action=register', json={
            "stuId": stu_id, "password": "abc123456"
        })
        code, body = anon_client.post('/auth.php?action=login', json={
            "stuId": stu_id, "password": "wrongpass"
        })
        assert body['success'] is False
        assert '密码错误' in body['msg']

    @allure.story("管理员登录")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.auth
    def test_admin_login_success(self, anon_client):
        """管理员正常登录：admin / 123456"""
        code, body = anon_client.post('/auth.php?action=adminLogin', json={
            "adminId": "admin",
            "pwd": "123456"
        })
        assert body['success'] is True

    @allure.story("管理员登录")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.auth
    def test_admin_login_wrong(self, anon_client):
        """管理员登录失败：错误密码"""
        code, body = anon_client.post('/auth.php?action=adminLogin', json={
            "adminId": "admin",
            "pwd": "wrong"
        })
        assert body['success'] is False
