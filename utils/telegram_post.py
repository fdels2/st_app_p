import requests
import os


def telegram_bot_sendtext(bot_message):
    """Send a text message via Telegram bot.

    This function sends a text message using a Telegram bot. The bot token and chat ID
    are retrieved from environment variables. The message is sent using the Telegram
    Bot API.

    Args:
        bot_message (str): The message to be sent.

    Returns:
        dict: The JSON response from the Telegram API.

    Raises:
        None
    """
    bot_token = os.environ.get('ST_BOT_TOKEN')
    bot_chatID = os.environ.get('ST_BOT_CHATID')
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()
