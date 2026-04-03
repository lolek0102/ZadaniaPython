from multiprocessing import Process, Queue

def suma_poteg(n):
    suma = 0
    for i in range(1, 100):
        suma += n ** i
    return suma

def licz_zakres(start, end, queue):
    wyniki = []
    for n in range(start, end + 1):
        wyniki.append((n, suma_poteg(n)))
    queue.put(wyniki)


if __name__ == "__main__":
    start = 1
    koniec = 20
    liczba_procesow = 4

    queue = Queue()
    procesy = []

    rozmiar = (koniec - start + 1) 

    aktualny_start = start

    for i in range(liczba_procesow):
        aktualny_koniec = aktualny_start + rozmiar - 1

        if i == liczba_procesow - 1:
            aktualny_koniec = koniec

        p = Process(target=licz_zakres, args=(aktualny_start, aktualny_koniec, queue))
        procesy.append(p)
        p.start()

        aktualny_start = aktualny_koniec + 1

    wszystkie_wyniki = []

    for _ in procesy:
        wszystkie_wyniki.extend(queue.get())

    for p in procesy:
        p.join()

    wszystkie_wyniki.sort()

    for liczba, wynik in wszystkie_wyniki:
        print(f"Liczba: {liczba}, suma 100 potęg: {wynik}")