
# from global_const import app_config
# import sys

import paho.mqtt.client as mqtt
# pylib
from singleton import Singleton
from terminal_font_color import TerminalFontColor



class MqttHelper(metaclass=Singleton):
# class MqttHelper(mqtt.Client, metaclass=Singleton):

    def __init__(self):
        # super(MqttHelper, self).__init__()
        self.__is_connected = False
        self.__mqtt = mqtt
        self.__mqtt = mqtt.Client("sower-2039-1004")  # create new instance

        self.__YELLOW = TerminalFontColor.Fore.yellow
        self.__GREEN = TerminalFontColor.Fore.green
        self.__RED = TerminalFontColor.Fore.red
        self.__RESET = TerminalFontColor.Control.reset
        self.mqtt_system_turn_on = True
        self.__invoke_eye = None
        self.__on_message_callbacks = []

    def connect_broker(self, broker, port, uid, psw):
        # if broker == '':
        #     broker = app_config.server.mqtt.broker_addr
        # if uid == '':
        #     uid = app_config.server.mqtt.username
        # if psw == '':
        #     psw = app_config.server.mqtt.password
        # if port == 0:
        #     port = app_config.server.mqtt.port

        self.__mqtt.username_pw_set(username=uid, password=psw)
        self.__mqtt.connect(broker, port=port)
        if self.__mqtt.is_connected():
            print(self.__GREEN + '[Info]: MQTT has connected to: %s' % broker + self.__RESET)
        else:
            print(self.__RED + '[Info]: MQTT has NOT!  connected to: %s' % broker + self.__RESET)

        self.__mqtt.loop_start()
        self.__mqtt.on_message = self.__mqtt_on_message
        # self.__mqtt.loop_stop()
        return self.__mqtt

    def append_on_message_callback(self, callback):
            self.__on_message_callbacks.append(callback)
    
    def subscribe(self, topic, qos=0):
        self.__mqtt.subscribe(topic, qos)
    
    def __mqtt_on_message(self, client, userdata, message, do_debug_print_out=False):
        if do_debug_print_out:
            print("message received ", str(message.payload.decode("utf-8")))
            print("message topic=", message.topic)
            print("message qos=", message.qos)
            print("message retain flag=", message.retain)
        payload = str(message.payload.decode("utf-8"))
        for invoking in self.__on_message_callbacks:
            invoking(message.topic, payload)

    def publish_init(self):
        #  traverse app_config, publish all elements to broker with default values
        pass
    
    def publish_cv_image(self, flag):
      # return image as mqtt message payload
        # f= open("Python/test.jpg")
        # content = f.read()
        # byte_im = bytearray(content)



        # im = cv2.imread('test.jpg')
        # im_resize = cv2.resize(im, (500, 500))
        # is_success, im_buf_arr = cv2.imencode(".jpg", im_resize)
        # byte_im = im_buf_arr.tobytes()
        filename = 'test.jpg'
        if flag:
            filename = 'star.png'

        with open(filename, 'rb') as f:
            byte_im = f.read()
        self.__mqtt.publish('sower/img/bin',byte_im )
    
    def publish_float(self, topic, value):
        self.__mqtt.publish(topic, value, qos=2, retain =True)


g_mqtt = MqttHelper()

if __name__ == "__main__":
    g_mqtt.connect_broker('voicevon.vicp.io', 1883, 'von','von1970')
    g_mqtt.publish_float('sower/eye/outside/height', 1)


