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


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
