import time
from datetime import datetime

def log_to_file(filename):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            
            result = func(*args, **kwargs)
            
            end = time.time()
            duration = end - start
            
            with open(filename, "a") as f:
                f.write(f"{func.__name__} | {datetime.now()} | {duration:.4f}s\n")
            
            return result
        return wrapper
    return decorator

@log_to_file("log.txt")
def test():
    time.sleep(1)
    print("Działa!")

test()