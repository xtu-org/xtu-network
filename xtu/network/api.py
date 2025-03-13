from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol
from json.decoder import JSONDecodeError
from typing_extensions import override
from urllib.parse import quote
from functools import partial
import asyncio
import random
import httpx


from .exception import NoLoginError, LoginReadyError
from .const import NETWORK_TEST_URLS, RETRY_COUNT
from .models import LoginResult, OnlineUserInfo
from .utils import logger

if TYPE_CHECKING:

    class _ApiCall(Protocol):
        async def __call__(self, **kwargs: Any) -> Any: ...


HEADERS = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.1 Safari/605.1.15",
}


class XtuNetwork:
    """校园网 API"""

    def __init__(self, username: int, password: str):
        """
        :param username: 学号
        :param password: RSA 加密后的密码
        """
        self.username = username
        self.password = password
        self.client = httpx.AsyncClient(timeout=None, headers=HEADERS)

    @override
    def __getattr__(self, name: str, **data: Any) -> "_ApiCall":
        """调用 /eportal/InterFace.do 的 API"""
        if name.startswith("_") or name.endswith("_"):
            raise AttributeError(f"Attribute {name} not found")
        url = "http://172.16.0.32:8080/eportal/InterFace.do"
        data["params"] = {
            "method": name,
        }
        return partial(self.client.post, url, **data)

    async def aclose(self):
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.aclose()

    async def login(self) -> "LoginResult":
        """登录校园网"""
        if not self.password or not self.username:
            raise ValueError("用户名或密码不能为空")
        resp = await self.client.post(
            url="http://172.16.0.32:8080/eportal/InterFace.do",
            params={
                "method": "login",
            },
            data={
                "userId": self.username,
                "password": self.password,
                "service": "",
                "queryString": quote(await self.getQueryString()),
                "operatorPwd": "",
                "operatorUserId": "",
                "validcode": "",
                "passwordEncrypt": True,
            },
        )
        res: "LoginResult" = resp.json()
        self._userIndex = res.get("userIndex", None)

        return res

    async def getUserIndex(self) -> str:
        """获取用户索引
        注意：登录后才能调用该 API
        """
        if not hasattr(self, "_userIndex") or not self._userIndex:
            resp = await self.client.get(
                url="http://172.16.0.32:8080/eportal/redirectortosuccess.jsp",
            )
            if resp.next_request.url.host == "123.123.123.123":
                raise NoLoginError
            self._userIndex = resp.next_request.url.params.get("userIndex", None)
            return self._userIndex
        else:
            return self._userIndex

    async def getQueryString(self) -> str:
        """获取 queryString
        注意：登录后无法调用该 API
        """
        try:
            resp = await self.client.get(
                url="http://123.123.123.123",
            )
        except httpx.ReadError:
            raise LoginReadyError
        else:
            queryString = resp.text.replace(
                "<script>top.self.location.href='http://172.16.0.32:8080/eportal/index.jsp?",
                "",
            ).replace("'</script>", "")
            return queryString.replace("\r\n", "")

    async def logout(self):
        """注销校园网"""
        await self.client.post(
            url="http://172.16.0.32:8080/eportal/InterFace.do",
            params={
                "method": "logout",
            },
            data={
                "userIndex": await self.getUserIndex(),
            },
        )
        self._userIndex = None

    async def getOnlineUserInfo(self) -> "OnlineUserInfo" | dict:
        """获取在线用户信息
        注意：登录后才能调用该 API
        """
        for index in range(RETRY_COUNT):
            resp = await self.client.post(
                url="http://172.16.0.32:8080/eportal/InterFace.do",
                params={
                    "method": "getOnlineUserInfo",
                },
                data={
                    "userIndex": await self.getUserIndex(),
                },
            )
            try:
                res: "OnlineUserInfo" = resp.json()
            except JSONDecodeError:
                logger.warning(f"getOnlineUserInfo response is not json: {resp.text}")
                return {}

            if res["result"] == "success" or index == RETRY_COUNT - 1:
                return res

            await asyncio.sleep(random.randint(3, 8))

    async def getErrorMsg(self) -> str:
        """获取错误信息"""
        resp = await self.client.post(
            url="http://172.16.0.32:8080/eportal/userV2.do",
            params={
                "method": "getErrorMsg",
            },
            data={
                "userIndex": await self.getUserIndex(),
            },
        )
        return resp.text

    async def checkOnline(self) -> bool:
        """检查在线状态"""
        resp = await self.client.get(
            url="http://172.16.0.32:8080/eportal/redirectortosuccess.jsp",
        )
        if resp.next_request.url.host == "123.123.123.123":
            return False
        else:
            return True

    async def checkNetwork(self) -> bool:
        """检查实际网络状态"""

        async def _request(client: httpx.AsyncClient, url: str) -> bool:
            """请求"""
            try:
                resp = await client.get(url, timeout=None)
            except (httpx.ConnectError, httpx.ReadTimeout):
                return False
            else:
                if "<script>top.self.location.href='http://172.16.0.32:8080/eportal/index.jsp" in resp.text:
                    return False
                else:
                    return True

        result = await asyncio.gather(
            *[_request(self.client, url) for url in random.sample(NETWORK_TEST_URLS, 3)]
        )
        return any(item for item in result)
