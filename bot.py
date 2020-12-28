from pymongo import MongoClient
from vkbottle import Text, Keyboard, KeyboardButtonColor, GroupTypes, GroupEventType, VKAPIError
from vkbottle.bot import Bot, Message, rules
from typing import Optional
from threading import Thread

import vkcoin
import time, datetime
import logging
import random
import tracemalloc

cluster = MongoClient("Подключение mongodb")
db = cluster["Название вашей базы данных"]
collection = db["Название вашей коллекции"]

logging.basicConfig(filename="users.log", level=logging.INFO)

bot = Bot("Токен от группы вк")
merchant = vkcoin.VKCoin(user_id="ID без ковычек", key='Ваш API KEY', token='Token от вашей страницы')

MAIN_KEYBOARD = Keyboard(one_time=False, inline=False)
MAIN_KEYBOARD.add(Text("📈 Инвестировать"), color=KeyboardButtonColor.POSITIVE)
MAIN_KEYBOARD.row()
MAIN_KEYBOARD.add(Text("👥 Рефералы"), color=KeyboardButtonColor.PRIMARY)
MAIN_KEYBOARD.add(Text("👤 Профиль"), color=KeyboardButtonColor.PRIMARY)
MAIN_KEYBOARD.row()
MAIN_KEYBOARD.add(Text("🏆 Топ"), color=KeyboardButtonColor.NEGATIVE)
MAIN_KEYBOARD.add(Text("💸 Смена ника"), color=KeyboardButtonColor.NEGATIVE)
MAIN_KEYBOARD.row()
MAIN_KEYBOARD.add(Text("🎁 Бонус"), color=KeyboardButtonColor.POSITIVE)
MAIN_KEYBOARD.add(Text("📤 Вывести"), color=KeyboardButtonColor.POSITIVE)
MAIN_KEYBOARD.row()
MAIN_KEYBOARD.add(Text("📊 База данных"), color=KeyboardButtonColor.PRIMARY)
MAIN_KEYBOARD.add(Text("🏛 Банк"), color=KeyboardButtonColor.PRIMARY)
MAIN_KEYBOARD.row()
MAIN_KEYBOARD.add(Text("🎫 Продать коины"))
MAIN_KEYBOARD.add(Text("💬 Чат"))
MAIN_KEYBOARD.row()
MAIN_KEYBOARD.add(Text("Пополнить"))
MAIN_KEYBOARD = MAIN_KEYBOARD.get_json()

TOP_KEYBOARD = Keyboard(one_time=False, inline=False)
TOP_KEYBOARD.add(Text("🏆 Топ инвесторов"), color=KeyboardButtonColor.PRIMARY)
TOP_KEYBOARD.add(Text("🏆 Топ рефералов"), color=KeyboardButtonColor.PRIMARY)


BANK_KEYBOARD = Keyboard(one_time=False, inline=False)
BANK_KEYBOARD.add(Text("💎 История VKC"), color=KeyboardButtonColor.PRIMARY)
BANK_KEYBOARD.row()
BANK_KEYBOARD.add(Text("📈 Акции 7Star"), color=KeyboardButtonColor.POSITIVE)
BANK_KEYBOARD.add(Text("🍸 Повышение дохода"), color=KeyboardButtonColor.POSITIVE)
BANK_KEYBOARD.row()
BANK_KEYBOARD.add(Text("Назад"), color=KeyboardButtonColor.NEGATIVE)


link_merchant = merchant.get_payment_url(amount=1000, payload=-345678, free_amount=True)

