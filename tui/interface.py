import urwid
from address_book.Addressbook import AddressBook
from address_book.models_book import Record


class ContactBookApp:
    def __init__(self, book: AddressBook):
        self.book = book
        self.overlay_open = False  # флаг открытого окна overlay
        self.COLUMN_WEIGHTS = [14, 20, 20, 10, 10, 10]
        self.HEADERS = [" Name", "Phone", "Email",
                        "Address", "Birthday", "Notes"]

        self.palette = [
            ('header', 'white', 'dark blue'),
            ('footer', 'black', 'light gray'),
            ('selected', 'black', 'light cyan'),
            ('default', 'white', 'black'),
            ('button_green', 'black', 'dark green'),
            ('button_green_focus', 'white', 'dark green', 'bold'),
            ('button_red', 'white', 'dark red'),
            ('button_red_focus', 'black', 'dark red', 'bold'),
        ]

        # создаем меню футера:
        self.menu = urwid.Text(
            "[↑/↓] Move  [Enter] Select  [A]dd  [E]dit  [D]elete [Q]uit", align='center')
        self.footer = urwid.AttrMap(self.menu, 'footer')

        # Заголовок таблицы
        self.header_row = self.create_table_row('header',
                                                self.HEADERS, is_header=True)
        # Контактный список
        self.walker = urwid.SimpleFocusListWalker(self.build_contact_list())
        self.listbox = urwid.ListBox(self.walker)
        # Основная область
        self.list_area = urwid.Pile([
            ('pack', self.header_row),
            self.listbox
        ])

        # Основной вид, обёрнутый в рамку
        self.view = urwid.Frame(
            # header=self.header,
            body=self.create_mc_linebox(
                self.list_area, title=" 📒 Адресная книга "),
            footer=self.footer
        )

        # Переменная для хранения текущего оверлея
        self.overlay = None

    # Обновление текста футера в зависимости от контекста:
    def update_footer(self):
        if not self.book.data:
            contact_info = "No contact selected"
        else:
            selected_contact = self.book.get_record_by_index(
                self.book.selected_index)
            contact_info = f"Selected: {selected_contact.get_name()}" if selected_contact else "No contact selected"
        self.menu.set_text(
            f"[↑/↓] Move  [Enter] Select  [A]dd  [E]dit  [D]elete [Q]uit | {contact_info}")

    def create_mc_linebox(self, widget, title=""):
        return urwid.LineBox(
            widget,
            title=title,
            tlcorner='┌', tline='─', lline='│',
            trcorner='┐', rline='│',
            blcorner='└', bline='─', brcorner='┘'
        )

    def create_table_row(self, attr, columns, is_header=False):
        """Создаёт строку таблицы с равномерным заполнением и выделением"""
        # Собираем текст строки с разделителями
        row_text = " │ ".join(
            col.ljust(self.COLUMN_WEIGHTS[i]) for i, col in enumerate(columns)
        )
        # Создаём Text-виджет, который занимает всю ширину
        text_widget = urwid.Text(row_text, align='left')

        # Оборачиваем в AttrMap:
        # - если заголовок — используем стиль 'header'
        # - если нет — используем стиль 'default' + активный стиль 'reveal focus'
        if is_header:
            return urwid.AttrMap(text_widget, 'header')
        else:
            return urwid.AttrMap(text_widget, attr)  # , 'reveal focus')

    def build_contact_list(self):
        rows = []
        for idx, key in enumerate(self.book.data):
            # for key in self.book.data:
            record = self.book.data[key]
            attr = 'selected' if idx == self.book.selected_index else 'default'
            row_data = [
                record.get_name(),
                record.get_phones(),
                record.get_email(),
                record.get_address(),
                record.get_birthday(),
                record.get_notes()
            ]
            row = self.create_table_row(attr, row_data)
            # row = urwid.AttrMap(row, None, 'reveal focus') # Важно!
            row = urwid.AttrMap(row, attr)
            rows.append(row)
        return rows

    def refresh_list(self):
        # Сохраняем текущий индекс выбранной строки
        current_focus = self.book.selected_index
        # Очищаем и обновляем список
        self.walker.clear()
        self.walker.extend(self.build_contact_list())
        # Восстанавливаем фокус на выбранную строку
        if 0 <= current_focus < len(self.walker):
            self.walker.set_focus(current_focus)
        # Обновляем футер
        self.update_footer()

    def keypress(self, key):
        # if self.overlay_open:
        #     return  # Пока открыт popup, игнорируем глобальные клавиши
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()
        elif key in ('down',):
            self.update_footer()
            # self.show_error(
            #     f'sel index: {self.book.selected_index}, len: {len(self.book.data)}')
            if self.book.selected_index < len(self.book.data) - 1:
                self.book.selected_index += 1
        elif key in ('up',):
            self.update_footer()
            # self.show_error(
            #     f'sel index: {self.book.selected_index}, len: {len(self.book.data)}')
            if self.book.selected_index > 0:
                self.book.selected_index -= 1
        elif key == 'a':
            self.add_contact()
        elif key == 'd':
            if not self.book.data:
                return  # Ничего не делаем, если адресная книга пуста
            self.book.remove_record_by_index(self.book.selected_index)
        elif key == 'enter':
            if not self.book.data:
                return  # Ничего не делаем, если адресная книга пуста
            self.edit_contact(self.book.selected_index)
        elif key in ('h', 'H'):
            self.show_help()
        self.refresh_list()

    def create_contact_form(self, record=None):
        """Создает форму для добавления или редактирования контакта."""
        # Поля редактирования
        edit_name = urwid.Edit("Name: ", record.get_name() if record else "")
        edit_phone = urwid.Edit(
            "Phone: ", record.get_phones() if record else "")
        edit_email = urwid.Edit(
            "E-Mail: ", record.get_email() if record else "")
        edit_address = urwid.Edit(
            "Address: ", record.get_address() if record else "")
        edit_birthday = urwid.Edit(
            "Birthday: ", record.get_birthday() if record else "")
        edit_notes = urwid.Edit(
            "Notes: ", record.get_notes() if record else "")

        # Кнопки
        s_button = urwid.Button("💾 Save", align='center')
        cancel_button = urwid.Button(
            "❌ Cancel", self.close_popup, align='center')
        # Цвета кнопок
        save_button = urwid.AttrMap(
            s_button, 'button_green', focus_map='button_green_focus')
        cancel_button = urwid.AttrMap(
            cancel_button, 'button_red', focus_map='button_red_focus')
        # Компоновка формы
        pile = urwid.Pile([
            urwid.Divider(),
            edit_name,
            edit_phone,
            edit_email,
            edit_address,
            edit_birthday,
            edit_notes,
            urwid.Divider(),
            urwid.Columns([save_button, cancel_button],
                          dividechars=2, min_width=10),
            urwid.Divider()
        ])

        # Рамка с заголовком
        if record:
            boxtitle = record.get_name()
        else:
            boxtitle = 'New record'
        title = f" ✏️ Редактирование — {boxtitle} "
        boxed = urwid.LineBox(
            pile,
            title=title,
            tlcorner='╭', tline='─', lline='│',
            trcorner='╮', rline='│',
            blcorner='╰', bline='─', brcorner='╯',
            title_align='center')  # Попробуй выровнять заголовок по центру

        overlay = urwid.Overlay(
            boxed, self.view,
            align='center', width=('relative', 50),
            valign='middle', height=('relative', 50)
        )

        return overlay, s_button, (edit_name, edit_phone, edit_email, edit_address, edit_birthday, edit_notes)

    def add_contact(self):
        if not hasattr(self, 'loop'):
            raise RuntimeError(
                "Application loop is not initialized. Call run() first.")
        overlay, save_button, data = self.create_contact_form()
        urwid.connect_signal(save_button, 'click',
                             self.save_contact, data + (-1,))
        self.show_overlay(overlay)

    def edit_contact(self, index):
        if not hasattr(self, 'loop'):
            raise RuntimeError(
                "Application loop is not initialized. Call run() first.")
        record = self.book.get_record_by_index(index)
        if not record:
            return
        form, save_button, data = self.create_contact_form(record)
        urwid.connect_signal(save_button, 'click',
                             self.save_contact, data + (index,))
        self.show_overlay(form)

    def show_overlay(self, overlay):
        # Сохраняем текущий виджет (основной интерфейс) перед отображением оверлея
        self.previous_widget = self.loop.widget
        self.loop.widget = overlay
        self.overlay_open = True

    def close_popup(self, button=None):
        if hasattr(self, 'previous_widget'):
            self.loop.widget = self.previous_widget
        self.overlay_open = False
        self.refresh_list()
        # Очистка сигналов
        if button:
            urwid.disconnect_signal(button, 'click', self.save_contact)

    def save_contact(self, button, data):
        edit_name, edit_phone, edit_email, edit_address, edit_birthday, edit_notes, index = data
        new_rec = Record(
            edit_name.edit_text,
            edit_phone.edit_text,
            edit_birthday.edit_text,
            edit_email.edit_text,
            edit_address.edit_text,
            edit_notes.edit_text
        )
        if index >= 0:
            self.book.update_record_by_index(index, new_rec)
        else:
            self.book.add_record(new_rec)
        self.close_popup()

    def show_error(self, message):
        error_text = urwid.Text(
            ('button_red', f"\n⚠️  {message}\n"), align='center')
        ok_button = urwid.Button("❌ Закрыть", self.close_popup)
        ok_button = urwid.AttrMap(
            ok_button, 'button_red', focus_map='button_red_focus')

        pile = urwid.Pile([
            error_text,
            urwid.Divider(),
            urwid.Padding(ok_button, align='center', width=12),
            urwid.Divider()
        ])

        box = urwid.LineBox(
            pile,
            title=" Ошибка ",
            title_align='center',
            tlcorner='╭', tline='─', lline='│',
            trcorner='╮', rline='│',
            blcorner='╰', bline='─', brcorner='╯'
        )

        overlay = urwid.Overlay(
            box, self.view,
            align='center', width=('relative', 50),
            valign='middle', height=('relative', 30)
        )
        self.show_overlay(overlay)

    def show_error1(self, message):
        error_text = urwid.Text(f"Error: {message}")
        overlay = urwid.Overlay(
            urwid.LineBox(error_text),
            self.view,
            'center', 40, 'middle', 10
        )
        self.loop.widget = overlay

    def show_help(self):
        """Показывает справку."""
        help_text = urwid.Text("""
        Клавиши управления:
        ────────────────────────────────────────────────
        ↑ / ↓       Переместить курсор
        Enter       Редактировать выбранный контакт
        A           Добавить новый контакт
        E           Редактировать выбранный контакт
        D           Удалить выбранный контакт
        Q           Выйти из программы
        """, align='left')
        ok_button = urwid.Button("OK", self.close_popup)
        ok_button = urwid.AttrMap(
            ok_button, 'button_green', focus_map='button_green_focus')
        pile = urwid.Pile([
            help_text,
            urwid.Divider(),
            urwid.Padding(ok_button, align='center', width=10)
        ])
        box = urwid.LineBox(pile, title="📘 Справка",
                            tlcorner='╭', tline='─', lline='│',
                            trcorner='╮', rline='│',
                            blcorner='╰', bline='─', brcorner='╯',
                            title_align='center')
        overlay = urwid.Overlay(
            box, self.view, align='center', width=60, valign='middle', height=16)
        self.show_overlay(overlay)

    def run(self):
        self.loop = urwid.MainLoop(
            self.view, self.palette, unhandled_input=self.keypress)
        self.loop.run()
