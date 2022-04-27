from pyexpat.errors import messages
from tkinter import Button
from turtle import color
from xml.dom.minidom import Element
from numpy import positive
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardButton, VkKeyboardColor
import bs4
from vktools import Keyboard, ButtonColor, Text, Carousel, Element
from bs4 import BeautifulSoup
token_vk = "c8609dc97fbce1d1543d76c138d715942d305af4d873d451650af8ab460a1a961427330e12adf65a212bf"
vk_session = vk_api.VkApi(token=token_vk)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
# class Vkbot:
#     def __init__(self, id):
#         print("created new bot object")
#         self._USER_ID = id
#         self._USERNAME = self._get_user_name_from_vk_id(id)
#         self.COMMANDS = ["HI", "WEATHER", "TIME", "BYE"]
    
    
#     def _get_user_name_from_vk_id(self, id):
#         request = request.get("https://vk.com/id"+str(id))
#         bs = bs4.BeautifulSoup(request.text(), "html.parser")
        
#         user_name = self._clean_all_tag_from_str(bs.findAll("title")[0])
        
#         return user_name.split()[0]

#     def new_message(self, message):

#     # Привет
#         if message.upper() == self._COMMANDS[0]:
#             return f"Привет-привет, {self._USERNAME}!"
        
#         # Погода
#         elif message.upper() == self._COMMANDS[1]:
#             return self._get_weather()
        
#         # Время
#         elif message.upper() == self._COMMANDS[2]:
#             return self._get_time()
        
#         # Пока
#         elif message.upper() == self._COMMANDS[3]:
#             return f"Пока-пока, {self._USERNAME}!"
        
#         else:
#             return "Не понимаю о чем вы..."
# def sender(text, id, Keyboard=None):
#     payload = {"user_id" : id, "message": text, "random_id" : 0 }
#     if Keyboard == None:
#         pass
#     else:
#         payload["keyboard"] = Keyboard.get_keyboard()
#     vk_session.method("messages.send", payload )


price = {
    "1": 2500,
    "2": 3000,
    "3": 4000,
    "4": 5000

}
total_price = 0

for event in longpoll.listen():
    def sender(text, id, keyboard=None, carousel=None):
        # payload = {"user_id" : id, "message": text, "random_id" : 0 }
        # if Keyboard != None:
        #     payload["keyboard"] = Keyboard.get_keyboard()
        # elif carousel != None:
        #     payload["carousel"] = carousel.add_carousel()
        # else:
        #     pass
        # vk_session.method("messages.send", payload )
    

        values = {
            "user_id": id,
            "message": text,
            "random_id": 0
        }

        if carousel is not None:
            values["template"] = carousel.add_carousel()
        if keyboard != None:
            values["keyboard"] = keyboard.get_keyboard()
        vk_session.method("messages.send", values)
    
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            msg = event.text.lower()
            print(msg, total_price)
            id = event.user_id
            
            if msg == "start" or "привет":
                
                Keyboard = VkKeyboard(one_time=True)
                Keyboard.add_button("Вперед", VkKeyboardColor.POSITIVE)
                
                sender("Тебя приветствует bot-helper, и я так понимаю у тебя проблема с учебой, да?\nЕсли хочешь просмотреть мои товары, нажми на кнопку 'Вперед'",id,Keyboard)
            

            if msg[::-1][0].isdigit() and "т"==msg[0]:
                
                total_price += price.get(msg[::-1][0])
            
            if msg == "вперед":
                carousel = Carousel(
                    [
                        Element(
                            "Товар 1",
                            "Description 1",
                                None,
                            "https://vk.com/public212630555", # redirect url, if user click on element
                            [Text("Товар 1", ButtonColor.POSITIVE)]
                        ),
                        Element(
                            "Товар 2",
                            "Description 2",
                            None,
                            "https://vk.com/public212630555", # redirect url, if user click on element
                            [Text("Товар 2", ButtonColor.PRIMARY)]
                        ),
                        Element(
                            "Товар 3",
                            "Description 3",
                            None,
                            "https://vk.com/public212630555", # redirect url, if user click on element
                            [Text("Товар 2", ButtonColor.PRIMARY)]
                        ),
                    ]
                )
                caroseul_2 = Carousel(
                    [Element(
                            "Товар 4",
                            "Description 4",
                            None,
                            "https://vk.com/public212630555", # redirect url, if user click on element
                            [Text("Товар 2", ButtonColor.PRIMARY)]
                        ),
                        Element(
                            "Товар 5",
                            "Description 5",
                            None,
                            "https://vk.com/public212630555", # redirect url, if user click on element
                            [Text("Товар 2", ButtonColor.PRIMARY)]
                        ),
                    ]
                )
                btns_names = ["Проверить баланс", "Вернуться в главное меню","Остаться"]
                btns_colors = [VkKeyboardColor.PRIMARY,VkKeyboardColor.NEGATIVE, VkKeyboardColor.SECONDARY]
                keyboard = VkKeyboard()
                for buttons, color in zip(btns_names, btns_colors):
                    keyboard.add_button(buttons,color)

                sender("А вот и мой товар, выбирай что тебе требуется и если хочешь проверить баланс просто нажми на кнопку 'Проверить баланс'",id,carousel=carousel)
                sender("None", id, carousel=caroseul_2)
                sender("А вот и кнопки, с помощью которых ты можешь проверить баланс", id, keyboard, None)
                sender("А, если что ты можешь убрать тот товар, который тебе не нужен, просто написав 'Убери Товар (номер товара)", id)
            
            
            
            
            
            
            
            
            
            # if msg == "вперед":
                
            #     Keyboard = VkKeyboard()
            #     btns_names = ["Проверить баланс", "Вернуться в главное меню","Остаться"]
            #     btns_colors = [VkKeyboardColor.PRIMARY,VkKeyboardColor.NEGATIVE, VkKeyboardColor.SECONDARY]
                
            #     for buttons, color in zip(btns_names, btns_colors):
            #         Keyboard.add_button(buttons,color)
                
            #     sender("Вас понял", id , Keyboard)
            if "убери" in msg:
                sender("Хорошо, убираю товар под номером {}".format(msg[::-1][0]), id)
                total_price -= price.get(msg[::-1][0])
            
            if msg == "проверить баланс":
                
                sender("Ваш баланс : {}".format(total_price), id)
        