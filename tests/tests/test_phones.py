"""
电话接口测试：列表、新增、编辑、删除
"""
import pytest
import allure
from faker import Faker

fake = Faker('zh_CN')


@allure.epic("校园电话查询小程序")
@allure.feature("电话模块")
class TestPhones:

    @allure.story("电话列表")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.phone
    def test_get_phone_list(self, anon_client):
        """获取电话列表：应返回数组且有数据"""
        code, body = anon_client.get('/phones.php?action=list')
        assert code == 200
        assert isinstance(body, list)
        assert len(body) > 0

    @allure.story("电话列表")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.phone
    def test_phone_list_fields(self, anon_client):
        """列表每条数据的字段是否完整"""
        code, body = anon_client.get('/phones.php?action=list')
        first = body[0]
        assert 'id' in first
        assert 'cateId' in first
        assert 'name' in first
        assert 'tel' in first
        assert 'desc' in first

    @allure.story("新增电话")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.phone
    def test_add_phone(self, anon_client):
        """管理员新增电话"""
        code, body = anon_client.post('/phones.php?action=add', json={
            "cateId": 1,
            "name": f"测试部门{fake.random_number(digits=4)}",
            "tel": "020-99999999",
            "desc": "自动化测试新增"
        })
        assert body is True

    @allure.story("编辑电话")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.phone
    def test_edit_phone(self, anon_client):
        """管理员编辑电话"""
        # 先新增一个
        anon_client.post('/phones.php?action=add', json={
            "cateId": 2,
            "name": "待修改部门",
            "tel": "020-88888888",
            "desc": "待修改"
        })
        # 拿到列表最后一条的 id
        code, list_data = anon_client.get('/phones.php?action=list')
        phone_id = list_data[-1]['id']

        # 编辑它
        code, body = anon_client.post('/phones.php?action=edit', json={
            "id": phone_id,
            "cateId": 3,
            "name": "已修改部门",
            "tel": "020-77777777",
            "desc": "已修改描述"
        })
        assert body is True

    @allure.story("删除电话")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.phone
    def test_delete_phone(self, anon_client):
        """管理员删除电话"""
        # 先新增一个
        anon_client.post('/phones.php?action=add', json={
            "cateId": 4,
            "name": "待删除部门",
            "tel": "020-66666666",
            "desc": "待删除"
        })
        code, list_data = anon_client.get('/phones.php?action=list')
        phone_id = list_data[-1]['id']

        # 删除它
        code, body = anon_client.post('/phones.php?action=delete', json={
            "id": phone_id
        })
        assert body is True
