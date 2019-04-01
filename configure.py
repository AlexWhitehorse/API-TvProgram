#python 3.6.7

# IP сервера
HOST_NAME = 'localhost'


# PORT
PORT_NUMBER = 9000


# Login и password от VseTV
login = 'livetv'

password = 'odessaepg'



#Включить/выключть логи ошибок
logging_err = False

#Частота очищения лога ошибок в секундах или не очищать(False)
#96 hours * 3600sec(1hour) = 4 days
logging_err_cl_f = 96 * 3600




#Вкл/выкл лог обновлений файлов
logging_upd = False

#Частота очищения лога обновлений в секундах или не очищать(False)
#6 hours * 3600sec(1hour)
logging_upd_cl_f = 6 * 3600




#Вкл/выкл лог сервера(запуск/остановка)
logging_srv = True

#Частота очищения лога сервера или не очищать(False)
logging_srv_cl_f = False


#Ручная коректировка UTC
flag_UTC = False # False(авто-коректировка) или числовое значение




#Имена файлов логов
name_log_updates = 'Updates_log.txt'

name_err_log = 'Errors.txt'

#name log fille of server
name_server_log = 'Server_log.txt'

#Частота обновления телепрограммы с сайта
# 12 hours * 3600 seconds( - 1 hour)
freq = 12 * 3600

#Частота обновления локальных файлов телепрограм и текущих файлов всех каналов
#300 sec = 5 min
freq_local = 300




#Список (ID канала : Название)\
# -По названию происходит обращение к серверу
dict_ID_channels = {
    '685' : 'ekotv',
    '827' : 'uakrym',
    '1249' : 'ua1',
    '1199' : '3tvod',
    '1200' : '31chod',
    '874' : 'sonce',
    '1329' : 'uaod',
    '285' : 'uakult',
    '823' : 'rada',
    '1298' : 'dumska',
    '933' : '7tvod',
    '1148' : 'wave',
    '871' : 'nadia',
    '921' : '112ua',
    '1379' : 'tgtv',
    '25' : 'prmua'
}

# Кодтровка файлов
encod = 'utf-8'

#  Путь к файлам телепрограммы
path_to_file = 'temp/'


# Имя файла в который копируеться данные из VseTv
nameXMLFille = path_to_file + 'TvProgram.xml'

# Путь к логам
path_to_log_lile = 'logs/'

#ССылка, которая используеться для парсинга телепрограммы
url = u'http://' + login + ':' + password + '@www.vsetv.com/export/livetv/epg/export.xml'
