from transliterate import translit

def transliterate_text(text):
    return translit(text, language_code='ru', reversed=True)

if __name__=="__main__":
    ru_text = 'Лорем ипсум долор сит амет'
    text = transliterate_text(ru_text)
    print(text)