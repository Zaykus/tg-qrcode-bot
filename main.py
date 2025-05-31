import os
import io
import uuid
import dotenv
import qrcode
from qrcode.image.pil import PilImage
from telethon import TelegramClient, events
from telethon.tl.custom import Button # Import Button for keyboard markups


BOT_GREETING_MESSAGE = """Hello there! I am a bot that can generate QR codes.

Choose an option below to get started:"""

BOT_HELP_MESSAGE = """
🤖 *QR Code Bot Commands:*

➡️ Send any text to generate a standard black and white QR code.

🎨 */color_qr*
    - Choose a color for your QR code using buttons!

👋 */start*
    - Displays the welcome message and main menu.

❓ */help*
    - Shows this help message.

_Tips:_
- The longer your text, the denser the QR code will be!
"""

# Define common colors for buttons
COLOR_OPTIONS = {
    "Red": "#FF0000",
    "Blue": "#0000FF",
    "Green": "#00FF00",
    "Purple": "#800080",
    "Orange": "#FFA500",
    "Black": "#000000" # Default black
}

# --- User state management ---
# A dictionary to store the state for each user.
# Key: user_id (int)
# Value: state_string (str) e.g., "waiting_for_text_for_color_qr", "idle"
user_states = {}
# --- End user state management ---


def generate_qrcode(text: str, fill_color: str = "black", back_color: str = "white") -> io.BytesIO:
    """Generates a QR code image from text with specified fill and background colors."""
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(image_factory=PilImage, fill_color=fill_color, back_color=back_color)
    
    img_b = io.BytesIO()
    img.save(img_b, format="png")
    img_b.seek(0)
    img_name = "qr-"+str(uuid.uuid4())+".png"
    img_b.name = img_name
    return img_b


def get_main_menu_keyboard():
    """Returns the main menu keyboard."""
    return client.build_reply_markup([
        Button.inline("Generate Regular QR", data="regular_qr_mode"),
        Button.inline("Generate Colored QR", data="color_qr_mode")
    ])

def get_color_selection_keyboard():
    """Returns the color selection keyboard."""
    buttons = []
    # Create buttons in two columns
    color_names = list(COLOR_OPTIONS.keys())
    for i in range(0, len(color_names), 2):
        row = []
        if i < len(color_names):
            name1 = color_names[i]
            row.append(Button.inline(name1, data=f"set_color_{COLOR_OPTIONS[name1]}"))
        if i + 1 < len(color_names):
            name2 = color_names[i+1]
            row.append(Button.inline(name2, data=f"set_color_{COLOR_OPTIONS[name2]}"))
        buttons.append(row)
    
    buttons.append([Button.inline("⬅️ Back to Main Menu", data="back_to_main")]) # Add a back button
    return client.build_reply_markup(buttons)


async def send_color_mode_prompt(event, user_id):
    """Sends the prompt to choose a color for the QR code."""
    await event.respond("Choose a color for your QR code:", buttons=get_color_selection_keyboard())
    # No specific state needed here, as the color selection itself drives the next action


async def handle_qr_generation(event, text_data, user_id, fill_color="black", back_color="white"):
    """Handles the actual QR code generation and sending."""
    try:
        img_b = generate_qrcode(text_data, fill_color=fill_color, back_color=back_color)
        await event.reply(file=img_b, force_document=False)
    except Exception as e:
        print(f"Error generating or sending QR: {e}")
        await event.reply("Sorry, something went wrong while generating your QR code.")
    finally:
        if 'img_b' in locals() and not img_b.closed:
            img_b.close()
        # Reset state after QR code is sent
        user_states[user_id] = "idle"
        await event.respond("What's next?", buttons=get_main_menu_keyboard())


def main() -> None:
    dotenv.load_dotenv()

    global client # Make client globally accessible for keyboard building

    with TelegramClient(
        "anything",
        api_id=os.getenv("TG_APP_API_ID"),
        api_hash=os.getenv("TG_APP_API_HASH"),
    ) as client:

        # --- Handle incoming text messages ---
        @client.on(events.NewMessage(incoming=True))
        async def handle_messages(event) -> None:
            user_id = event.sender_id
            message_text = event.raw_text.strip()

            current_state = user_states.get(user_id, "idle")

            if message_text == "/start":
                user_states[user_id] = "idle" # Reset state on start
                await event.respond(BOT_GREETING_MESSAGE, buttons=get_main_menu_keyboard())
                return
            
            if message_text == "/help":
                user_states[user_id] = "idle" # Reset state on help
                await event.respond(BOT_HELP_MESSAGE, parse_mode='markdown', buttons=get_main_menu_keyboard())
                return
            
            if message_text == "/color_qr": # Command to initiate colored QR
                user_states[user_id] = "choosing_color"
                await send_color_mode_prompt(event, user_id)
                return

            # State-specific handling
            if current_state == "waiting_for_text_for_color_qr":
                chosen_color = user_states.get(f"color_for_{user_id}", "black") # Retrieve chosen color
                await handle_qr_generation(event, message_text, user_id, fill_color=chosen_color)
                # State is reset inside handle_qr_generation
            elif current_state == "waiting_for_text_regular_qr":
                await handle_qr_generation(event, message_text, user_id)
                # State is reset inside handle_qr_generation
            else: # Default behavior for idle state or unrecognized command
                # If not a command, treat as regular QR request
                await handle_qr_generation(event, message_text, user_id)


        # --- Handle inline keyboard button presses (callback queries) ---
        @client.on(events.CallbackQuery)
        async def handle_buttons(event) -> None:
            user_id = event.sender_id
            data = event.data.decode('utf-8') # Callback data is bytes, decode to string

            await event.answer() # Acknowledge the callback query

            if data == "regular_qr_mode":
                user_states[user_id] = "waiting_for_text_regular_qr"
                await event.edit("Okay! Send me the text you want to convert into a *regular* QR code.", parse_mode='markdown')
            elif data == "color_qr_mode":
                user_states[user_id] = "choosing_color"
                await send_color_mode_prompt(event, user_id)
            elif data.startswith("set_color_"):
                chosen_color_hex = data.split('_', 2)[2] # Extract hex code
                user_states[f"color_for_{user_id}"] = chosen_color_hex # Store chosen color
                user_states[user_id] = "waiting_for_text_for_color_qr"
                await event.edit(f"You chose color: `{chosen_color_hex}`. Now, send me the text you want to convert into a *colored* QR code.", parse_mode='markdown')
            elif data == "back_to_main":
                user_states[user_id] = "idle"
                await event.edit(BOT_GREETING_MESSAGE, buttons=get_main_menu_keyboard())


        print("Bot started. Listening for messages and button presses...")

        client.start()
        client.run_until_disconnected()


if __name__ == "__main__":
    main()
