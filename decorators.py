def convert(argument):
    def function_decorator(_function):
        def add_tags(*args, **kwargs):
            return "<{}>{}</{}>".format(argument, _function(*args, **kwargs), argument)

        return add_tags

    return function_decorator


tag = None

while not tag:
    print('Введите тег в который необходимо обернуть строку')

    tag = str(input()).replace('<', '').replace('>', '')

print('Введите строку которую необходимо оберунть в тег')

string = str(input())


@convert(tag)
def string_return(_string):
    return _string


print(string_return(string))
