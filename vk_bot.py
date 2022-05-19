
import pandas as pd
from price import price
from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text, template_gen, TemplateElement
from config import token
import asyncio
bot = Bot(token="c8609dc97fbce1d1543d76c138d715942d305af4d873d451650af8ab460a1a961427330e12adf65a212bf")


class User:
    total_price = 0
    def __init__(self, id, total_price, name, surname):
        self.korzina = {}
        self.id = id
        self.total_price = total_price
        self.name = name
        self.surname = surname

    def add_bag(self, tovar, quantity):
        if tovar in self.korzina.keys():
            self.korzina[tovar] += 1
        else:
            self.korzina[tovar] = quantity

keyboard_vk = Keyboard(one_time=True)
keyboard_vk.add(Text("Магазин"), color=KeyboardButtonColor.POSITIVE)
keyboard_vk = keyboard_vk.get_json()

manager_button = Keyboard(one_time=False).add(Text("Связаться с менеджером"), color=KeyboardButtonColor.PRIMARY).get_json()

oplata_button = Keyboard(one_time=False).add(Text("Оплатить"), color=KeyboardButtonColor.SECONDARY).get_json()

korzina_button = Keyboard(one_time=True).add(Text("Корзина"), color=KeyboardButtonColor.PRIMARY).get_json()

users = []





@bot.on.private_message(text="start")
async def handler(message: Message):


    user_info = await bot.api.users.get(message.from_id)
    users.append(User(user_info[0].id, 0, user_info[0].first_name, user_info[0].last_name))

    
    await message.answer("Привет, {}👋🏻. Здесь ты можешь заказать работу, просто выбери что тебе нужно\nНапиши Магазин, чтобы посмотреть наши товары.\nКорзина, чтобы просмотреть свои покупки😉".format(user_info[0].first_name), keyboard=keyboard_vk)
    for user in users:
        if user.id == user_info[0].id:
            df = pd.DataFrame({"Name": [user.name],
                                            "Surname": [user.surname],
                                            "Link":["https://vk.com/id{}".format(user.id)],
                                            "Korzina": [0],
                                            "Quantity":[0]
                                        })

            df.to_excel('./vk_bot.xlsx')
@bot.on.private_message(text="Здравствуйте!\nМеня заинтересовал этот товар.")
async def printer(message: Message):

    user_info = await bot.api.users.get(message.from_id)
    user_info_id = user_info[0].id
    await message.answer("Привет, {}👋🏻. Добавить товар в корзину? Тогда напиши название товара".format(user_info[0].first_name))
    if users == []:
        users.append(User(user_info_id, 0, user_info[0].first_name, user_info[0].last_name))
    else:
        for user in users:
            if user_info_id != user.id:
                users.append(User(user_info_id, 0, user_info[0].first_name, user_info[0].last_name))


@bot.on.private_message(text="Магазин")
async def shop(message: Message):
    user_id = await bot.api.users.get(message.from_id)
    user_id = user_id[0].id
    for user in users:
        if user.id == user_id:
            carousel = template_gen(
            TemplateElement(
            "Реферат",
            "Простой Реферат на 150 стр. \nЦена : 1500 р.",
            buttons = Keyboard().add(Text("Купить Реферат"), color=KeyboardButtonColor.POSITIVE).get_json()
            ),
            TemplateElement(
                "Дипломная",
                "Простая Дипломная на 8 стр. \nЦена : 2000 р.",
                buttons = Keyboard().add(Text("Купить Дипломную"), color=KeyboardButtonColor.POSITIVE).get_json()
            ),
            TemplateElement(
                "Дом. задание",
                "Дом задание на 15 стр. \nЦена : 500 р.",
                buttons = Keyboard().add(Text("Купить Дом. задание"), color=KeyboardButtonColor.POSITIVE).get_json()
            )
            )   
            await message.answer("Магазин: ",template=carousel)

@bot.on.private_message(text="Реферат")
async def add(message: Message):
    user_id = await bot.api.users.get(message.from_id)
    user_id = user_id[0].id
    for user in users:
            if user.id == user_id:
                await message.answer("Добавляю Реферат в корзину. Чтобы просмотреть её, напишите - Корзина или тыкните по кнопке", keyboard=korzina_button)
                user.total_price += price.get(message.text)
                user.add_bag(message.text, 1)


@bot.on.chat_message(text="Заказы")
async def add(message: Message):
    await message.answer()



@bot.on.private_message(text="Купить Реферат")
async def id(message_vk: Message):
    user_id = await bot.api.users.get(message_vk.from_id)
    user_id = user_id[0].id
    if users == []:
        await message_vk.answer("Откуда ты знаешь что писать?:)")
    else:
        for user in users:
            if user.id == user_id:
                user.total_price += price.get(message_vk.text[7:])
                user.add_bag(message_vk.text[7:], 1)
        
@bot.on.private_message(text="Купить Дипломную")
async def id(message_vk: Message):
    user_id = await bot.api.users.get(message_vk.from_id)
    user_id = user_id[0].id
    if users == []:
        await message_vk.answer("Откуда ты знаешь что писать?:)")
    else:
        for user in users:
            if user.id == user_id:
                user.total_price += price.get(message_vk.text[7:])
                tovar_name = message_vk.text[7:]
                user.add_bag(tovar_name[:len(tovar_name)-3], 1)

                





@bot.on.private_message(text="Корзина")
async def balance(message_vk: Message):
    user_id = await bot.api.users.get(message_vk.from_id)
    user_id = user_id[0].id
    await message_vk.answer("Ваша корзина : ")
    for user in users:
        if user.id == user_id:
            
            for items in user.korzina:
                await message_vk.answer("{0} - {1} шт.".format(items, user.korzina[items]))

            await message_vk.answer("Итого : {} р.".format(user.total_price))





@bot.on.private_message()
async def answer(message:Message):
    await message.answer("Простите, я не понимаю что вы написали. Напишите start для начала общения с ботом.\nМагазин, чтобы просмотреть товары.\nКорзина, чтобы посмотреть купленные товары.")


bot.run_forever()