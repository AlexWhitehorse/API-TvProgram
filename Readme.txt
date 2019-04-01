!Программа разрабатывалась для python 3.6+
!Проверено для Ubuntu 18, Ubuntu 16

Запуск: puthon3 main.py

Для работы программы необходимо:

python 3

    Зависимости:

        grab
        datetime
        timedelta
        transliterate

Установка:

    0. sudo apt-get update

    1. Установить python3
        sudo apt install python3

    2. Рекомендуеться установить менеджер пакетов python3
        sudo apt install pyton3-pip

    3. Далее можно установить все зависимость вучную либо запустить insallDepends.sh
        в случае ошибки insallDepends.sh, продолжить установку вручную

        - Как запустить установку с помощью insallDepends.sh?

            1. chmod +x insallDepends.sh
            2. sudo ./insallDepends.sh

    4. Ручная установка:

        1. pip3 install -U grab
            
            - в случае возникновения ошибки:

                https://grablab.org/docs/usage/installation.html

        2. pip3 install datetime

        3. pip3 install timedelta

        4. pip3 install transliterate

