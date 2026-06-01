import os
import telebot
import anthropic

bot = telebot.TeleBot(os.environ['TELEGRAM_TOKEN'])
client = anthropic.Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])

SYSTEM_PROMPT = """Sei un assistente nutrizionale personale per Gian Luca Positano, 37 anni, Milano.

PROFILO CLINICO:
- Ipercolesterolemia familiare: LDL 205 mg/dL, Colesterolo totale 289 mg/dL
- HDL ottimo: 63 mg/dL, TG/HDL ratio 1.70
- Glicemia borderline: 105 mg/dL (pre-diabetica, da monitorare)
- Terapia: Rosuvibe (rosuvastatina) 1 cps/sera
- Si allena 2-3 volte/settimana

PIANO NUTRIZIONALE (Dott.ssa Daria Chin):
- Schema IF 16:8 o classico 3 pasti
- PRANZO: 70g pasta/riso/farro + proteina + 150-200g verdura + 20g olio EVO
- CENA: proteina + verdura + olio, pane/patate opzionale
- Frequenze: carne 3-4x/sett, pesce 3-4x/sett, uova 2-3x, legumi 1-2x
- Zero alcol, limitare grassi saturi, favorire omega-3

COME RISPONDERE:
- Sempre in italiano
- Se ti dice gli ingredienti: suggerisci ricetta con porzioni e preparazione in 3-4 passi
- Se chiede il piano del giorno: dai colazione/pranzo/cena completi
- Segnala sempre se il piatto è ottimo per LDL o glicemia
- Risposte pratiche e concise"""

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Ciao Gian Luca! 👋\n\nSono il tuo assistente nutrizionale personale.\n\nDimmi:\n🧊 Cosa hai in frigo e ti dico cosa cucinare\n📅 Chiedimi il piano del giorno\n\nEsempio: 'Ho uova e zucchine, cosa cucino per cena?'")

@bot.message_handler(func=lambda m: True)
def handle(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": message.text}]
        )
        bot.reply_to(message, response.content[0].text)
    except Exception as e:
       
        
bot.reply_to(message, "Errore, riprova tra un bot.infinity_polling(allowed_updates=[], timeout=60, long_polling_timeout=60)


