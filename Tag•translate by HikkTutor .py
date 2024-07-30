#┏┓━┏┓━━┏┓━━┏┓━━┏━━━━┓━━━━━┏┓━━━━━━━━━━━━
#┃┃━┃┃━━┃┃━━┃┃━━┃┏┓┏┓┃━━━━┏┛┗┓━━━━━━━━━━━
#┃┗━┛┃┏┓┃┃┏┓┃┃┏┓┗┛┃┃┗┛┏┓┏┓┗┓┏┛┏━━┓┏━┓━━━━
#┃┏━┓┃┣┫┃┗┛┛┃┗┛┛━━┃┃━━┃┃┃┃━┃┃━┃┏┓┃┃┏┛━━━━
#┃┃━┃┃┃┃┃┏┓┓┃┏┓┓━┏┛┗┓━┃┗┛┃━┃┗┓┃┗┛┃┃┃━━━━━
#┗┛━┗┛┗┛┗┛┗┛┗┛┗┛━┗━━┛━┗━━┛━┗━┛┗━━┛┗┛━━━━━
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ---------------------------------------------------------------------------------
# Name: tag
# Description: Tag :
# -> Tag all admins (fast way to report).
# -> Tag all bots (why not ?).
# -> Tag all members (why not ?).\n
# Commands :
# Author: HitaloSama
# Commands:
# .admin | .all | .bot
# translate HikkTutor ---------------------------------------------------------------------------------


#    Friendly Telegram (telegram userbot)
#    By Magical Unicorn (based on official Anti PM & AFK Friendly Telegram modules)
#    Copyright (C) 2020 Magical Unicorn

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging

from telethon import functions, types
from telethon.tl.types import ChannelParticipantsAdmins, PeerChannel, PeerChat, PeerUser

from .. import loader, utils

logger = logging.getLogger(__name__)


def register(cb):
    cb(Tag())


@loader.tds
class TagMod(loader.Module):
    """
    Tag•translate by @HikkTutor:
    -> Упоминание всех админов (быстрый репорт).
    -> Упоминание всех ботов (почему нет?).
    -> Упоминание всех участников (для закрытых групп и сообществ друзей).\n
    Commands :

    """

    strings = {
        "name": "Tag•translate by @HikkTutor",
        "error_chat": (
            "<b>Эта команда может работать только в каналах и группах.</b>"
        ),
        "unknow": (
            "Незвестная ошибка."
            "\n\nПожалуйста, пришлите репорт проблемы из логов"
            "<a href='https://github.com/LegendaryUnicorn/FTG-Unofficial-Modules'>Github</a>."
        ),
        "user_link": "\n• <a href='tg://user?id={}'>{}</a>",
    }

    def config_complete(self):
        self.name = self.strings["name"]

    async def admincmd(self, message):
        """
        .admin : Упоминание всех админов (боты не в счет).
        .admin [сообщение] : Упоминание всех админов... .

        """
        if isinstance(message.to_id, PeerUser):
            await utils.answer(message, self.strings["error_chat"])
            return
        if utils.get_args_raw(message):
            rep = utils.get_args_raw(message)
        else:
            rep = ""
        user = await utils.get_target(message)
        if isinstance(message.to_id, PeerChat) or isinstance(
            message.to_id, PeerChannel
        ):
            async for user in message.client.iter_participants(
                message.to_id, filter=ChannelParticipantsAdmins
            ):
                if not user.bot:
                    user_name = user.first_name
                    if user.last_name is not None:
                        user_name += " " + user.last_name
                    rep += self.strings["user_link"].format(user.id, user_name)
            await utils.answer(message, rep)
        else:
            await utils.answer(message, self.strings["unknow"])

    async def allcmd(self, message):
        """
        .all : Упоминание всех участников .
        .all [сообщение] : Упоминание всех участников...

        """
        if isinstance(message.to_id, PeerUser):
            await utils.answer(message, self.strings["error_chat"])
            return
        if utils.get_args_raw(message):
            rep = utils.get_args_raw(message)
        else:
            rep = ""
        user = await utils.get_target(message)
        if isinstance(message.to_id, PeerChat) or isinstance(
            message.to_id, PeerChannel
        ):
            async for user in message.client.iter_participants(message.to_id):
                user_name = user.first_name
                if user.last_name is not None:
                    user_name += " " + user.last_name
                rep += self.strings["user_link"].format(user.id, user_name)
            await utils.answer(message, rep)
        else:
            await utils.answer(message, self.strings["unknow"])

    async def botcmd(self, message):
        """
        .bot : Упоминание всех ботов.
        .bot [сообщение] : Упоминание всех ботов...

        """
        if isinstance(message.to_id, PeerUser):
            await utils.answer(message, self.strings["error_chat"])
            return
        if utils.get_args_raw(message):
            rep = utils.get_args_raw(message)
        else:
            rep = ""
        user = await utils.get_target(message)
        if isinstance(message.to_id, PeerChat) or isinstance(
            message.to_id, PeerChannel
        ):
            async for user in message.client.iter_participants(message.to_id):
                if user.bot:
                    user_name = user.first_name
                    if user.last_name is not None:
                        user_name += " " + user.last_name
                    rep += self.strings["user_link"].format(user.id, user_name)
            await utils.answer(message, rep)
        else:
            await utils.answer(message, self.strings["unknow"])