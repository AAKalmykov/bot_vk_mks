import files

# Функция для сохранения слов в файле
def save_words_to_file(words):
  with open('words.txt', 'a') as file:
    file.write('\n'.join(words) + '\n')
