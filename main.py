#!/usr/bin/env python
#-*- coding: utf-8 -*-

#python 3.6.7

from configure import *
from http.server import BaseHTTPRequestHandler, HTTPServer
from grab import Grab
import xml.etree.ElementTree as etree
from pprint import pprint
from datetime import datetime, timedelta, timezone
from transliterate import translit
import sys
import threading
import time

g = Grab()

g.setup(method = 'get')



list_translit_ch = dict()

listNamesChsnnels = dict()

def translatechannels(nameChannel_en):
    if nameChannel_en == 'Monday':
        return 'понедельник'
    elif nameChannel_en == 'Tuesday':
        return 'вторник'
    elif nameChannel_en == 'Wednesday':
        return 'среда'
    elif nameChannel_en == 'Thursday':
        return 'четверг'
    elif nameChannel_en == 'Friday':
        return 'пятница'
    elif nameChannel_en == 'Saturday':
        return 'суббота'
    elif nameChannel_en == 'Sunday':
        return 'воскресенье'

# Get current timezone for Ukraine
def timezn(flag = False):

    if flag == False:

        a = datetime.utcfromtimestamp(0)
        b = datetime.fromtimestamp(0)

        l_tz = timezone(b - a)

        c = str(l_tz)
        #print(c)
        c = int(c[5])

        return c

    return flag

#UTC
tmzone = timezn(flag_UTC)

# The function to get content from vsetv and save this in to file
def get_content():

    try:
        response = g.go(url)
        out = response.unicode_body()

        open('TvProgram.xml', 'w', encoding= encod).write(response.unicode_body())
    except:
        time.sleep(3)
        get_content()

def getProgressTime(time_start, time_end): # Strings t_s t_e

    #Преобраует строковые данные в timedelta           
    time_start = datetime.strptime(time_start[:14],"%Y%m%d%H%M%S")
    time_end = datetime.strptime(time_end[:14],"%Y%m%d%H%M%S")

    # UTC +/- tmzone
    time_start = time_start + timedelta(hours = tmzone)
    time_end = time_end + timedelta(hours = tmzone)


    #Formatting the current time into the need string
    timeNow = datetime.now()
    formatTime = timeNow.strftime("%Y%m%d%H%M%S")
    time_now = datetime.strptime(str(formatTime),"%Y%m%d%H%M%S")

        #Прогрес времени телепрограммы
    time_prog = time_now - time_start

        #длительность телепрограммы
    time_difference = (time_end - time_start)

        #Перевод в сикунды для простоты вычислений
    time_difference_seconds = time_difference.total_seconds()
    time_prog_seconds = time_prog.total_seconds()

    progress_seconds = time_difference_seconds - time_prog_seconds

    time_prog_seconds = time_difference_seconds - progress_seconds

    result = time_prog_seconds / time_difference_seconds * 100

    result = int(result)

    if 0 > result or result > 100:
        return 111

    return result

def translit_channel(channel_name):
    del_smbls = '(),\'/.: _'

    channel_name = channel_name.lower()

    tr_ch = translit(channel_name, "ru", reversed=True)

    for i in del_smbls:

        tr_ch = tr_ch.replace(i, "")   

    return  tr_ch


def list_translit():

    tree = etree.parse('TvProgram.xml')
    root = tree.getroot()

    for prog in root.findall("channel"):

        name_ch = prog.find('display-name').text

        list_translit_ch[translit_channel(name_ch)] = name_ch

    return list_translit_ch

def printListChannels():

    list_translit()

    for ch in list_translit_ch:

        print(ch)

