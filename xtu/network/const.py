from typing import TypeAlias, Literal
import os

MessageType: TypeAlias = Literal[
    "",
    "用户不存在或者密码错误!",
    "您的账户已欠费，为了不影响您正常使用网络，请尽快缴费!",
    "用户不存在,请输入正确的用户名!",
    "您未绑定服务对应的运营商!",
    "你使用的账号已达到同时在线用户数量上限!",
    "运营商用户认证失败!失败原因[[Code 3]: Unable to find user in database]",
    "运营商用户认证失败!失败原因[109026012|109020105|The subscriber is deregistered or the password is incorrect]",
    "运营商用户认证失败!失败原因[RD103]",
    "运营商用户认证失败!失败原因[109026002|109020122|The subscriber status is incorrect.]",
    "运营商用户认证失败!失败原因[[Code 4]: User status is not RUN]",
    "认证设备响应超时,请稍后再试!",
    "运营商用户认证失败!失败原因[RD104]",
    "只允许该运营商用户使用校园网账号登录!",
    "用户ID与密码不匹配,请输入与用户ID相匹配的密码!",
    "运营商用户认证失败!失败原因[109026004|109020109|Reject by concurrency control.]",
    "运营商用户认证失败!失败原因[109026001|109020102|The subscriber is deregistered or the password is incorrect.]",
]

UserPackageType: TypeAlias = Literal[
    "学生电信宽带套餐",
    "学生联通宽带套餐",
    "学生移动宽带套餐",
    "学生校园网有线包月",
]


NETWORK_TEST_URLS = [
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


RETRY_COUNT = int(os.getenv("XTU_NETWORK_RETRY_COUNT", 20))
