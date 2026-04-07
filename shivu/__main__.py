import asyncio
import os
from aiohttp import web
from shivu import application, shivuu, LOGGER

async def handle(request): return web.Response(text="Bot is Alive!")

async def main():
    # Render Keep-Alive Server
    app = web.Application(); app.router.add_get('/', handle)
    runner = web.AppRunner(app); await runner.setup()
    await web.TCPSite(runner, '0.0.0.0', int(os.environ.get("PORT", 10000))).start()

    # Start Both Clients
    await shivuu.start()
    async with application:
        await application.initialize()
        await application.start_polling()
        LOGGER.info("Gʀᴀsᴘ Cʜᴀʀᴀᴄᴛᴇʀs Pro is Online! 🚀")
        await asyncio.Event().wait()

if __name__ == '__main__':
    asyncio.run(main())
