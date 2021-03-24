# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

import io
import math
import random
import urllib.request
from os import remove

from PIL import Image
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.types import (
    DocumentAttributeFilename,
    DocumentAttributeSticker,
    InputStickerSetID,
    MessageMediaPhoto,
)

from userbot import CMD_HELP, bot, S_PACK_NAME as custompack
from userbot.events import register


KANGING_STR = [
    "ᴡᴀᴏ.,ʙᴀɢᴜꜱ ɴɪʜ...ᴄᴏʟᴏɴɢ ᴅᴜʟᴜ ʏᴇᴋᴀɴ..",
    "𝕮𝖔𝖑𝖔𝖓𝖌 𝕾𝖙𝖎𝖈𝖐𝖊𝖗 𝖉𝖚𝖑𝖚 𝖞𝖊𝖊 𝖐𝖆𝖓",
    "𝕖𝕙𝕙, 𝕞𝕒𝕟𝕥𝕖𝕡 𝕟𝕚𝕙.....𝕒𝕜𝕦 𝕔𝕠𝕝𝕠𝕟𝕘 𝕪𝕒...",
    "𝙄𝙣𝙞 𝙎𝙩𝙞𝙘𝙠𝙚𝙧 𝙖𝙠𝙪 𝙘𝙤𝙡𝙤𝙣𝙜 𝙮𝙖𝙖\n𝘿𝙐𝘼𝙍𝙍!",
    "𝚕𝚎𝚑 𝚞𝚐𝚑𝚊 𝚗𝚒 𝚂𝚝𝚒𝚌𝚔𝚎𝚛\nᶜᵒˡᵒⁿᵍ ᵃʰʰ~",
    "Pιɱ Pιɱ Pσɱ!!!\n🄽🄸 🅂🅃🄸🄲🄺🄴🅁 🄿🅄🄽🅈🄰 🄰🄸🄽🄶 🅂🄴🄺🄰🅁🄰🄽🄶 🄷🄴🄷🄴",
    "̷C̷o̷l̷o̷n̷g ̷l̷a̷g̷i ̷y̷e̷e ̷k̷a̷n.....",
    "̷𝕮𝖔𝖑𝖔𝖓𝖌 𝕿𝖊𝖗𝖔𝖘𝖘",
    "★彡[ʙᴏʟᴇʜᴋᴀʜ ꜱᴀʏᴀ ᴄᴏʟᴏɴɢ ɴɪ ꜱᴛɪᴄᴋᴇʀ]彡★\n★彡[ᴀᴜ ᴀʜ ᴄᴏʟᴏɴɢ ᴀᴊᴀ ʜᴇʜᴇ]彡★",
    "█▓▒­░⡷⠂CФLФИG SΓICҜΞЯ ДHH⠐⢾░▒▓█.....",
]


