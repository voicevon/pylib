class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Person(metaclass=Singleton):
    def __init__(self, name):
        self.name = name

    def rename(self, name):
        self.name = name


if __name__ == "__main__":
    me = Person('me')
    print (me.name)

    you = Person('you')
    print(you.name)
    print(me.name)
    
    you.rename('who')
    print(you.name)
    print(me.name)



