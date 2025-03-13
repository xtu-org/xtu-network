from xtu.network import XtuNetwork
from xtu.network import NoLoginError
from xtu.network import OnlineUserInfo
from xtu.network import LoginReadyError


async def main():
    async with XtuNetwork(202400001111, "password") as xtu:
        try:
            print(await xtu.login())
        except LoginReadyError:
            print("Login is not ready yet.")

        print(await xtu.checkOnline())

        print(await xtu.getErrorMsg())
        print(res := await xtu.getOnlineUserInfo())

        print(OnlineUserInfo.get_online_count_from_ball_info(res["ballInfo"]))

        print(await xtu.checkNetwork())

        try:
            print(await xtu.logout())
        except NoLoginError:
            print("Not logged in.")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
