import asyncio
import telegram


from config import TG_TOKEN


async def main():
    bot = telegram.Bot(TG_TOKEN)  # type: ignore
    async with bot:
        update = (await bot.get_updates())[0]
        print(update.message.text)
        print(update.message.from_user.id)


if __name__ == "__main__":
    asyncio.run(main())
