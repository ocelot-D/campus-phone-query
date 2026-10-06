"""
pytest fixtures：提供匿名客户端、测试用户等
"""
import pytest
from faker import Faker
from common.api_client import ApiClient

fake = Faker('zh_CN')


@pytest.fixture(scope="session")
def anon_client():
    """未登录的客户端"""
    return ApiClient()


@pytest.fixture(scope="session")
def test_stu_id(anon_client):
    """注册一个测试用户，返回学号"""
    stu_id = f"TEST{fake.unique.random_number(digits=6)}"
    password = "abc123456"

    code, body = anon_client.post('/auth.php?action=register', json={
        "stuId": stu_id,
        "password": password,
        "userName": "测试用户"
    })
    assert body.get('success'), f"注册失败: {body}"
    return stu_id