def getTVProgramOnWeek(nameChannel):

    tree = etree.parse('TvProgram.xml')
    root = tree.getroot()

    #Получение ИД канала по имени
    for prog in root.findall("channel"):

        nameChannel_find = prog.find('display-name').text

        if nameChannel_find == nameChannel:

            # ID of channel
            channelID = prog.get('id')

            break


    timeNow = datetime.now()

    timeNow_format = timeNow.strftime("%Y%m%d%H%M%S")
    time_now = datetime.strptime(str(timeNow_format),"%Y%m%d%H%M%S")



    setDayOfWeek = 'понедельник'

    out_str =  '{"'+ setDayOfWeek +'":['

    for prog in root.findall('programme'):

        out = prog.get('channel')
        
        if out == channelID:

            time_start = prog.get('start')
            time_end = prog.get('stop')

            time_start_format = datetime.strptime(time_start[:14],"%Y%m%d%H%M%S")

            # Добавление временной зоны для старта и конца телепередачи
            time_start_format = time_start_format + timedelta(hours = tmzone)

            # приведение к стандарту вывода
            time_start_format_out = time_start_format.strftime("%Y%m%d%H%M")
            time_start_format_forCompare = time_start_format.strftime("%Y%m%d")

            time_end_format = datetime.strptime(time_end[:14],"%Y%m%d%H%M%S")
            
            # Добавление временной зоны для старта и конца телепередачи
            time_end_format = time_end_format + timedelta(hours = tmzone)

            time_end_format_out = time_end_format.strftime("%Y%m%d%H%M")
            
            dayOfWeek = datetime.strptime(str(time_start_format_out),"%Y%m%d%H%M").strftime("%A")

            

            title_curProg = prog.find('title').text
            title_curProg = title_curProg.replace("\"", '')

            currentProg_progress = getProgressTime(time_start_format_out+'00', time_end_format_out+'00')
            
            # День недели 0 - 6
            numDayOfWeek_now = timeNow.weekday()
            
            #Число понедельника текущей недели
            this_monday = timeNow + timedelta(days=int(-numDayOfWeek_now), hours=int(-time_now.hour), minutes=-time_now.minute)
  
            #Число воскресенья текущей недели
            this_sunday = this_monday + timedelta(days=6)

            #Приведение формата для строки сравнения
            this_monday_format = this_monday.strftime("%Y%m%d")
            this_sunday_format = this_sunday.strftime("%Y%m%d")


            #Находит программу в промкжутке текущей недели
            # TO DO
            # + Баг!! на канале wave выводит {"понедельник":], а после идет воскресенье
            # + Не правильно выводит текушую передачу
            # + Не правильно показывает день недели + нет загаловка в виде дня недели
            # ++ Исправлено 13:04:2019

            # Если тукушая дата понедельником м воскресеньем
            if this_monday_format <= time_start_format_forCompare <= this_sunday_format:

                if setDayOfWeek != translatechannels(dayOfWeek):

                    setDayOfWeek = translatechannels(dayOfWeek)

                    out_str = out_str[:-1] + '],\"'+ setDayOfWeek +'\":['

                title_curProg = prog.find('title').text
                title_curProg = title_curProg.replace("\"", '')

                currentProg_start = time_start_format
                currentProg_end = time_end_format

                out_str += ('{"%s":"%s","%s":"%s","%s":"%s","%s":"%s","%s":"%s","%s":%s},' % (
                    'nameChannel',dict_ID_channels[out],'nameShow',title_curProg,
                    'startTime',time_start_format_out, 'endTime',time_end_format_out,
                    # 'dayOfWeek',translatechannels(dayOfWeek),
                    'dayOfWeek',setDayOfWeek,
                    'progress',currentProg_progress  ))

    return out_str[:-1] + ']}'



