<center><div align="center">

<img src="https://www.xtu.edu.cn/images/logo.png" width="236" height="80" style="border-radius: 50%"></img>

<img alt="version" src="https://img.shields.io/github/last-commit/xtu-org/xtu-network.svg?style=for-the-badge&label=%E6%9C%80%E5%90%8E%E6%9B%B4%E6%96%B0&logo=velog&logoColor=BE95FF&color=7B68EE"/></img>
<img alt="stars" src="https://img.shields.io/github/stars/xtu-org/xtu-network.svg?style=for-the-badge&label=Stars&logo=undertale&logoColor=orange&color=orange"/></img>
<img alt="forks" src="https://img.shields.io/github/forks/xtu-org/xtu-network.svg?style=for-the-badge&label=Forks&logo=stackshare&logoColor=f92f60&color=f92f60"/></img>
<img alt="pr" src="https://img.shields.io/github/issues-pr-closed/xtu-org/xtu-network.svg?style=for-the-badge&label=PR&logo=addthis&logoColor=green&color=0AC18E"/></img>
<img alt="issues" src="https://img.shields.io/github/issues/xtu-org/xtu-network.svg?style=for-the-badge&label=Issues&logo=openbugbounty&logoColor=e38dff&color=e38dff"/></img>

</div></center>

<div align="center" style="font-weight:bold"><b>湘潭大学 校园网 API</b></div>  

## 安装

从 PyPI 安装：

```bash
pip install xtu-network
```

从 GitHub 安装：

```bash
pip install git+https://github.com/xtu-org/xtu-network.git@main#egg=xtu-network
```

## 示例

简单代码示例

```python
from xtu.network import XtuNetwork
from xtu.network import NoLoginError
from xtu.network import OnlineUserInfo

async def main():
    async with XtuNetwork(202400001111, "rsa_password") as xtu:
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

- `XtuNetwork` 类用于连接校园网。
- `getErrorMsg()` 乍一看是获取错误信息，实际上什么也不返回，但是不调用此 API 的话 `getOnlineUserInfo` 就无法正确返回。
- `getOnlineUserInfo()` 用于获取在线用户信息，返回一个字典。
- `checkNetwork()` 用于检查网络状态，返回一个布尔值。
- `logout()` 用于退出校园网，无返回值，如果尚未登录则抛出 `NoLoginError` 异常。

**如何获得 RSA 加密后的密码？**

使用 [security.html](https://github.com/xtu-org/xtu-network/blob/main/example/web/security.html) 获取，或者 F12 查看校园网登录请求。

自 0.0.29 版开始，可以传入未加密的代码，将自动完成 RSA 加密。

## 开源协议

本仓库使用 [AGPL-3.0](https://www.gnu.org/licenses/agpl-3.0.en.html) 协议，注意事项：

1. **源代码共享义务**：使用或修改此软件进行开发或提供网络服务时，必须提供完整的源代码。
2. **网络应用条款**：若通过网络向用户提供此程序的功能，必须确保用户能够获取到相应的源代码。
3. **许可证继承**：任何分发的修改版必须继续使用AGPL-3.0许可证，确保后续版本的开放性和共享要求。
4. **修改版标识**：任何分发的修改版本须在显著位置标明已修改，并附上具体修改的内容和日期。
5. **专利权警示**：使用此软件即表明你接受并遵循软件中规定的专利权限。
6. **免责条款**：软件按“现状”提供，不提供任何明示或暗示的保证。使用软件所产生的任何风险由用户自行承担。
