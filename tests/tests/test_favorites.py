"""
收藏接口测试：收藏、取消收藏、收藏列表
"""
import pytest
import allure


@allure.epic("校园电话查询小程序")
@allure.feature("收藏模块")
class TestFavorites:

    @allure.story("收藏电话")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.favorite
    def test_add_favorite(self, anon_client, test_stu_id):
        """正常收藏：收藏一个电话"""
        # 拿一个电话
        code, phones = anon_client.get('/phones.php?action=list')
        phone = phones[0]

        code, result = anon_client.post('/favorites.php?action=add', json={
            "stuId": test_stu_id,
            "phone": phone
        })
        assert result is True

    @allure.story("收藏电话")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.favorite
    def test_add_duplicate_favorite(self, anon_client, test_stu_id):
        """重复收藏：同一电话收藏两次应返回 false"""
        code, phones = anon_client.get('/phones.php?action=list')
        phone = phones[1]

        # 第一次收藏
        anon_client.post('/favorites.php?action=add', json={
            "stuId": test_stu_id, "phone": phone
        })
        # 第二次收藏
        code, result = anon_client.post('/favorites.php?action=add', json={
            "stuId": test_stu_id, "phone": phone
        })
        assert result is False  # 已收藏过，返回 false

    @allure.story("收藏列表")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.favorite
    def test_favorite_list(self, anon_client, test_stu_id):
        """查看收藏列表：先收藏一个，再查列表"""
        code, phones = anon_client.get('/phones.php?action=list')
        phone = phones[2]
        anon_client.post('/favorites.php?action=add', json={
            "stuId": test_stu_id, "phone": phone
        })

        code, result = anon_client.get(f'/favorites.php?action=list&stuId={test_stu_id}')
        assert isinstance(result, list)
        assert len(result) >= 1

    @allure.story("取消收藏")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.favorite
    def test_remove_favorite(self, anon_client, test_stu_id):
        """取消收藏：先收藏再取消"""
        code, phones = anon_client.get('/phones.php?action=list')
        phone = phones[3]
        anon_client.post('/favorites.php?action=add', json={
            "stuId": test_stu_id, "phone": phone
        })

        code, result = anon_client.post('/favorites.php?action=remove', json={
            "stuId": test_stu_id,
            "id": phone['id']
        })
        assert result is True