@register(outgoing=True, pattern=r"^\.(?:colong|kang)\s?(.)?")
async def kang(args):
    user = await bot.get_me()
    if not user.username:
        user.username = user.first_name
    message = await args.get_reply_message()
    photo = None
    emojibypass = False
    is_anim = False
    emoji = None

    if message and message.media:
        if isinstance(message.media, MessageMediaPhoto):
            await args.edit(f"`{random.choice(KANGING_STR)}`")
            photo = io.BytesIO()
            photo = await bot.download_media(message.photo, photo)
        elif "image" in message.media.document.mime_type.split("/"):
            await args.edit(f"`{random.choice(KANGING_STR)}`")
            photo = io.BytesIO()
            await bot.download_file(message.media.document, photo)
            if (
                DocumentAttributeFilename(file_name="sticker.webp")
                in message.media.document.attributes
            ):
                emoji = message.media.document.attributes[1].alt
                if emoji != "":
                    emojibypass = True
        elif "tgsticker" in message.media.document.mime_type:
            await args.edit(f"`{random.choice(KANGING_STR)}`")
            await bot.download_file(message.media.document, "AnimatedSticker.tgs")

            attributes = message.media.document.attributes
            for attribute in attributes:
                if isinstance(attribute, DocumentAttributeSticker):
                    emoji = attribute.alt

            emojibypass = True
            is_anim = True
            photo = 1
        else:
            return await args.edit("`★彡[ꜰɪʟᴇ ᴛɪᴅᴀᴋ ᴅɪᴅᴜᴋᴜɴɢ ᴀᴊɢ!]彡★`")
    else:
        return await args.edit("`𓂀 𝔾𝕒𝕘𝕒𝕝 ℂ𝕠𝕝𝕠𝕟𝕘 ℂ𝕒𝕣𝕚 𝕐𝕒𝕟𝕘 𝕃𝕒𝕖𝕟! 𓂀`")

    if photo:
        splat = args.text.split()
        if not emojibypass:
            emoji = "➖"
        pack = 1
        if len(splat) == 3:
            pack = splat[2]  # User sent both
            emoji = splat[1]
        elif len(splat) == 2:
            if splat[1].isnumeric():
                # User wants to push into different pack, but is okay with
                # thonk as emote.
                pack = int(splat[1])
            else:
                # User sent just custom emote, wants to push to default
                # pack
                emoji = splat[1]

        u_name = user.username
        f_name = user.first_name
        packname = f"sticker_by_{u_name}_{pack}X"
        custom_packnick = f"{custompack}" or f"{f_name}"
        packnick = f"{custom_packnick} Vol.{pack}"
        cmd = "/newpack"
        file = io.BytesIO()

        if not is_anim:
            image = await resize_photo(photo)
            file.name = "sticker.png"
            image.save(file, "PNG")
        else:
            packname += "_anim"
            packnick += " (Animated)"
            cmd = "/newanimated"

        response = urllib.request.urlopen(
            urllib.request.Request(f"http://t.me/addstickers/{packname}")
        )
        htmlstr = response.read().decode("utf8").split("\n")

        if (
            "  A <strong>Telegram</strong> user has created the <strong>Sticker&nbsp;Set</strong>."
            not in htmlstr
        ):
            async with bot.conversation("Stickers") as conv:
                await conv.send_message("/addsticker")
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.send_message(packname)
                x = await conv.get_response()
                while "120" in x.text:
                    pack += 1
                    packname = f"sticker_by_{u_name}_{pack}X"
                    packnick = f"{custom_packnick} Vol.{pack}"
                    await args.edit(
                        "`Switching to Pack "
                        + str(pack)
                        + " due to insufficient space`"
                    )
                    await conv.send_message(packname)
                    x = await conv.get_response()
                    if x.text == "Invalid pack selected.":
                        await conv.send_message(cmd)
                        await conv.get_response()
                        # Ensure user doesn't get spamming notifications
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.send_message(packnick)
                        await conv.get_response()
                        # Ensure user doesn't get spamming notifications
                        await bot.send_read_acknowledge(conv.chat_id)
                        if is_anim:
                            await conv.send_file("AnimatedSticker.tgs")
                            remove("AnimatedSticker.tgs")
                        else:
                            file.seek(0)
                            await conv.send_file(file, force_document=True)
                        await conv.get_response()
                        await conv.send_message(emoji)
                        # Ensure user doesn't get spamming notifications
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        await conv.send_message("/publish")
                        if is_anim:
                            await conv.get_response()
                            await conv.send_message(f"<{packnick}>")
                        # Ensure user doesn't get spamming notifications
                        await conv.get_response()
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.send_message("/skip")
                        # Ensure user doesn't get spamming notifications
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        await conv.send_message(packname)
                        # Ensure user doesn't get spamming notifications
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        # Ensure user doesn't get spamming notifications
                        await bot.send_read_acknowledge(conv.chat_id)
                        return await args.edit(
                            "`Sticker ditambahkan ke pack yang berbeda !"
                            "\nIni pack yang baru saja kamu buat!"
                            f"\nKlik [disini](t.me/addstickers/{packname}) untuk liat pack kamu",
                            parse_mode="md",
                        )
                if is_anim:
                    await conv.send_file("AnimatedSticker.tgs")
                    remove("AnimatedSticker.tgs")
                else:
                    file.seek(0)
                    await conv.send_file(file, force_document=True)
                rsp = await conv.get_response()
                if "Sorry, the file type is invalid." in rsp.text:
                    return await args.edit(
                        "`gagal menambahkan sticker, gunakan` @Stickers `bot untuk menambahkan sticker.`"
                    )
                await conv.send_message(emoji)
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await conv.send_message("/done")
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
        else:
            await args.edit("`Membuat Pack baru`")
            async with bot.conversation("Stickers") as conv:
                await conv.send_message(cmd)
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.send_message(packnick)
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                if is_anim:
                    await conv.send_file("AnimatedSticker.tgs")
                    remove("AnimatedSticker.tgs")
                else:
                    file.seek(0)
                    await conv.send_file(file, force_document=True)
                rsp = await conv.get_response()
                if "Sorry, the file type is invalid." in rsp.text:
                    return await args.edit(
                        "`gagal menambahkan sticker, gunakan` @Stickers `bot untuk menambahkan sticker.`"
                    )
                await conv.send_message(emoji)
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await conv.send_message("/publish")
                if is_anim:
                    await conv.get_response()
                    await conv.send_message(f"<{packnick}>")
                # Ensure user doesn't get spamming notifications
                await conv.get_response()
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.send_message("/skip")
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await conv.send_message(packname)
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)

        await args.edit(
            "`Sticker Sukses Dibuat!`"
            f"\n    🔥 **[KLIK DISINI](t.me/addstickers/{packname})** 🔥\nUntuk Menggunakan Sticker",
            parse_mode="md",
        )