@bot.on.message(text=["Начать", "начать"])
async def starting(message: Message):
    user = await bot.api.users.get(message.from_id)
    firstName = user[0].first_name
    lastName = user[0].last_name
    if message.ref != None:
        if collection.count_documents({"_id": message.from_id}) == 0:
            collection.insert_one({"_id": message.from_id, "Ban": False, "Admin": "Пользователь", "Subscribe": False, "Farm": True, "Time": 86400, "FirstName": firstName, "LastName": lastName, "Withdrawal_VkCoin": 5000, "Investments_VkCoin": 0, "Stocks": 0, "Invested": 0, "Refs": 0})
            collection.update_one({"_id": message.from_id}, {"$inc": {"Investments_VkCoin": + 350000}})
            collection.update_one({"_id": int(message.ref)}, {"$inc": {"Investments_VkCoin": + 350000}})
            collection.update_one({"_id": int(message.ref)}, {"$inc": {"Refs": + 1}})
            await message.answer(f"🤑 Добро пожаловать инвестиционный проект 7Star Coin | Invest!.\n\n"
                                 f"- Инвестируй и зарабaтывай VkCoin на полном пассиве!\n"
                                 f"- Получай до 17% от пополнения своих рефералов"
                                 f"- Покупай/продавай рефералов на бирже", keyboard = MAIN_KEYBOARD)
            await bot.api.messages.send(
                        peer_id=message.ref, message=f"По вашей реферальной ссылки перешёл @id{message.from_id}", random_id=0)
        else:
            
            collection.insert_one({"_id": message.from_id, "Ban": False, "Admin": "Пользователь", "Subscribe": False, "Farm": True, "Time": 86400, "FirstName": firstName, "LastName": lastName, "Withdrawal_VkCoin": 5000, "Investments_VkCoin": 0, "Stocks": 0, "Invested": 0, "Refs": 0})
            await message.answer("Добро пожаловать!\nНажми начать, если бот не ответил попробуй еще раз.", keyboard = MAIN_KEYBOARD)
    else:
        collection.insert_one({"_id": message.from_id, "Ban": False, "Admin": "Пользователь", "Subscribe": False, "Farm": True, "Time": 86400, "FirstName": firstName, "LastName": lastName, "Withdrawal_VkCoin": 5000, "Investments_VkCoin": 0, "Stocks": 0, "Invested": 0, "Refs": 0})
        await message.answer("Добро пожаловать!\nНажми начать, если бот не ответил попробуй еще раз.", keyboard = MAIN_KEYBOARD)

@bot.on.message(text=["Назад", "НАЗАД"])
async def behind(message: Message):
    await message.answer(f"🤑 Добро пожаловать инвестиционный проект 7Star Coin | Invest!.\n\n"
                                 f"- Инвестируй и зарабaтывай VkCoin на полном пассиве!\n"
                                 f"- Получай до 17% от пополнения своих рефералов"
                                 f"- Покупай/продавай рефералов на бирже", keyboard = MAIN_KEYBOARD)

@bot.on.message(text=["👥 Рефералы", "Рефералы", "рефералы"])
async def refs(message: Message):
    _Refs_ = collection.find_one({"_id": message.from_id})["Refs"]
    await message.answer(
                        f"Твоя реферальная ссылка \n"
                        f"https://vk.me/wcg_by_pyzen?ref={message.from_id}\n "
                        f"🧸Рефералов: {_Refs_} \n"
                        f"За каждого реферала ты получишь по 350 000 коинов. \n"
                        f"Твой реферал тоже получит 350 000 коинов. \n"
                        f"С каждого пополнения реферала, ты получишь 2.7% на свой баланс для инвестиций.", keyboard = MAIN_KEYBOARD)

@bot.on.message(text=["👤 Профиль", "Профиль", "профиль"])
async def profile(message: Message):
    _first_name_ = collection.find_one({"_id": message.from_id})["FirstName"]
    _Withdrawal_VkCoin_ = collection.find_one({"_id": message.from_id})["Withdrawal_VkCoin"]
    _Investments_VkCoin_ = collection.find_one({"_id": message.from_id})["Investments_VkCoin"]
    _Invested_ = collection.find_one({"_id": message.from_id})["Invested"]
    _Stocks_ = collection.find_one({"_id": message.from_id})["Stocks"]
    _Refs_ = collection.find_one({"_id": message.from_id})["Refs"]
    await message.answer(
                        f"{_first_name_}, твой профиль: \n \n"
                        f"💰 Баланс:\n "
                        f"💴Баланс для вывода: {round(_Withdrawal_VkCoin_)} \n"
                        f"💵Баланс для инвестиций: {_Investments_VkCoin_} \n"
                        f"💰Вами инвестировано: {_Invested_} \n"
                        f"💎Акций: {_Stocks_} \n"
                        f"🧸Рефералов: {_Refs_}\n \n"
                        f"-Доход в 10 минут: {round(_Invested_ * 0.07 / 86400 * 600, 2)} VkCoin \n"
                        f"-Доход в час: {round(_Invested_ * 0.07 / 86400 * 3600, 2)} VkCoin \n"
                        f"-Доход в сутки: {round(_Invested_ * 0.07,2)} VkCoin \n"
                        f"-Доход в месяц: {round(_Invested_ * 0.07 * 30, 2)} VkCoin \n", keyboard = MAIN_KEYBOARD)


