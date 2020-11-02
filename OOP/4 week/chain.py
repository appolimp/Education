class SomeObject:
    def __init__(self):
        self.integer_field = 0
        self.float_field = 0.0
        self.string_field = ""


class EventGet:
    def __init__(self, data):
        self.req = 'GET'
        self.data = data


class EventSet:
    def __init__(self, data):
        self.req = 'SET'
        self.data = data


class NullHandler:
    def __init__(self, successor=None):
        self.__successor = successor

    def handle(self, obj, req):
        if self.__successor is not None:
            return self.__successor.handle(obj, req)


class IntHandler(NullHandler):
    def handle(self, obj, req):
        if req.req == 'GET' and req.data == int:
            return obj.integer_field
        elif req.req == 'SET' and type(req.data) == int:
            obj.integer_field = req.data
        else:
            return super().handle(obj, req)


class FloatHandler(NullHandler):
    def handle(self, obj, req):
        if req.req == 'GET' and req.data == float:
            return obj.float_field
        elif req.req == 'SET' and type(req.data) == float:
            obj.float_field = req.data
        else:
            return super().handle(obj, req)


class StrHandler(NullHandler):
    def handle(self, obj, req):
        if req.req == 'GET' and req.data == str:
            return obj.string_field
        elif req.req == 'SET' and type(req.data) == str:
            obj.string_field = req.data
        else:
            return super().handle(obj, req)


if __name__ == '__main__':
    obj = SomeObject()
    obj.integer_field = 42
    obj.float_field = 3.14
    obj.string_field = "some text"

    chain = IntHandler(FloatHandler(StrHandler(NullHandler())))

    print(chain.handle(obj, EventGet(int)))
    print(chain.handle(obj, EventGet(float)))
    print(chain.handle(obj, EventGet(str)))

    print()

    chain.handle(obj, EventSet(100))
    chain.handle(obj, EventSet(0.5))
    chain.handle(obj, EventSet('new text'))

    print(chain.handle(obj, EventGet(int)))
    print(chain.handle(obj, EventGet(float)))
    print(chain.handle(obj, EventGet(str)))