def currentTVProgramAllChannels():

    tree = etree.parse('TvProgram.xml')

    root = tree.getroot()

    # Словарь ТВ Каналов ID : channel
    channels_list = dict()

    # Заполнение словаря
    for channel in root.findall("channel"):
        #id : channel
        nameChannel = channel.find('display-name').text
        channel_ID = channel.get('id')

        channels_list[channel_ID] = nameChannel

        listNamesChsnnels[translit_channel(nameChannel)] = dict_ID_channels[channel_ID]


    # Поиск текущей телепрограммы каналов
    timeNow = datetime.now()
    
    timeNow_format = timeNow.strftime("%Y%m%d%H%M%S")
    time_now = datetime.strptime(str(timeNow_format),"%Y%m%d%H%M%S")
    
    out_str = '['

    for prog in root.findall('programme'):

        out = prog.get('channel')
        
        
        time_start = prog.get('start')
        time_end = prog.get('stop')

        time_start_format = datetime.strptime(time_start[:14],"%Y%m%d%H%M%S")        
        time_end_format = datetime.strptime(time_end[:14],"%Y%m%d%H%M%S")

        # Добавление временной зоны для старта и конца телепередачи
        time_start_format = time_start_format + timedelta(hours = tmzone)
        time_end_format = time_end_format + timedelta(hours = tmzone)

        time_start_format_out = time_start_format.strftime("%Y%m%d%H%M")
        time_end_format_out = time_end_format.strftime("%Y%m%d%H%M")

        if time_start_format < time_now and time_now < time_end_format:

            currentProg_progress = getProgressTime(time_start, time_end)

            title_prog = prog.find('title').text
            title_prog = title_prog.replace("\"", '')
                
            # !!
            dayOfWeek = datetime.strptime(time_start_format_out,"%Y%m%d%H%M%S").strftime("%A")

            out_str += '{"%s":"%s","%s":"%s","%s":"%s","%s":"%s","%s":"%s","%s":%s},' % (
                'nameChannel',dict_ID_channels[out],'nameShow',title_prog,
                'startTime',time_start_format_out, 'endTime',time_end_format_out,
                'dayOfWeek',translatechannels(dayOfWeek),
                'progress',currentProg_progress  ) 
    
    return out_str[:-1] + ']'

def writeTvProgramOnWeek():

    list_translit()
    
    for lst in list_translit_ch:
        
        nameCh = list_translit_ch[lst]

        f = open('tmp/'+lst+'.txt', 'w', encoding= encod)
        f.write('')
        f.close()

        f = open('tmp/'+lst+'.txt', 'a', encoding= encod)
        f.write(getTVProgramOnWeek(str(nameCh)))
        f.close

def writeCurrentProgram():

    f = open('tmp/currentProg.txt', 'w', encoding= encod)

    f.write(currentTVProgramAllChannels())

    f.close()

def writeListOfChannels():

    list_translit()

    f = open('tmp/listProgs.txt', 'w', encoding= encod)
    f.write('')
    f.close()

    for ls in list_translit_ch:

       f =  open('tmp/listProgs.txt', 'a', encoding= encod)
       f.write(str(ls)+" = "+str(list_translit_ch[ls])+'\n')
       f.close()

#Logining
def writerLOG(logining, log_way, log_nameFile, text):

    if logining:
    
        time_now = datetime.now()

        f = open(log_way + log_nameFile, 'a', encoding=encod)
        f.write(text + str(time_now) + '\n')
        
        f.close()


#Clearing logs
def clearLogs(log_way, lof_nameFille, frequency):

    if frequency != False:

        time.sleep(frequency)

        f = open(log_way + lof_nameFille, 'w')
        f.write('')
        f.close()
    
        clearLogs(log_way, lof_nameFille, frequency)


def newThread_claerLogs():

    #Error log
    clearLogs(path_to_log_lile, name_err_log, logging_err_cl_f)

    #Update log
    clearLogs(path_to_log_lile, name_log_updates, logging_upd_cl_f)

    #server
    clearLogs(path_to_log_lile, name_server_log, logging_srv_cl_f)


def newThread_getContent():

    try:

        while True:
            
            #Обновление смещения UTC
            tmzone = timezn(flag_UTC)

            get_content()
            
            #Лог обновлений файал с телепрограммой
            writerLOG(logging_upd, path_to_log_lile, name_log_updates, 'Update the source file sucsessful!  ')

            time.sleep(freq)
    except:

        
        writerLOG(logging_err, path_to_log_lile, name_err_log, 'Error updating TVprogram file!  ')

        time.sleep(1)

        newThread_getContent()

