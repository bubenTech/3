from math import log2
from copy import deepcopy, copy
import itertools
from decimal import Decimal


def srednee(arr_propability, codding):
    s = 0
    for i in range(len(arr_propability)):
        s += arr_propability[i] * len(codding[i])

    return round(s, 8)


def shenon_fano(arr_propability: list, start: int, end: int, codding: list):
    if end - start == 2:
        codding[start] += "0"
        codding[start + 1] += "1"
        return codding

    i = start
    different_1 = abs(sum(arr_propability[start:i + 1]) - sum(arr_propability[i + 1:end]))
    while i < end:
        different_2 = abs(sum(arr_propability[start:i + 2]) - sum(arr_propability[i + 2:end]))
        if different_1 < different_2:
            break
        different_1 = different_2
        i += 1

    for k in range(start, i + 1):
        codding[k] += "0"
    for k in range(i + 1, end):
        codding[k] += "1"

    if (i + 1 - start == 1) and (end - i - 1) == 1:
        return codding

    if i + 1 - start != 1:
        codding = shenon_fano(arr_propability, start, i + 1, codding)
    if end - i - 1 != 1:
        codding = shenon_fano(arr_propability, i + 1, end, codding)

    return codding


def sorted_dict(diction: dict):
    b = list(diction.items())
    b.sort(key=lambda x: x[1], reverse=True)

    values = list(map(lambda x: x[1], b))
    keys = list(map(lambda x: x[0], b))

    return keys, values

def block_coding(diction: dict, n: int):
    keys = list(diction.keys())
    values = list(diction.values())
    block_tuple = list(itertools.product(keys, repeat=n))
    block_keys = []
    for tuple in block_tuple:
        s = ""
        for k in tuple:
            s += str(k)
        block_keys.append(s)

    block_tuple = list(itertools.product(values, repeat=n))
    block_value = []
    for tuple in block_tuple:
        s = 1
        for k in tuple:
            s *= k
        block_value.append(round(s, 8))

    block_tuple = sorted_dict(dict(zip(block_keys, block_value)))
    block_keys = block_tuple[0]
    block_value = block_tuple[1]

    codding = shenon_fano(block_value, 0, len(block_value), ["" for i in range(len(block_value))])
    k = 0
    for i in zip(block_keys, codding):
        print('{0}: {2:<8} {1}'.format(i[0], i[1], block_value[k]))
        k += 1
    print('Средняя длина (количество блоков {0}): {1}/{0} = {2}'.format(n, srednee(values, codding), round(srednee(values, codding) / n, 8)))
    print('Энропия равна: ', -sum(map(lambda p: p*log2(p) if p != 0 else 0 ,block_value)) / n)

    string = input("Введите сообщение, которое хотите закодировать: ")
    s = ""
    diction = dict(zip(block_keys, codding))
    t = ""
    for i in string:
        if len(t) != n:
            t += i
        else:
            s += diction[t]

    print('Закодированное сообщение:', s)
    from os import system
    system("pause")

if __name__ == "__main__":
    n = int(input('Введите размер алфавита: '))

    arr = {chr(ord('A') + i): float(input('Введите вероятность появления символа {0}: '.format(chr(ord('A') + i)))) for
           i in range(n)}
    b = arr.values()
    if abs(sum(arr.values()) - 1) > 0.0000001:
        print("Сумма вероятностей не равна 1")
        exit()
    n = int(input('Введите количество блоков: '))
    block_coding(arr, n)
    string = input("end ")

