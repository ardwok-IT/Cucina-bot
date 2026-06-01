import os
import telebot
import anthropic

bot = telebot.TeleBot(os.environ['TELEGRAM_TOKEN'])
client = anthropic.Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])

SYSTEM_PROMPT = """Sei un assistente nutrizionale personale per Gian Luca Positano, 37 anni, Milano.
LDL 205, colesterolo 289, HDL 63, glicemia 105 borderline, statina in corso.
Piano Dott.ssa Chin: IF 16:8 o 3 pasti. Pranzo: 70g pasta + proteina + verdura + olio EVO.
Cena: proteina + verdura + olio. Zero alcol, limitare grassi saturi, favorire omega-3.
Rispondi sempre in italiano, in modo pratico e conciso."""

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Ciao Gian Luca! Dimmi cosa hai in frigo e ti dico cosa cucinare!")

@bot.message_handler(func=lambda m: True)
def handle(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": message.text}]
        )
        bot.reply_to(message, response.content[0].text)
    except Exception as e:
        bot.reply_to(message, f"Errore: {str(e)}")

bot.infinity_polling()
