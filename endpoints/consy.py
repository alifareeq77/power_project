from channels.generic.websocket import WebsocketConsumer


class ESP32WebsocketConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        print(f'esp disconnected with st code :{close_code}')

    def receive(self, text_data):
        print(f'Received message: {text_data}')

    def send_response(self, response_data):
        self.send(response_data)