@bot.on.message(text=["🏆 Топ", "Топ", "топ"])
async def top(message: Message):
    await message.answer(f"Выбери какой топ тебе интересен", keyboard=TOP_KEYBOARD)



@bot.on.message(text=["🏆 Топ рефералов", "Топ рефералов", "топ рефералов"])
async def top_refs(message: Message):
    r =0
    #for number in range(1, 11):
        #print(number)
    await message.answer("🏆 Топ 10 рефералов")
    for i in list(collection.find().sort("Refs", -1))[:10]:
        r +=1
        await message.answer(f"{r}. @id{str(i['_id'])}({str(i['FirstName'])}) пригласил {str(i['Refs'])} рефералов!", keyboard=MAIN_KEYBOARD)


@bot.on.message(text=["🏆 Топ инвесторов", "Топ инвесторов", "топ инвесторов"])
async def top_invested(message: Message):
    p =0
    await message.answer("🏆 Топ 10 инвесторов")
    for i in list(collection.find().sort("Invested", -1))[:10]:
        p +=1
        await message.answer(f"{p}. @id{str(i['_id'])}({str(i['FirstName'])}) инвестировал {str(i['Invested'])} VkCoin!", keyboard=MAIN_KEYBOARD)

@bot.on.message(text=["💸 Смена ника", "Смена ника", "cмена ника"])
async def nick(message: Message):
    await message.answer("Что бы сменить ник, пиши !ник (новый ник) - цена 1 750 000.", keyboard=MAIN_KEYBOARD)

@bot.on.message(text=["!ник <nick_user>"])
async def nick_change(message: Message, nick_user: Optional[int] = None):
    if collection.find_one({"_id": message.from_id})["Investments_VkCoin"] >= 1750000:
        if nick is None:
            await message.answer("Введите !ник 'ТВОЙ НИК' ", keyboard = MAIN_KEYBOARD)
        else:
            collection.update_one({"_id": message.from_id}, {"$inc": {"Investments_VkCoin": - 1750000}})
            collection.update_one({"_id": message.from_id},{"$set": {"FirstName": nick_user}})
            await message.answer(f"Вы успешно сменили ник на {nick_user}. ", keyboard = MAIN_KEYBOARD)
    else:
        await message.answer("Недостаточно средств.", keyboard = MAIN_KEYBOARD)



@bot.on.message(text=["🎁 Бонус", "Бонус", "бонус"])
async def bonus(message: Message):
    await message.answer("Бонус начислится автоматический когда вы подпишетесь."
                         f"Но также ты можешь его потерять, если отпишешься.", keyboard=MAIN_KEYBOARD)

@bot.on.raw_event(GroupEventType.GROUP_JOIN, dataclass=GroupTypes.GroupJoin)
async def group_join_handler(event: GroupTypes.GroupJoin):
    try:

        # Basic API call, please notice that bot.api (or blueprint.api) is
        # not accessible in case multibot is used, API can be accessed from
        # event.ctx_api
        collection.update_one({"_id": event.object.user_id}, {"$inc": {"Investments_VkCoin": + 350000}})
        collection.update_one({"_id": event.object.user_id},{"$set": {"Subscribe": True}})
        await bot.api.messages.send(
            peer_id=event.object.user_id, message="Благодарю за подписку", random_id=0
        )
        await bot.api.messages.send(
            peer_id=event.object.user_id, message="Ты получил 350 000 коинов на свой баланс для инвестиций.", random_id=0
        )

    # Read more about exception handling in documentation
    # low-level/exception_factory/exception_factory
    except VKAPIError(901):
        pass

