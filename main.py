import os
import io
import uuid
import dotenv
import qrcode
# from qrcode.image.styledpil import StyledPilImage
# from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from telethon import TelegramClient, events


BOT_GREETING_MESSAGE = """Hello there. I am a bot that can generate QR codes. Send me any text and I will give you your QR"""


def generate_qrcode(text: str) -> io.BytesIO:
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(text)
    # img = qr.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer())
    img = qr.make_image()
    img_b = io.BytesIO()
    img.save(img_b, format="png")
    img_b.seek(0)
    img_name = "qr-"+str(uuid.uuid4())+".png"
    img_b.name = img_name
    return img_b


def main() -> None:
    dotenv.load_dotenv()

    with TelegramClient(
        "anything",
        api_id=os.getenv("TG_APP_API_ID"),
        api_hash=os.getenv("TG_APP_API_HASH"),
    ) as client:

        @client.on(events.NewMessage(incoming=True))
        async def handle_text(event) -> None:
            if event.raw_text == "/start":
                await event.respond(BOT_GREETING_MESSAGE)
                return

            img_b = generate_qrcode(event.raw_text)
            await event.reply(file=img_b, force_document=False)
            img_b.close()

        print("Started")

        client.start()
        client.run_until_disconnected()


if __name__ == "__main__":
    main()
