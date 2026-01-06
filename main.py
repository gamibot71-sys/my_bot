import telebot
from telebot import types

API_TOKEN = ‘7832517563:AAGCHOU1krEDzOSAg_UGEijVWaUEbPcbges’
bot = telebot.TeleBot(API_TOKEN)

# Буюртма маълумотларини вақтинча сақлаш учун луғат
user_data = {}

@bot.message_handler(commands=[‘start’])
def start(message):
    bot.reply_to(message, “Assalomu alaykum! Buyurtma berish uchun ismingizni kiriting:”)
    bot.register_next_step_handler(message, get_name) #

def get_name(message):
    user_data[message.chat.id] = {‘name’: message.text}
    
    # Telefon raqamini yuborish tugmasi
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = types.KeyboardButton(“Telefon raqamni yuborish”, request_contact=True) #
    markup.add(button)
    
    bot.send_message(message.chat.id, f”Raxmat, {message.text}. Endi telefon raqamingizni yuboring:”, reply_markup=markup)
    bot.register_next_step_handler(message, get_phone)
def get_phone(message):
    if message.contact:
        user_data[message.chat.id][‘phone’] = message.contact.phone_number
    else:
        user_data[message.chat.id][‘phone’] = message.text
        
    bot.send_message(message.chat.id, “Nima buyurtma qilmoqchisiz? (Mahsulot nomi va miqdori):”, reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, get_order)

def get_order(message):
    user_data[message.chat.id][‘order’] = message.text
    
    # Yakuniy ma’lumotlarni yig’ish
    data = user_data[message.chat.id]
    order_summary = (f”✅ Yangi buyurtma!\n\n"
  f”👤 Mijoz: {data[‘name’]}\n”
                     f”📞 Tel: {data[‘phone’]}\n”
                     f”📦 Buyurtma: {data[‘order’]}”)
    
    bot.send_message(message.chat.id, “Raxmat! Buyurtmangiz qabul qilindi. Tez orada bog’lanamiz.”)
    
    # Buyurtmani o’zingizga (admin’ga) yuborish
    # Bu yerga o’z ID raqamingizni yozishingiz mumkin
    bot.send_message(message.chat.id, order_summary) 
    print(order_summary) #

bot.infinity_polling()
  