def newThread_update():
    
    try:


        while True:


            writeListOfChannels()

            writeCurrentProgram()
            
            writeTvProgramOnWeek()

            writerLOG(logging_upd, path_to_log_lile, name_log_updates, 'Update the program on week/currentProg is sucsessful!  ')


            time.sleep(freq_local)
    except:

        writerLOG(logging_err, path_to_log_lile, name_err_log, 'Refuse updating files the TV program on week/currentProgram  ')

        time.sleep(1)

        newThread_update()




#Запуск обновления файлов в отдельных потоках
def main():

    thrd_1 = threading.Thread(target=newThread_getContent)

    thrd_2 = threading.Thread(target=newThread_update)

    thrd_3 = threading.Thread(target=newThread_claerLogs)

    thrd_1.start()

    #Для минимизации ошибок, потоки стартуют с промежутком
    time.sleep(6)

    thrd_2.start()

    time.sleep(6)

    thrd_3.start()

class MyHandler(BaseHTTPRequestHandler):
    
    def do_HEAD(self):

        # Sends code to the browser that this page was found.
        self.send_response(200)

        #'Content-Type: application/json'
        self.send_header('Content-type', 'application/json')

        self.end_headers()


    def do_GET(self):
        
        listChannels = list()

        list_translit()

        # Можно упростить, совместив циклы
        for name_ch in list_translit_ch:

            
            listChannels.append(name_ch)


        getCurShowByID = '/Get_cut_shows_by_id?id='

        paths = dict()

        value = {'status' : 200}
        
        #Добавление адресов get запроса 
        for ch in listChannels:


            name = getCurShowByID + listNamesChsnnels[ch] 
            
            paths.update({name : value})

        paths.update({'/cur_shows' : value})

        if self.path in paths:
            

            self.respond(paths[self.path])

            for channel in listNamesChsnnels:


                if str(self.path) == getCurShowByID + listNamesChsnnels[channel]:


                    sng = open('tmp/'+ channel + '.txt', 'r', encoding = 'utf-8')

                    self.wfile.write(bytes(sng.read(), "utf-8"))

                    sng.close()

                    break

                elif str(self.path) == '/cur_shows':


                    sng = open('tmp/currentProg.txt', 'r', encoding = 'utf-8')

                    self.wfile.write(bytes(sng.read(), "utf-8"))

                    sng.close()

                    break
        
        else:
            
            self.respond({'status': 200})

            self.wfile.write(bytes("Error! - invalid url", "utf-8"))
        
    def handle_http(self, status_code, path):
        
        self.send_response(status_code)
        
        self.send_header('Content-type', 'application/json')
        
        self.end_headers()

        content = ''

        return bytes(content, 'UTF-8')

    def respond(self, opts):

        response = self.handle_http(opts['status'], self.path)
        
        self.wfile.write(response)


if __name__ == '__main__':

    server_class = HTTPServer

    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)

    writerLOG(logging_srv, path_to_log_lile, name_server_log, 'Server Starts - %s:%s  ' % (HOST_NAME, PORT_NUMBER))
    
    main()

    try:

        print('Server started %s:%s' % (HOST_NAME, PORT_NUMBER))

        httpd.serve_forever()


    except KeyboardInterrupt:

        print('Server stopped %s:%s' % (HOST_NAME, PORT_NUMBER))

        pass



    # При любой ошибке на сервере, он перезагружается
    except:

        print('Server Error %s:%s' % (HOST_NAME, PORT_NUMBER))

        writerLOG(logging_srv, path_to_log_lile, name_server_log, 'Server down! Trying restart - %s:%s  ' % (HOST_NAME, PORT_NUMBER))

        httpd.server_close()

        httpd.serve_forever()

        
    httpd.server_close()    

    writerLOG(logging_srv, path_to_log_lile, name_server_log, 'Server Stops - %s:%s  ' % (HOST_NAME, PORT_NUMBER))
