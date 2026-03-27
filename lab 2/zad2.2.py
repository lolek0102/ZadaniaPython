import threading
import queue
import time

kolejka = queue.Queue()
n = 20

parzyste_wyniki = []
nieparzyste_wyniki = []


def producent():
    for i in range(1, n + 1):
        print("Producent dodal:", i)
        kolejka.put(i)
        time.sleep(0.1)

    kolejka.put(None)
    kolejka.put(None)


def konsument_parzyste():
    while True:
        x = kolejka.get()

        if x is None:
            break

        if x % 2 == 0:
            print("Parzyste:", x)
            parzyste_wyniki.append(x)
        else:
            kolejka.put(x)

        time.sleep(0.1)


def konsument_nieparzyste():
    while True:
        x = kolejka.get()

        if x is None:
            break

        if x % 2 == 1:
            print("Nieparzyste:", x)
            nieparzyste_wyniki.append(x)
        else:
            kolejka.put(x)

        time.sleep(0.1)


t_prod = threading.Thread(target=producent)
t_parz = threading.Thread(target=konsument_parzyste)
t_nieparz = threading.Thread(target=konsument_nieparzyste)

t_prod.start()
t_parz.start()
t_nieparz.start()

t_prod.join()
t_parz.join()
t_nieparz.join()

print("\nPodsumowanie:")
print("Parzyste:", parzyste_wyniki)
print("Nieparzyste:", nieparzyste_wyniki)

print("Koniec")