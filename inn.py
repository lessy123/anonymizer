import random as rnd
import re 
 

#import random.randint as rnd.randint

def inn_ctrl_summ(nums, type):
    """
    Подсчет контрольной суммы
    """
    inn_ctrl_type = {
        'n2_12': [7, 2, 4, 10, 3, 5, 9, 4, 6, 8],
        'n1_12': [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8],
        'n1_10': [2, 4, 10, 3, 5, 9, 4, 6, 8],
    }
    n = 0
    l = inn_ctrl_type[type]
    for i in range(0, len(l)):
        n += nums[i] * l[i]
    return n % 11 % 10

def inn_gen(l=None):
    """
    Генерация ИНН (10 или 12 значный)
    На входе указывается длина номера - 10 или 12.
    Если ничего не указано, будет выбрана случайная длина.
    """
    if not l:
        l = list((10, 12))[rnd.randint(0, 1)]
    if l not in (10, 12):
        return None
    nums = [
        rnd.randint(1, 9) if x == 0
        else rnd.randint(0, 9)
        for x in range(0, 9 if l == 10 else 10)
    ]
    if l == 12:
        n2 = inn_ctrl_summ(nums, 'n2_12')
        nums.append(n2)
        n1 = inn_ctrl_summ(nums, 'n1_12')
        nums.append(n1)
    elif l == 10:
        n1 = inn_ctrl_summ(nums, 'n1_10')
        nums.append(n1)
    return ''.join([str(x) for x in nums])

def inn_check(inn):
    """
    Проверка ИНН на корректность
    В соответствии с алгоритмом, описанным по ссылке:
        https://ru.wikipedia.org/wiki/Контрольное_число
    """
    sinn = str(inn)
    nums = [int(x) for x in sinn]
    if len(sinn) == 10:
        n1 = inn_ctrl_summ(nums, 'n1_10')
        return n1 == nums[-1]
    elif len(sinn) == 12:
        n2 = inn_ctrl_summ(nums, 'n2_12')
        n1 = inn_ctrl_summ(nums, 'n1_12')
        return n2 == nums[-2] and n1 == nums[-1]
    else:
        return False
def inn_check_into_text(string):
    regex = "^[0-9 -]+$"

    pattern = re.compile(regex)

    if pattern.search(string) is not None: 
        s1 = "".join(c for c in string if  c.isdecimal())
        return int(inn_check(s1))
    else:
        return 0

if __name__=="__main__":
    # print(inn_check(inn_gen()))
    # print(inn_gen())
    print(inn_gen())
    # print(inn_check_into_text("7 87 76 3 27-773 "))
