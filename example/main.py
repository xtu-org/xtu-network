from xtu.network import XtuNetwork
from xtu.network import NoLoginError  # noqa: F401


async def main():
    async with XtuNetwork(202400001111, "password") as xtu:
        print(await xtu.login())
        print(await xtu.checkOnline())
        print(await xtu.getOnlineUserInfo())
        print(await xtu.checkNetwork())
        print(await xtu.logout())
