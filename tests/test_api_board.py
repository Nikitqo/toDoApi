import pytest
from httpx import AsyncClient


class TestCrudTask:

    @pytest.mark.anyio
    async def test_create_board(self, client: AsyncClient, create_user, prepare_board, delete_user):
        assert prepare_board.status_code == 200
        assert prepare_board.json()['name'] == 'test board'