async def resize_photo(photo):
    image = Image.open(photo)
    if (image.width and image.height) < 512:
        size1 = image.width
        size2 = image.height
        if size1 > size2:
            scale = 512 / size1
            size1new = 512
            size2new = size2 * scale
        else:
            scale = 512 / size2
            size1new = size1 * scale
            size2new = 512
        size1new = math.floor(size1new)
        size2new = math.floor(size2new)
        sizenew = (size1new, size2new)
        image = image.resize(sizenew)
    else:
        maxsize = (512, 512)
        image.thumbnail(maxsize)

    return image


@register(outgoing=True, pattern=r"^\.stkrinfo$")
async def get_pack_info(event):
    if not event.is_reply:
        return await event.edit(
            "`Aku tidak bisa mengambil info dari apapun, bisakah aku?!`"
        )

    rep_msg = await event.get_reply_message()
    if not rep_msg.document:
        return await event.edit("`Balas ke sticker untuk melihat detail pack`")

    try:
        stickerset_attr = rep_msg.document.attributes[1]
        await event.edit("`Fetching details of the sticker pack, please wait..`")
    except BaseException:
        return await event.edit("`Ini bukan sticker,balas ke sticker.`")

    if not isinstance(stickerset_attr, DocumentAttributeSticker):
        return await event.edit("`Ini bukan sticker,balas ke sticker.`")

    get_stickerset = await bot(
        GetStickerSetRequest(
            InputStickerSetID(
                id=stickerset_attr.stickerset.id,
                access_hash=stickerset_attr.stickerset.access_hash,
            )
        )
    )
    pack_emojis = []
    for document_sticker in get_stickerset.packs:
        if document_sticker.emoticon not in pack_emojis:
            pack_emojis.append(document_sticker.emoticon)

    OUTPUT = (
        f"**Sticker Title:** `{get_stickerset.set.title}\n`"
        f"**Sticker Short Name:** `{get_stickerset.set.short_name}`\n"
        f"**Official:** `{get_stickerset.set.official}`\n"
        f"**Archived:** `{get_stickerset.set.archived}`\n"
        f"**Stickers In Pack:** `{len(get_stickerset.packs)}`\n"
        f"**Emojis In Pack:**\n{' '.join(pack_emojis)}"
    )

    await event.edit(OUTPUT)


@register(outgoing=True, pattern=r"^\.getsticker$")
async def sticker_to_png(sticker):
    if not sticker.is_reply:
        await sticker.edit("`NULL information to fetch...`")
        return False

    img = await sticker.get_reply_message()
    if not img.document:
        await sticker.edit("`Reply ke suatu stiker...`")
        return False

    try:
        img.document.attributes[1]
    except Exception:
        await sticker.edit("`Ini bukan sticker...`")
        return

    with io.BytesIO() as image:
        await sticker.client.download_media(img, image)
        image.name = "sticker.png"
        image.seek(0)
        try:
            await img.reply(file=image, force_document=True)
        except Exception:
            await sticker.edit("`Err, gak bisa ngirim file...`")
        else:
            await sticker.delete()
    return


CMD_HELP.update(
    {
        "stickers": ">`.kang | .colong [emoji('s)]?`"
        "\nUsage: Reply .kang to a sticker or an image to kang it to your userbot pack "
        "\nor specify the emoji you want to."
        "\n\n>`.kang | .colong  (emoji['s]]?` [number]?"
        "\nUsage: Kang's the sticker/image to the specified pack but uses 🤔 as emoji "
        "or choose the emoji you want to."
        "\n\n>`.stkrinfo`"
        "\nUsage: Gets info about the sticker pack."
        "\n\n>`.getsticker`"
        "\nUsage: reply to a sticker to get 'PNG' file of sticker."})
