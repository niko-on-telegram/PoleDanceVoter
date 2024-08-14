from aiogram import Bot, types

default_commands = [
    types.BotCommand(command='/start', description='start bot'),
    types.BotCommand(command='/balance', description='check balance'),
]


async def set_bot_commands(bot: Bot) -> None:
    await bot.set_my_commands(default_commands)
