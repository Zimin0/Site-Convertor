import os

# Получаем путь к директории, где находится скрипт
script_dir = os.path.dirname(os.path.realpath(__file__))

# Обходим все директории и файлы, начиная с директории скрипта
for root, dirs, files in os.walk(script_dir):
    # Если мы находимся в директории "migrations"
    if os.path.basename(root) == 'migrations':
        # Обходим все файлы в текущей директории
        for file in files:
            # Если файл имеет расширение .py или .pyc и не является __init__.py
            if (file.endswith('.py') or file.endswith('.pyc')) and file != '__init__.py':
                # Получаем полный путь к файлу
                file_path = os.path.join(root, file)
                # Удаляем файл
                os.remove(file_path)
                print(f"Deleted file: {file_path}")