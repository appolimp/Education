def greg(patern):
    print('start greg')
    try:
        while True:
            line = yield
            if patern in line:
                print(line)
    except GeneratorExit:
        print('stop greg')
    except RuntimeError as err:
        print(err.args)


g = greg('python')
g.send(None)
g.send('golang is better?')
g.send('python is simple!')
g.throw(RuntimeError, ('1111', ))
# g.close()