@bot.on.raw_event(GroupEventType.GROUP_LEAVE, dataclass=GroupTypes.GroupLeave)
async def group_group_leave_handler(event: GroupTypes.GroupLeave):
    try:

        # Basic API call, please notice that bot.api (or blueprint.api) is
        # not accessible in case multibot is used, API can be accessed from
        # event.ctx_api
        collection.update_one({"_id": event.object.user_id},{"$set": {"Subscribe": False}})
        collection.update_one({"_id": event.object.user_id}, {"$inc": {"Investments_VkCoin": - 350000}})

        await bot.api.messages.send(
            peer_id=event.object.user_id, message="Прости что не оправдали твоих надежд!", random_id=0
        )
        await bot.api.messages.send(
            peer_id=event.object.user_id, message="С вашего баланса для инвестиций списано 350 000 коинов", random_id=0
        )


    # Read more about exception handling in documentation
    # low-level/exception_factory/exception_factory
    except VKAPIError(901):
        pass

@bot.on.message(text=["📤 Вывести", "Вывести", "вывести"])
async def withdrawal(message: Message):
    await message.answer("💰 Введите сумму для вывода...", keyboard=MAIN_KEYBOARD)

@bot.on.message(text=["📊 База данных", "База данных", "база данных"])
async def bd(message: Message):
    await message.answer(
                        f"📊 Файлов с логами в базе уже 0. \n"
                        f"Ипользуйте команду лог (айди, ссылка и т.п.), что бы узнать \n"
                        f"краткую информацию о игроке, его баланс, последняя \n"
                        f"активность, доход, количество рефералов и прочее, а самое\n"
                        f"главное файл с логами его команд и сообщений в оф.беседе.\n \n"
                        f"💶 Цена за 1 раз, 1 000 000 коинов для инвестиций.", keyboard = MAIN_KEYBOARD)



@bot.on.message(text=["🏛 Банк", "Банк", "банк"])
async def bank(message: Message):
     await message.answer(f"""🍀 Раздел выгодного инвестирования средств в акции 7Star, 
                            а так же повышение процента дохода и многое другое!
                            Воспользуйся кнопками""", keyboard=BANK_KEYBOARD)


@bot.on.message(text=["💎 История VKC", "История VKC", "история VKC"])
async def history_vkc(message: Message):
    await message.answer(f"""История VKC: 5 836 \n
                        💎 За недавний период:""", keyboard=BANK_KEYBOARD)


@bot.on.message(text=["📈 Акции 7Star", "Акции 7Star", "акции 7Star"])
async def history_stocks(message: Message):
    await message.answer(f"""💰 Восхитительно!
    💳Выплата будет реализована на баланс для инвестиций. """, keyboard=BANK_KEYBOARD)


@bot.on.message(text=["🍸 Повышение дохода", "Повышение дохода", "повышение дохода"])
async def income_increase(message: Message):
    await message.answer(f"""Событие 'Чёрная Пятница' подошло к концу.""", keyboard=BANK_KEYBOARD)


@bot.on.message(text=["🎫 Продать коины", "Продать коины", "продать коины"])
async def sell_vkcoin(message: Message):
    _Withdrawal_VkCoin_ = collection.find_one({"_id": message.from_id})["Withdrawal_VkCoin"]
    await message.answer(f"💶 Скупка по 1.27 за 1 000 000 коинов\n"
                        f"Ваш баланс: {_Withdrawal_VkCoin_}\ns\n"
                        f"Кошелек: Не указан, Вам доступна коинов только на \n банковскую карту / мобильный счёт.\n"
                        f"Всего в продаже:\n"
                        f"Готовы скупить: \n"
                        f"Как пользоваться магазином: http://vk.com/@7star_coin_invest-magazin-koinov-v-7star-coin-invest", keyboard=MAIN_KEYBOARD)


@bot.on.message(text=["💬 Чат", "Чат", "чат"])
async def chat(message: Message):
    await message.answer("fff", keyboard=MAIN_KEYBOARD)


@bot.on.message(text=["Пополнить"])
async def deposit_vkcoin(message: Message):
    await message.answer(f"Ссылка для пополнения: {link_merchant}")


