from channels.generic.websocket import WebsocketConsumer
import json

from .bitrix_chat import send_message_to_bitrix24


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.user = self.scope['user']
        self.send(text_data=json.dumps({
            'message': f'Добро пожаловать, {self.user.username}! Пожалуйста, выберите цель Вашего обращения:',
            'options': [
                '1. Хочу сделать заказ',
                '2. Консультация эксперта по обустройству дома',
                '3. Обращение по текущему заказу',
                '4. Сервисная поддержка или гарантийное обслуживание',
                '5. Соединение со специалистом'
            ]
        }))

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        if message == '1':
            if self.user.is_authenticated:
                send_message_to_bitrix24('Заказ')
                self.send(text_data=json.dumps({
                    'message': 'Заказ успешно оформлен!'
                }))
            else:
                self.send(text_data=json.dumps({
                    'message': 'Для оформления заказа, пожалуйста, предоставьте следующую информацию...'
                }))
        elif message == '2':
            self.send(text_data=json.dumps({
                'message': 'Для консультации эксперта, пожалуйста, выберите дату и время...'
            }))
        elif message == '3':
            self.send(text_data=json.dumps({
                'message': 'Для обращения по текущему заказу, пожалуйста, выберите номер заказа...'
            }))
        elif message == '4':
            self.send(text_data=json.dumps({
                'message': 'Для сервисной поддержки или гарантийного обслуживания, пожалуйста, введите номер заказа...'
            }))
        elif message == '5':
            self.send(text_data=json.dumps({
                'message': 'Для соединения со специалистом, пожалуйста, выберите специалиста...'
            }))
        else:
            self.send(text_data=json.dumps({
                'message': 'К сожалению, я не могу обработать Ваш запрос. Пожалуйста, выберите другой вариант.'
            }))
