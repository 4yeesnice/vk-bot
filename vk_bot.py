from price import price
from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text, template_gen, TemplateElement
from config import token
import asyncio
bot = Bot(token="c8609dc97fbce1d1543d76c138d715942d305af4d873d451650af8ab460a1a961427330e12adf65a212bf")

class User:
    total_price = 0
    def __init__(self, id, total_price,korzina): ''' Класс Юзера, который пишет сообществу. Создан для того, чтобы не путать пользователей когда их будет больше чем 1'''
        self.id = id
        self.total_price = total_price
        self.korzina = korzina

keyboard_vk = Keyboard(one_time=False)
keyboard_vk.add(Text("Корзина"), color=KeyboardButtonColor.POSITIVE)
keyboard_vk = keyboard_vk.get_json()

manager_button = Keyboard(one_time=False).add(Text("Связаться с менеджером"), color=KeyboardButtonColor.PRIMARY).get_json()

oplata_button = Keyboard(one_time=False).add(Text("Оплатить"), color=KeyboardButtonColor.SECONDARY).get_json()

users = []


@bot.on.private_message()
async def printer(message: Message):
    print(message.text, message.attachments[0].market.title) 
    '''При взаимодействии с товаром из сообщества, можно отправить в лс товар. Конкретно здесь он фиксирует,
    под каким названием этот товар'''


@bot.on.private_message(text="start")
async def handler(message: Message):
'''
Если юзер написал start, то начинается диалог
'''

    user_info = await bot.api.users.get(message.from_id)
    users.append(User(user_info[0].id, 0, None))
    # print(users[0].id)
    carousel = template_gen(
        TemplateElement(
            "Реферат",
            "Простой Реферат на 150 стр. \nЦена Реферата : 1500 р.",
            buttons = Keyboard().add(Text("Купить Реферат"), color=KeyboardButtonColor.POSITIVE).get_json()
        )
    )
    await message.answer("Привет, {}. Здесь ты можешь заказать работу, просто выбери что тебе нужно".format(user_info[0].first_name), template=carousel)
    await message.answer(keyboard=keyboard_vk)




@bot.on.private_message(text="Купить Реферат")
async def id(message_vk: Message):
    user_id = await bot.api.users.get(message_vk.from_id)
    user_id = user_id[0].id
    korzina = []
    if users == []:
        await message_vk.answer("Откуда ты знаешь что писать?:)")
    else:
        for user in users:
            if user.id == user_id:
                user.total_price += price.get(message_vk.text[7:])
                korzina.append(message_vk.text[7:])
                user.korzina = korzina
                print(user.korzina)







@bot.on.private_message(text="Корзина")
async def balance(message_vk: Message):
    user_id = await bot.api.users.get(message_vk.from_id)
    user_id = user_id[0].id
    await message_vk.answer("Ваша корзина : ")
    for user in users:
        if user.id == user_id:
            
            for items in user.korzina:
                await message_vk.answer("{}".format(items))

            await message_vk.answer("Итого : {} р.".format(user.total_price))
'''
Корзина. Выводит предметы и окончательную цену. Есть несколько циклов, чтобы перебирать юзеров и их "личные" списки покупок
'''






bot.run_forever()
