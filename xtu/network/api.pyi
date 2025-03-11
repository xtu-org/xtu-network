from typing import TypedDict, Literal, Optional
import httpx

from .const import MessageType, UserPackageType

class XtuNetwork:
    def __init__(self, username: int, password: str): ...
    async def __aenter__(self) -> "XtuNetwork": ...
    async def __aexit__(self, exc_type, exc_val, exc_tb): ...
    async def aclose(self) -> None: ...
    async def login(self) -> "LoginResult": ...
    async def getUserIndex(self) -> str: ...
    async def getQueryString(self) -> str: ...
    async def logout(self) -> None: ...
    async def getOnlineUserInfo(self) -> "OnlineUserInfo": ...
    async def checkOnline(self) -> bool: ...
    async def checkNetwork(self) -> bool: ...
    async def getErrorMsg(self, data: BodyData) -> httpx.Response:
        """获取错误信息"""

class OnlineUserInfo(TypedDict):
    """在线用户信息"""

    result: Literal["success", "fail"]
    """结果"""
    userPackage: UserPackageType
    """用户套餐"""
    userName: Optional[str]
    """用户姓名"""
    userIp: Optional[str]
    """用户 IP"""
    userId: Optional[str]
    """学号"""
    userIndex: Optional[str]
    """用户索引"""

class LoginResult(TypedDict):
    """登录响应"""

    userIndex: str
    """用户索引"""
    result: Literal["success", "fail"]
    """结果"""
    message: MessageType

class BodyData(TypedDict):
    """请求体数据"""

    userIndex: str
    """用户索引"""
