"""
MIT License

Copyright (c) 2024 TheHamkerCat

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from pyrogram import filters
from pyrogram.types import Message

from wbb import SUDOERS, USERBOT_ID, USERBOT_PREFIX, app2, eor, log, telegraph

__MODULE__ = "Пользовательский бот"
TEXT = """
<code>alive</code>  →  Отправить сообщение о работе бота.<br>

<code>create (b|s|c) Title</code>  →  создать [обычную|супер]группу и канал<br>

<code>chatbot [ENABLE|DISABLE]</code>  →  Включить чатбот в чате.<br>

<code>autocorrect [ENABLE|DISABLE]</code>  →  Автоматически исправлять ваши сообщения на лету.<br>

<code>purgeme [Количество сообщений для удаления]</code>  →  Удалить ваши собственные сообщения.<br>

<code>eval [Строки кода]</code>  →  Выполнить Python код.<br>

<code>lsTasks</code>  →  Список выполняющихся задач (eval)<br>

<code>sh [Код оболочки]</code>  →  Выполнить Shell код.<br>

<code>approve</code>  →  Одобрить пользователя для отправки личных сообщений.<br>

<code>disapprove</code>  →  Отклонить пользователя для отправки личных сообщений.<br>

<code>block</code>  →  Заблокировать пользователя.<br>

<code>unblock</code>  →  Разблокировать пользователя.<br>

<code>anonymize</code>  →  Случайно изменить имя/аватар.<br>

<code>impersonate [User_ID|Username|Reply]</code> → Клонировать профиль пользователя.<br>

<code>useradd</code>  →  Добавить пользователя в sudoers. [НЕБЕЗОПАСНО]<br>

<code>userdel</code>  → Удалить пользователя из sudoers.<br>

<code>sudoers</code>  →  Список sudo пользователей.<br>

<code>download [URL или ответ на файл]</code>  →  Скачать файл из TG или по URL<br>

<code>upload [URL или путь к файлу]</code>  →  Загрузить файл с локального диска или по URL<br>

<code>parse_preview [ОТВЕТ НА СООБЩЕНИЕ]</code>  →  Разобрать предварительный просмотр веб-страницы(ссылки)<br>

<code>id</code>  →  То же что /id, но для Ubot<br>

<code>paste</code> → Вставить на batbin.<br>

<code>help</code> → Получить ссылку на эту страницу.<br>

<code>kang</code> → Украсть стикеры.<br>

<code>dice</code> → Бросить кубик.<br>
"""
log.info("Pasting userbot commands on telegraph")

__HELP__ = f"""**Commands:** {telegraph.create_page(
    "Команды пользовательского бота",
    html_content=TEXT,
)['url']}"""

log.info("Done pasting userbot commands on telegraph")


@app2.on_message(
    filters.command("help", prefixes=USERBOT_PREFIX)
    & ~filters.forwarded
    & ~filters.via_bot
    & filters.user(USERBOT_ID)
)
async def get_help(_, message: Message):
    await eor(
        message,
        text=__HELP__,
        disable_web_page_preview=True,
    )


@app2.on_message(
    filters.command(["purgeme", "purge_me"], prefixes=USERBOT_PREFIX)
    & ~filters.forwarded
    & ~filters.via_bot
    & filters.user(USERBOT_ID)
)
async def purge_me_func(_, message: Message):
    if len(message.command) != 2:
        return await message.delete()

    n = message.text.split(None, 1)[1].strip()
    if not n.isnumeric():
        return await eor(message, text="Неверные аргументы")

    n = int(n)

    if n < 1:
        return await eor(message, text="Нужно число >=1")

    chat_id = message.chat.id

    message_ids = [
        m.id
        async for m in app2.search_messages(
            chat_id,
            from_user=int(USERBOT_ID),
            limit=n,
        )
    ]

    if not message_ids:
        return await eor(message, text="Сообщения не найдены.")

    # A list containing lists of 100 message chunks
    # because we can't delete more than 100 messages at once,
    # we have to do it in chunks of 100, i'll choose 99 just
    # to be safe.
    to_delete = [
        message_ids[i : i + 99] for i in range(0, len(message_ids), 99)
    ]

    for hundred_messages_or_less in to_delete:
        await app2.delete_messages(
            chat_id=chat_id,
            message_ids=hundred_messages_or_less,
            revoke=True,
        )
