def testing(func):
    def wrapper(*args, **kwargs):
        if 'id' in args:
            return True
        else:
            return False
    return wrapper

@testing
def my_app(id):
    return id


print(my_app(id=2))

