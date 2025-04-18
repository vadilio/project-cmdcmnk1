# from address_book.Models import Name, Phone, Record

# class PhoneValidationError(Exception):
#     """Кастомное исключение для ошибок валидации номера телефона."""
#     pass


# class BirthdayValidationError(Exception):
#     """Кастомное исключение для ошибок валидации ДР."""
#     pass


# def input_error(func):
#     """Декоратор для обробки помилок при додаванні нової записи"""
#     def inner_func(*args, **qwargs):
#         try:
#             return func(*args, **qwargs)
#         except ValueError:
#             return 'Невірна команда \n'
#         except PhoneValidationError as e:
#             return f'{e}\n'
#         except BirthdayValidationError as e:
#             return f'{e}\n'
#     return inner_func


# --- Обробники Команд ---


def input_error(func):
    """Декоратор для обробки помилок введення та інших винятків під час виконання команди."""
    def inner(*args, **kwargs):
        try:
            # Перший аргумент args - це кортеж аргументів команди (args,),
            # другий - book або notes_manager
            return func(*args, **kwargs)
        except ValueError as e:
            # Помилки валідації даних (неправильний формат тощо)
            return f"Помилка даних: {e}"
        except KeyError as e:
            # Спроба доступу до неіснуючого контакту за ім'ям
            return f"Помилка: Контакт з ім'ям '{e}' не знайдено."
        except IndexError:
            # Неправильний індекс для нотатки
            return "Помилка: Неправильний індекс. Перевірте індекси у списку нотаток."
        except TypeError as e:
            # Неправильний тип аргументів для функції
            return f"Помилка типу аргументів: {e}"
        except AttributeError as e:
            # Спроба доступу до неіснуючого атрибута (може статися при помилках завантаження даних)
            return f"Помилка атрибуту: {e}. Можливо, дані пошкоджено."
        except Exception as e:
            # Інші, непередбачені помилки
            return f"Сталася непередбачена помилка: {e}"
    return inner
