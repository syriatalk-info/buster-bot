# -*- coding: utf-8 -*-

WHO_JOIN = {}

def hnd_who_join(type, source, parameters):
    global WHO_JOIN
    if not source[1] in GROUPCHATS:
        return
    day=time.localtime()[2]
    if not day in WHO_JOIN:
        reply(type, source, u'Нет статистики')
        return
    if not source[1] in WHO_JOIN[day]:
        reply(type, source, u'Нет статистики')
        return
    rep=''
    for x in WHO_JOIN[day][source[1]]:
        s=') '
        if len(WHO_JOIN[day][source[1]])>1:
            s=') ,'
        rep+=x[:20]+' ('+str(WHO_JOIN[day][source[1]][x])+s
    if not rep or rep.isspace():
        reply(type, source, u'Нет статистики!')
        return
    if len(rep)>3000:
        rep=rep[:3000]+'>>>'
    if type!='chat':
        reply(type, source, u'Смотри в привате!')
    reply('chat', source, rep)
        

def hnd_stat_l(g, n, a, b):
    global WHO_JOIN
    if not g in GROUPCHATS:
        return
    day=time.localtime()[2]
    if not day in WHO_JOIN:
        WHO_JOIN[day]={}
    if not g in WHO_JOIN[day]:
        WHO_JOIN[day][g]={}
    WHO_JOIN[day][g][n]=time.ctime().split()[3]

register_leave_handler(hnd_stat_l)
register_command_handler(hnd_who_join, 'хтобыл', ['все'], 0, 'Статистика конференции', 'хтобыл', ['хтобыл'])

        
    
