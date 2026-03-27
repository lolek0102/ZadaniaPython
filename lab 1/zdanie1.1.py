import functools

def show_list_length(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"Długość listy: {len(result)}")
        return result
    return wrapper

@show_list_length
def get_list():
    return [1, 2, 3, 4, 5]

print(get_list())