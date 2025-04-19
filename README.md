# goit-pythonweb-hw-04

Скрипт для асинхронного сортування файлів за розширенням.

## Як використовувати

1. Встановіть залежності:
   pip install -r requirements.txt

2. Створіть папку з файлами, наприклад "source".

3. Запустіть скрипт:
   python src/sort_files_by_extension_async.py source output

Файли з папки "source" будуть скопійовані в папку "output" і розкладені по підпапках за типом (txt, jpg, pdf тощо).

Усі дії зберігаються у файл логів file_sorter.log.
