# 湘潭大学 校园网 API

## 安装

从 PyPI 安装：
```bash
pip install xtu-network
```

从 GitHub 安装：
```bash
pip install git+https://github.com/xtu-hit/xtu-network-python.git@main#egg=xtu-network
```

## 示例

简单示例
```python
from xtu.network import XtuNetwork
from xtu.network import NoLoginError
from xtu.network import OnlineUserInfo

async def main():
    async with XtuNetwork(202400001111, "password") as xtu:
        print(await xtu.login())
        print(await xtu.checkOnline())

        print(await xtu.getErrorMsg())
        print(res := await xtu.getOnlineUserInfo())

        print(OnlineUserInfo.get_online_count_from_ball_info(res["ballInfo"]))

        print(await xtu.checkNetwork())

        try:
            print(await xtu.logout())
        except NoLoginError:
            pass
```
详见 [example.py](https://github.com/xtu-org/xtu-network/blob/main/example/main.py) 用法

## 说明

- `XtuNetwork` 类是 `xtu.network` 模块的网络类，用于连接校园网。
- `NoLoginError` 异常是 `xtu.network` 模块的异常类，用于表示尚未登录校园网。

- `getErrorMsg()` 乍一看是获取错误信息，实际上什么也不返回，但是不调用此 API 的话 `getOnlineUserInfo` 就无法正确返回。
- `getOnlineUserInfo()` 用于获取在线用户信息，返回一个字典。
- `checkNetwork()` 用于检查网络状态，返回一个布尔值。
- `logout()` 用于退出校园网，无返回值，如果尚未登录则抛出 `NoLoginError` 异常。

## 开源协议

本仓库使用 [AGPL-3.0](https://www.gnu.org/licenses/agpl-3.0.en.html) 协议，注意事项：

1. **源代码共享义务**：使用或修改此软件进行开发或提供网络服务时，必须提供完整的源代码。

2. **网络应用条款**：若通过网络向用户提供此程序的功能，必须确保用户能够获取到相应的源代码。

3. **许可证继承**：任何分发的修改版必须继续使用AGPL-3.0许可证，确保后续版本的开放性和共享要求。

4. **修改版标识**：任何分发的修改版本须在显著位置标明已修改，并附上具体修改的内容和日期。

5. **专利权警示**：使用此软件即表明你接受并遵循软件中规定的专利权限。

6. **免责条款**：软件按“现状”提供，不提供任何明示或暗示的保证。使用软件所产生的任何风险由用户自行承担。
