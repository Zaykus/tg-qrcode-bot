# Telegram QR Code Bot

A feature-rich Telegram bot designed to generate QR codes from any text input. This bot makes it simple and efficient to create customized QR codes directly within Telegram.

---

## Features

* **QR Code Generation:** Quickly converts text messages into QR code images.
* **Customizable QR Colors:** Users can choose specific colors (foreground) for their QR codes using an interactive button menu.
* **Interactive Menu System:** Provides a user-friendly button-based menu for selecting QR code options.
* **Comprehensive Help:** A dedicated `/help` command offers detailed usage instructions for all features.
* **Secure Configuration:** Utilizes environment variables for storing sensitive credentials.
* **Modular Design:** Easy to set up and run locally.

---

## Setup and Running

Follow the steps below to set up and run the bot on your local machine.

### 1. Clone the Repository

Start by cloning this repository using Git. If Git is not installed, you can download the files manually and extract them.

```bash
# Clone the repository using Git
git clone https://github.com/your-username/tg-qrcode-bot.git
cd tg-qrcode-bot
```

---

### 2. Create a Python Virtual Environment

To avoid dependency conflicts, create a virtual environment for the project.

```bash
python3 -m venv venv
```

---

### 3. Activate the Virtual Environment

Activate the virtual environment depending on your operating system:

  * **Linux/macOS:**
    ```bash
    source venv/bin/activate
    ```
  * **Windows (Command Prompt):**
    ```cmd
    venv\Scripts\activate.bat
    ```
  * **Windows (PowerShell):**
    ```powershell
    .\venv\Scripts\Activate.ps1
    ```

Once activated, the terminal prompt will display `(venv)` to indicate that the virtual environment is active.

---

### 4. Install Dependencies

With the virtual environment activated, install the required Python libraries using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

This will install the following dependencies:

  * `python-dotenv`: For managing environment variables.
  * `qrcode`: For generating QR codes.
  * `telethon`: For interfacing with Telegram.
  * `Pillow`: For image manipulation.

---

### 5. Obtain Telegram API Credentials

You need three key credentials to interact with the Telegram API:

#### Telegram Bot Token

1. Open Telegram and search for `@BotFather`.
2. Start a chat and send the command `/newbot`.
3. Follow the prompts to choose a name and username for your bot.
4. `@BotFather` will provide a **Bot Token**. Save this token as `BOT_TOKEN`.

#### Telegram API ID and API Hash

1. Go to [my.telegram.org](https://my.telegram.org/) in your browser.
2. Log in using your Telegram phone number.
3. Navigate to "API development tools."
4. Fill in the "App title" and "Short name" fields (e.g., "My QR Bot", "qrbot").
5. Click "Create application."
6. Copy the **API ID** and **API Hash**. Save these as `TG_APP_API_ID` and `TG_APP_API_HASH`.

---

### 6. Configure Environment Variables

Create a file named `.env` in the root directory of the project. Add the credentials obtained in the previous step:

```dotenv
BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN_HERE"
TG_APP_API_ID="YOUR_TELEGRAM_API_ID_HERE"
TG_APP_API_HASH="YOUR_TELEGRAM_API_HASH_HERE"
```

#### Guidelines:

  * Replace placeholders with actual values.
  * Ensure values are enclosed in double quotes (`"`).
  * Avoid spaces around the `=` sign.

---

### 7. Run the Bot

Activate the virtual environment and run the bot using the following command:

```bash
python main.py
```

If the bot starts successfully, you will see "Bot started. Listening for messages and button presses..." in the terminal. The bot is now running and ready to respond.

---

## How to Use the Bot

1. **Start a Chat:** Open Telegram and search for your bot's username (set with `@BotFather`). Send the `/start` command to initiate a conversation and display the main menu.
2. **Interactive Menu:** The bot will present a menu with options to "Generate Regular QR" or "Generate Colored QR".
3. **Generate Regular QR Code:**
      * Click "Generate Regular QR" from the menu.
      * Send any text message to the bot. It will reply with a standard black and white QR code.
4. **Generate Colored QR Code:**
      * Click "Generate Colored QR" from the menu, or send the `/color_qr` command.
      * The bot will present a new menu with various color options (e.g., Red, Blue, Green).
      * Click your desired color.
      * Send the text you want to encode in the QR code. The bot will reply with a QR code in your chosen color.
5. **Get Help:** Send the `/help` command to see a detailed explanation of all bot features and usage.

---

## Quick Troubleshooting

### 1. Missing Dependencies (`ModuleNotFoundError`)

  * **Cause:** Required Python libraries are not installed.
  * **Solution:** Ensure the virtual environment is activated (`(venv)` in your prompt) and run:
    ```bash
    pip install -r requirements.txt
    ```

### 2. Missing or Incorrect API ID/Hash (`ValueError`)

  * **Cause:** Environment variables are not set correctly.
  * **Solution:** Double-check the `.env` file to ensure `TG_APP_API_ID` and `TG_APP_API_HASH` are properly configured.

### 3. Bot Not Responding in Telegram

  * **Cause:** The bot script is not running, or the `BOT_TOKEN` is incorrect.
  * **Solution:**
      * Check if `python main.py` is running in your terminal.
      * Verify `BOT_TOKEN` in the `.env` file matches the token provided by `@BotFather`.

### 4. Corrupted QR Code Images

  * **Cause:** Issues with the `Pillow` library or unsupported text characters.
  * **Solution:**
      * Ensure `Pillow` is installed:
        ```bash
        pip install Pillow
        ```
      * Test with simpler text inputs.

---

## Contribution

Contributions are welcome! You can fork this repository, submit issues, or create pull requests to improve the project.

---

## License

This project is licensed under the [MIT License](LICENSE.md).
