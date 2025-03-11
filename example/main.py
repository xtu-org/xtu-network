from xtu.network import XtuNetwork
from xtu.network import NoLoginError


async def main():
    async with XtuNetwork(202400001111, "password") as xtu:
        print(await xtu.login())
        print(await xtu.checkOnline())

        print(await xtu.getErrorMsg())
        print(await xtu.getOnlineUserInfo())

        print(await xtu.checkNetwork())

        try:
            print(await xtu.logout())
        except NoLoginError:
            pass


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
