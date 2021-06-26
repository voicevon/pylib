import paho.mqtt.client as mqtt
# pylib
from singleton import Singleton
from terminal_font import TerminalFont
# import cv2

class MqttConfigableItem():
    topic = ''
    type = ''
    value = ''

    def __init__(self,topic,value,type='string'):
        self.topic = topic
        self.type = type
        self.value = value


class MqttHelper(metaclass=Singleton):
# class MqttHelper(mqtt.Client, metaclass=Singleton):

    def __init__(self):
        # super(MqttHelper, self).__init__()
        self.__is_connected = False
        self.__mqtt = None
        # self.__mqtt = mqtt
        # self.__mqtt = mqtt.Client(client_id)  # create new instance

        self.__YELLOW = TerminalFont.Color.Fore.yellow
        self.__GREEN = TerminalFont.Color.Fore.green
        self.__RED = TerminalFont.Color.Fore.red
        self.__RESET = TerminalFont.Color.Control.reset
        # self.mqtt_system_turn_on = True
        self.__on_message_callbacks = []
        self.__configable_vars = []

    def connect_to_broker(self, client_id, broker, port, uid, psw):
        self.__mqtt = mqtt.Client(client_id)  # create new instance
        self.__mqtt.username_pw_set(username=uid, password=psw)
        self.__mqtt.connect(broker, port=port)
        if self.__mqtt.is_connected():
            print(self.__GREEN + '[Info]: MQTT has connected to: %s' % broker + self.__RESET)
        else:
            print(self.__RED + '[Info]: MQTT has NOT!  connected to: %s, Is trying auto connect backgroundly.' % broker + self.__RESET)

        self.__mqtt.loop_start()
        self.__mqtt.on_message = self.__mqtt_on_message
        self.__do_debug_print_out = False
        # self.__mqtt.loop_stop()
        return self.__mqtt

    def append_on_message_callback(self, callback, do_debug_print_out=False):
        '''
        will call back on received any message.
        Says not invoved to topic. 
        '''
        self.__on_message_callbacks.append(callback)
        self.__do_debug_print_out = do_debug_print_out

    def append_configable_var(self, var):
        self.__configable_vars.append(var)

    def subscribe(self, topic, qos=0):
        self.__mqtt.subscribe(topic, qos)
    
    def __mqtt_on_message(self, client, userdata, message):
        if self.__do_debug_print_out:
            print("MQTT message received ", str(message.payload.decode("utf-8")))
            print("MQTT message topic=", message.topic)
            print("MQTT message qos=", message.qos)
            print("MQTT message retain flag=", message.retain)
        payload = str(message.payload.decode("utf-8"))

        #Solution A:
        for invoking in self.__on_message_callbacks:
            invoking(message.topic, payload)
        #Solution B:
        self.update_from_topic(self. message.topic, payload)
    def publish_init(self):
        #  traverse Json file, publish all elements to broker with default values
        pass
    
    def publish_cv_image(self, topic, cv_image, retain=True):
      # return image as mqtt message payload
        is_success, img_encode = cv2.imencode(".jpg", cv_image)
        if is_success:
            img_pub = img_encode.tobytes()
            self.__mqtt.publish(topic, img_pub, retain=retain)

    def publish_file_image(self, topic, file_name, retain=True):
        with open(file_name, 'rb') as f:
            byte_im = f.read()
        self.__mqtt.publish('sower/img/bin',byte_im )

    def publish(self, topic, value):
        self.__mqtt.publish(topic, value, qos=2, retain =True)
    
    def update_from_topic(self, topic, value, space_len=0):
        target_type_name = 'MqttConfigableItem'
        if space_len / 8 >= 3:
            return
        for var in self.__configable_vars:
            for this_item in dir(var):
                if this_item[:1] != '_':
                    attr = getattr(var,this_item)
                    type_name =type(attr).__name__
                    # space = ' ' * space_len

                    if type_name == target_type_name:
                        # For better understanding, we rename attr.
                        configable_item = attr  
                        # print ('aaaa', space + configable_item, type_name)
                        for type_value_topic in dir(configable_item):
                            # print('bbbb',type_value_topic)
                            if type_value_topic == 'topic':
                                topic_string = getattr(configable_item,type_value_topic)
                                # print('cccc', type_value_topic,topic_string)
                                if topic_string == topic:
                                    # print('ffff',type_value_topic,topic_string)
                                    if topic_string == topic:
                                        # print('RRRRRRRRRRRR', configable_item, type_value_topic, value)
                                        #TODO: type checking here.
                                        setattr(configable_item,'value',value)
                    else:
                        self.find_member(attr, target_type_name, space_len + 4)

g_mqtt = MqttHelper()

if __name__ == "__main__":
    class mqtt_config_test:
        right = MqttConfigableItem('gobot/test/right',1)
        left = MqttConfigableItem('gobot/test/right',2)
        hello = MqttConfigableItem('gobot/test/hello','Hello World')



    # put this line to your system_setup()
    g_mqtt.connect_to_broker('123456', 'voicevon.vicp.io', 1883, 'von','von1970')
    test_id =2
    if test_id ==1:
        # put this line to anywhere.
        g_mqtt.publish('test/test1/test2', 1)
    
    if test_id ==2:
        g_mqtt.append_configable_var(mqtt_config_test)
        g_mqtt.update_from_topic(mqtt_config_test,'gobot/test/hello', 'aaaabbbb')
        print (mqtt_config_test.hello.value)

