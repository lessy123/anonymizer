from natasha import (
    Segmenter,
    MorphVocab,
    
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    
    PER,LOC,
    NamesExtractor,
    DatesExtractor,
    MoneyExtractor,
    AddrExtractor,

    Doc
)
# import phonenumbers
import re 
import inn
import faker_generate as faker

morph_vocab = MorphVocab()

names_extractor = NamesExtractor(morph_vocab)
dates_extractor = DatesExtractor(morph_vocab)
money_extractor = MoneyExtractor(morph_vocab)
addr_extractor = AddrExtractor(morph_vocab)
def number_sum(string):
    # find sum to all digits without ECC number
    numbers = list(str(string))
    number_sum = 0
    lenght = len(numbers)
    for x in range(0, lenght):
        if x % 2 == 0:
            number = (int(numbers[x]) * 2)
            if int(number) > 9:
                double_numbers = list(str(number))
                number = int(double_numbers[0]) + int(double_numbers[1])
        else:
            number = (numbers[x])
        number_sum += int(number)
    return(number_sum)
def lunh_controling(string):
    if str(string).isdigit():
        # Count control string.
        number = str(string)[:-1]
        total_count = number_sum(number)
        value = int(total_count) + int(str(string)[-1])
        # Control multiplicity 10
        return(value % 10 == 0)
    else:
        return False    
def to_lunh(string):
    # Add control number.
    if str(string).isdigit():
        total_count = int(number_sum(string))
        # Find control number
        control = 0
        while control < 10:
            value = total_count + control  
            if (value % 10 == 0):
                break
            else:
                control += 1
        #Make new number
        lunh_number = str(string) + str(control)
        return(lunh_number)        
    else:
        return("Wrong date type")
def to_normal(string):
    if not(str(string).isdigit()):
        return("Wrong string")
    # Del control number.
    if lunh_controling(string):
        string = str(string)[:-1]
        return string
    else:
        return("ECC wrong")




def if_email(text):
    try:
        if len(text[:text.index('@')]) > 64 or len(text) > 254 or text.count('@') != 1:
            # print("заданная строка не может быть электронным адресом")
            return 0
        if text[0] == '@' or text[-1] == '@' or text[0] == '.' or text[-1] == '.' or text.count(' ') > 0:
            # print("заданная строка не может быть электронным адресом")
            return 0
    except BaseException:
        # print("заданная строка не может быть электронным адресом")
        return 0
    return 1
def if_phone(text):
    match = re.search(r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', text) 
    if match is None: return 0 
    else: return 1
def Luhn(card):
    try:
        # Здесь храним контрольную сумму
        checksum = 0
        # Переводим номер карточки из строки в массив чисел
        cardnumbers = list(map(int, card))
        # Проходимся по каждому числу
        for count, num in enumerate(cardnumbers):
            # Если index чётный, значит число стоит на нечётной позиции
            # Так получается потому что считаем с нуля
            if count % 2 == 0:
                buffer = num * 2
                # Если удвоенное число больше 9, то вычитаем из него 9 и прибавляем к контрольной сумме
                if buffer > 9:
                    buffer -= 9
                # Если нет, то сразу прибавляем к контрольной сумме
                checksum += buffer
            # Если число стоит на чётной позиции, то прибавляем его к контрольной сумме
            else:
                checksum += num
        # Если контрольная сумма делится без остатка на 10, то номер карты правильный
        return (checksum % 10 == 0)*1
    except:
        return 0

    # return 1 if match else 0
def classifity_text(text):
    check_name=[0,0,0,0,0,0,0,0,0,0,0]
    """
        0 - имя
        1 - отчество
        2 - фамилия
        3 - наличие другого местоположения помимо улицы
        4 - улица
        5 - дата
        6 - деньги
        7 - емаил
        8 - номер телефона(вычисляет исключительно русские номера)
        9 - инн
        10 - кредитная карта
    """
    

    result = names_extractor.find(text)
    # print(result)
    if result is not None:
            if result.fact.first is not None:
                check_name[0]=1
            if result.fact.middle is not None:
                check_name[1]=1
            if result.fact.last is not None:
                check_name[2]=1
            
    result = addr_extractor.find(text)
    if result is not None:
        for i in result.fact.parts:
            if (not (i.type=='дом') and not(i.type=='улица')):
                check_name[3]=1
            if i.type=='улица':
                check_name[4]=1
    # print(result)
    result = dates_extractor.find(text)
    if result is not None:
            check_name[5]=1
    # print(result)
    result = money_extractor.find(text)
    if result is not None:
            check_name[6]=1
    check_name[7]=if_email(text)
    check_name[8]=int(if_phone(text))
    check_name[9]=inn.inn_check_into_text(text)
    integ=""
    for i in range(len(text)):
        if '0' <= text[i] <= '9':
            integ+=text[i]
    if integ:
        check_name[10]=lunh_controling(int(integ))*1


    return check_name

            #if result.fact.middle is not None:
    print(check_name)
if __name__=="__main__":
    # print(classifity_text("ne_magl@mail.ru"))
    # print(classifity_text("84444"))
    # print(classifity_text("7877632773")) 
    # print(classifity_text("+7 877 632 77 73"))    
    # print(classifity_text("Улица Богатырей 12"))
    num1=0
    num2=0
    x=10000
    for i in range(x):
        creditka=faker.generate_credit_card()
        num1+=lunh_controling(creditka)
        num2+=Luhn(creditka)
        if i%100==0:
            print(i//100)
    print("num1",num1/x)
    print("num2",num2/x)

    """
        0 - имя
        1 - отчество
        2 - фамилия
        3 - наличие другого местоположения помимо улицы
        4 - улица
        5 - дата
        6 - деньги
        7 - емаил
        8 - номер телефона(вычисляет исключительно русские номера)
        9 - инн
        10 - кредитная карта
    """
    # creditka=faker.generate_credit_card()
    # print(creditka)
    # print(lunh_controling(creditka))
    # print(lunh_controling("5854"))
    # print(Luhn(creditka))



    # text = "Call me at +7 510-748-8230 if it's before 9:30, or on 703-4800500 after 10am."
    # for match in phonenumbers.PhoneNumberMatcher(text, "RU"):
    #     print(match)
    # r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$'

    # match = re.search(r'\d\d\D\d\d', r'Телефон 123-12-12') 
    # print(match[0] if match else 'Not found') 

    



