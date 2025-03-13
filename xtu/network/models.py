from typing import Literal, Optional, TypedDict
from json.decoder import JSONDecodeError
import json

from .const import UserPackageType, MessageType


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
    mabInfoMaxCount: int
    """最大设备数量"""
    ballInfo: str
    """校园网信息"""

    @staticmethod
    def get_online_count_from_ball_info(ballInfo: str) -> int:
        """获取在线设备数量"""
        try:
            data: list[dict] = json.loads(ballInfo)
            return int(next((item["value"] for item in data if item["id"] == "onlinedevice"), 0))
        except (JSONDecodeError, KeyError):
            return 0


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
