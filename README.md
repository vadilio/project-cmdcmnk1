# Персональний помічник (Personal Assistant)

## ⚙️ Опис
**Персональний помічник** - це консольна програма, яка дозволяє зберігати та управляти контактами та нотатками. Програма розроблена на Python з використанням об'єктно-орієнтованого підходу.

## 👉 Пояснення коду:

Класи полів (Field, Name, Phone, Email, Birthday, Address): Використовуються для зберігання та валідації окремих частин інформації про контакт. Phone, Email та Birthday мають вбудовану перевірку формату за допомогою регулярних виразів та datetime.

Клас Record: Представляє один запис (контакт) у адресній книзі. Містить ім'я, список телефонів, адресу, email та день народження. Має методи для додавання, видалення, редагування телефонів та встановлення інших полів, а також метод days_to_birthday для обчислення днів до дня народження.

Клас AddressBook: Наслідується від UserDict і керує записами контактів. Має методи для додавання, пошуку, видалення записів, пошуку за критеріями та отримання списку контактів з найближчими днями народження.

Класи для Нотаток (Note, NotesManager):

Note: Представляє окрему нотатку з текстом, набором тегів та датою створення. Має методи для додавання/видалення тегів та редагування тексту.

NotesManager: Керує списком нотаток. Дозволяє додавати, шукати (за текстом або тегом), редагувати, видаляти та сортувати нотатки за тегом.

Збереження/Завантаження (save_data, load_data): Функції використовують модуль pickle для серіалізації (збереження) об'єктів AddressBook та NotesManager у файли (contacts.pkl, notes.pkl) та їх десеріалізації (завантаження) при запуску. Дані зберігаються у підпапці personal_assistant_data. Функція ensure_data_dir_exists створює цю папку, якщо її немає.

Обробники команд (add_contact, edit_contact, delete_contact і т.д.): Кожна функція відповідає за виконання певної команди користувача. Вони приймають аргументи (args) та відповідний об'єкт (book або notes) для маніпуляції даними.

Декоратор @input_error: Обгортає функції-обробники для перехоплення та обробки типових помилок (неправильний формат даних, відсутність контакту/нотатки тощо), повертаючи користувачеві зрозуміле повідомлення про помилку.

***Парсинг та Основний цикл (parse_input, main, find_closest_command):***

parse_input: Розбиває введення користувача на команду та аргументи.
find_closest_command: Реалізує додатковий функціонал вгадування команди за допомогою difflib, якщо користувач ввів щось невідоме.
main: Основний цикл програми. Завантажує дані, вітає користувача, читає команди, викликає відповідні обробники, обробляє вихід та зберігає дані перед завершенням.
Допомога (show_help): Функція генерує текст довідки зі списком доступних команд та їх описом.


## Як використовувати:

- Збережіть код у файл (наприклад, assistant.py).
- Запустіть його з терміналу: python assistant.py.

## Вводьте команди, наприклад:
- hello
- add_contact Богдан (далі програма запитає інші дані)
- add_note (програма запитає текст і теги)
- show_contacts
- show_notes
- find_contact Богдан
- find_notes робота
- birthdays
- help
- exit
