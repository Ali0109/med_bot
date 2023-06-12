from . import text, handlers, app


async def back_to_start(message, state):
    if message.text == text.back:
        await handlers.start_handler(message, state)
        await app.bot.send_message(
            message.from_user.id,
            f"Выбери другого дистра.",
        )
        return ""


async def back_to_distributor(message, state):
    if message.text == text.back:
        await handlers.distributor_handler(message, state)
        return ""
