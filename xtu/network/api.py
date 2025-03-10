from typing import TYPE_CHECKING, Any, Protocol, TypedDict, Literal
from typing_extensions import override
from urllib.parse import quote
from functools import partial
import asyncio
import random
import httpx


from .exception import NoLoginError

if TYPE_CHECKING:

    class _ApiCall(Protocol):
        async def __call__(self, **kwargs: Any) -> Any: ...


HEADERS = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.1 Safari/605.1.15",
}


class XtuNetwork:
    """"""

    def __init__(self, username: int, password: str):
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

    async def login(self):
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

        class LoginResult(TypedDict):
            """登录响应"""

            userIndex: str
            """用户索引"""
            result: Literal["success", "fail"]
            """结果"""
            message: Literal["", "用户不存在或者密码错误!"]

        return res

    async def getUserIndex(self) -> str:
        """获取用户索引"""
        if not hasattr(self, "_userIndex"):
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
        resp = await self.client.get(
            url="http://123.123.123.123",
        )
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

    async def getOnlineUserInfo(self) -> dict:
        """获取在线用户信息
        注意：登录后才能调用该 API
        """
        resp = await self.client.post(
            url="http://172.16.0.32:8080/eportal/InterFace.do",
            params={
                "method": "getOnlineUserInfo",
            },
            data={
                "userIndex": await self.getUserIndex(),
            },
        )
        res: "OnlineUserInfo" = resp.json()

        class OnlineUserInfo(TypedDict):
            """在线用户信息"""

            userPackage: Literal["学生电信宽带套餐"]
            """用户套餐"""
            userName: str
            """用户姓名"""
            userIp: str
            """用户 IP"""
            userId: str
            """学号"""
            userIndex: str
            """用户索引"""
            maxLeavingTime: str
            """最大在线时间"""

        return res

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
        urls = [
            "http://www.baidu.com",
            "http://www.qq.com",
            "http://www.sohu.com",
            "https://www.zhihu.com",
            "https://www.bilibili.com",
            "https://weibo.com",
            "https://sogou.com",
            "https://www.taobao.com",
            "https://www.jd.com",
            "https://www.douyin.com",
            "https://www.apple.com.cn",
            "https://www.mi.com",
            "https://weread.qq.com",
            "https://cloud.tencent.com",
            "https://www.huaweicloud.com",
            "https://www.aliyun.com",
        ]
        result = await asyncio.gather(*[self.client.get(url) for url in random.sample(urls, 3)])
        return any(r.status_code == 200 for r in result)
