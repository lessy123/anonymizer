from faker import Faker
def generate_names(country='ru_RU', num=5):
    fake = Faker(country) # initialize the faker instance for chosen country
    print('\n{} Fake Names: '.format(country))
    for i in range(num): print(fake.name()) # just to save line, don't code like this.

def generate_name(country='ru_RU'):
    fake = Faker(country) # initialize the faker instance for chosen country
    return fake.name()
def generate_first_name(country='ru_RU'):
    fake = Faker(country)
    return fake.first_name()
def generate_last_name(country='ru_RU'):
    fake = Faker(country)
    return fake.last_name()
def generate_address(country='ru_RU'):
    fake = Faker(country)
    return fake.address()
def generate_street_address(country='ru_RU'):
    fake = Faker(country)
    return fake.street_address()
def generate_street_name(country='ru_RU'):
    fake = Faker(country)
    return fake.street_name()
def generate_email(country='ru_RU'):
    fake = Faker(country)
    return fake.email()
def generate_phone(country='ru_RU'):
    fake = Faker(country)
    return fake.phone_number()
def generate_city(country='ru_RU'):
    fake = Faker(country)
    return fake.city()
def generate_credit_card(country='ru_RU'):
    fake = Faker(country)
    return fake.credit_card_number()
# generate_name('ja_JP')
# generate_name('en_US')
# print(__name__)
if __name__=="__main__":
    # print(generate_first_name('en_US'))
    # print(generate_last_name('ru_RU'))
    print(generate_city('ru_RU'))

