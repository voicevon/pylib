class MqttConfigableItem():
    topic = ''
    type = ''
    value = ''

    def __init__(self,topic,value,type='string'):
        self.topic = topic
        self.type = type
        self.value = value

class helper:

    def update_from_topic(self, mqtt_cofig_obj, topic, value, space_len=0):
        target_type_name = 'MqttConfigableItem'
        if space_len / 8 >= 3:
            return

        for this_item in dir(mqtt_cofig_obj):
            if this_item[:1] != '_':
                attr = getattr(mqtt_cofig_obj,this_item)
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

    '''
    Valuable function, might be useful in future.
    '''
    def find_member(self, var, target_type_name ='MqttConfigableItem', space_len=0 ):
        if space_len / 8 >= 3:
            return
        for this_item in dir(var):
            if this_item[:1] != '_':
                attr = getattr(var,this_item)
                type_name =type(attr).__name__
                space = ' ' * space_len
                # print( space + '---------------------')
                # print (space + this_item, type_name)

                if type_name == target_type_name:
                    # For better understanding, we rename attr.
                    target_obj = attr  
                    print (space + this_item, type_name)
                    for attr_name in dir(target_obj):
                        if attr_name[:1] != '_':
                            print ('     --', attr_name, getattr(target_obj, attr_name)) 
                else:
                    self.find_member(attr, target_type_name, space_len + 4)




if __name__ == '__main__':
    class mqtt_config_test:
        right = MqttConfigableItem('gobot/test/right',1)
        left = MqttConfigableItem('gobot/test/right',2)
        hello = MqttConfigableItem('gobot/test/hello','Hello World')

    hh = helper()
    # hh.find_member(mqtt_config_test)
    hh.update_from_topic(mqtt_config_test,'gobot/test/hello', 'aaaabbbb')
    print (mqtt_config_test.hello.value)