def oplata():
    @merchant.payment_handler(handler_type='longpoll')
    def like(data):
        usr_id = data[ 'from_id' ]
        amo = data['amount']
        if collection.find_one({"_id": usr_id})["_id"] == int(usr_id):
            print(int(usr_id ), int(amo)/1000)
            collection.update_one({"_id": int(usr_id)}, {"$inc": {"Investments_VkCoin": + int(amo)/1000}})
                      
        else:
            print(int(usr_id ),"ошибака", int(amo)/1000)
            
    merchant.run_longpoll( tx=[1] )


t = Thread(target=oplata)
t.start()

#Проверка на число и число с плавающей точкой
def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False


#merchant.run_longpoll(tx=[1], interval=0.05)
@bot.on.message(text=[f"📈Инвестировать <invest_coin>", "📈 Инвестировать", "инвестировать"])
async def investt(message: Message, invest_coin: Optional[int] = None):
    _Invested_ = collection.find_one({"_id": message.from_id})["Invested"]
    _Withdrawal_VkCoin_ = collection.find_one({"_id": message.from_id})["Withdrawal_VkCoin"]
    button_1 = collection.find_one({"_id": message.from_id})["Investments_VkCoin"]
    invest_keyboard = Keyboard(one_time=False, inline=True)
    invest_keyboard.add(Text(f"📈Инвестировать {button_1}"), color=KeyboardButtonColor.POSITIVE)  
    if collection.find_one({"_id": message.from_id})["Investments_VkCoin"] >= 1000:
        if invest_coin is None:
            await message.answer(f"💰 Вы можете инвестировать: {round(button_1)} VkCoin \n"
                                 f"💶 Из них для инвестиций: {round(button_1)}\n"
                                 f"💷 Из них для вывода: {round(_Withdrawal_VkCoin_)}  \n\n"
                                 f"Укажите сумму, которую хотите инвестировать...", keyboard = invest_keyboard)
        elif invest_coin:
            if isfloat(invest_coin) == True:
                await message.answer(f"Вы успешно инвестировали {invest_coin}\n"
                                     f"-Доход в 10 минут: {round(_Invested_ * 0.07 / 86400 * 600, 2)} VkCoin \n"
                                     f"-Доход в час: {round(_Invested_ * 0.07 / 86400 * 3600, 2)} VkCoin \n"
                                     f"-Доход в сутки: {round(_Invested_ * 0.07,2)} VkCoin \n"
                                     f"-Доход в месяц: {round(_Invested_ * 0.07 * 30, 2)} VkCoin \n", keyboard = MAIN_KEYBOARD)
                collection.update_one({"_id": message.from_id}, {"$inc": {"Invested": + int(invest_coin)}})
                collection.update_one({"_id": message.from_id}, {"$inc": {"Investments_VkCoin": - int(invest_coin)}})
            elif invest_coin.isdigit() == False:
                await message.answer(f"Упс.Вы не ввели число.", keyboard = MAIN_KEYBOARD)
    elif collection.find_one({"_id": message.from_id})["Investments_VkCoin"] < 1000:
        await message.answer("Минимальная сумма инвестиции 1 000 коинов.")
  
    def sleeping(num):
        time.sleep(num)

    def invest():
        while True:
            _Invested_ = collection.find_one({"_id": message.from_id})["Invested"]
            _Withdrawal_VkCoin_ = collection.find_one({"_id": message.from_id})["Withdrawal_VkCoin"]
    
            if collection.find_one({"Farm": True})["Time"] >= 1:
                if collection.find_one({"Farm": True})["Time"] <= 86400:
        #timeA = timeB

                    for i in collection.find_one({"_id": message.from_id}):
                        sleeping(1)
                        collection.update_many({"_id": message.from_id}, {"$inc": {"Time": - 1}})
                        collection.update_many({"_id": message.from_id}, {"$inc": {"Withdrawal_VkCoin": + round(_Invested_ * 0.07 / 86400 , 2) }})
    
            elif collection.find_one({"_id": message.from_id})["Time"] <= 0:
        #timeA = 0
                for i in collection.find_one({"_id": message.from_id}):
                    collection.update_many({"_id": message.from_id},{"$set": {"Time": 86400}})
 
    t1 = Thread(target=invest)
    t1.start()

bot.run_forever()
