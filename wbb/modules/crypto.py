from pyrogram import filters

from wbb import app
from wbb.core.decorators.errors import capture_err
from wbb.core.keyboard import ikb
from wbb.core.sections import section
from wbb.utils.http import get

__MODULE__ = "Crypto"
__HELP__ = """
/crypto [валюта]
        Получить курс валюты в реальном времени.
"""


@app.on_message(filters.command("crypto"))
@capture_err
async def crypto(_, message):
    if len(message.command) < 2:
        return await message.reply("/crypto [валюта]")

    currency = message.text.split(None, 1)[1].lower()

    btn = ikb(
        {"Доступные валюты": "https://plotcryptoprice.herokuapp.com"},
    )

    m = await message.reply("`Обработка...`")

    try:
        r = await get(
            "https://x.wazirx.com/wazirx-falcon/api/v2.0/crypto_rates",
            timeout=5,
        )
    except Exception:
        return await m.edit("[ОШИБКА]: Что-то пошло не так.")

    if currency not in r:
        return await m.edit(
            "[ОШИБКА]: НЕВЕРНАЯ ВАЛЮТА",
            reply_markup=btn,
        )

    body = {i.upper(): j for i, j in r.get(currency).items()}

    text = section(
        "Текущие курсы криптовалют для " + currency.upper(),
        body,
    )
    await m.edit(text, reply_markup=btn)
