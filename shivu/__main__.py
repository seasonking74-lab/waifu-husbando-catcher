import asyncio
from aiohttp import web
from shivu import application, shivuu, LOGGER
import shivu.modules.game, shivu.modules.upload, shivu.modules.harem, shivu.modules.leaderboard

async def handle(request): return web.Response(text="Bot is Alive!")

async def main():
    # Render Keep-Alive
    app = web.Application(); app.router.add_get('/', handle)
    runner = web.AppRunner(app); await runner.setup()
    await web.TCPSite(runner, '0.0.0.0', 10000).start()

    # Start Clients
    await shivuu.start()
    async with application:
        await application.initialize()
        await application.start_polling()
        LOGGER.info("Gʀᴀsᴘ Cʜᴀʀᴀᴄᴛᴇʀs Is Lɪᴠᴇ! 🚀")
        await asyncio.Event().wait()

if __name__ == '__main__':
    asyncio.run(main())
