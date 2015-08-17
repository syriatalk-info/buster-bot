# -*- coding: utf-8 -*-

import datetime
import operator


NICKS_TIMER = 0
NICKS_FILE = 'dynamic/nicks_.txt'

db_file(NICKS_FILE, dict)


NICKS = eval(read_file(NICKS_FILE))

BAN_NEWBIE_FILE = 'dynamic/bannewbie.txt'

db_file(BAN_NEWBIE_FILE, dict)

BAN_NEWBIE = eval(read_file(BAN_NEWBIE_FILE))

def hnd_join_nicks(g, n, afl, role, cl):
        global NICKS
        global NICKS_TIMER
        global NICKS_FILE
        jid = get_true_jid(g+'/'+n)
        if not g in NICKS:
                NICKS[g]={}
        if not jid in NICKS[g]:
                NICKS[g][jid] = {'n':{},'t':time.time(),'m':0, 'last':0}
                hnd_ban_newbie(cl, g, jid)
        if not n in NICKS[g][jid]['n']:
                NICKS[g][jid]['n'][n] = {}
        NICKS[g][jid]['last']=time.time()
        if time.time() - NICKS_TIMER > 1200:
                NICKS_TIMER = time.time()
                write_file(NICKS_FILE, str(NICKS))

register_join_handler(hnd_join_nicks)


def get_muclast_list(muc):
        d = {}
        for x in NICKS[muc]:
                d[x]=NICKS[muc][x]['last']
        sorte = sorted(d.items(), key=operator.itemgetter(1))
        if len(sorte)>15:
                sorte = sorte[:15]
        return sorte

UMENU_BANLAST = {}

def hnd_banlastmuc(t, s, p):
        if not s[1] in GROUPCHATS:
                return
        global UMENU_BANLAST
        jid = get_true_jid(s)+s[1]
        rep = ''
        n = 0
        if not p:
                UMENU_BANLAST[jid] = {}
                list = get_muclast_list(s[1])
                for x in list:
                        n+=1
                        rep+=str(n)+') '+x[0]+'\n'
                        UMENU_BANLAST[jid][str(n)]=x[0]
                reply(t, s, rep+u'\nЧтобы забанить отправьте <банласт номер1 номер2 ..> без кавычек')
        else:
                ss = p.split()
                for x in ss:
                        if jid in UMENU_BANLAST.keys() and x in UMENU_BANLAST[jid].keys():
                                ban(s[3], s[1], UMENU_BANLAST[jid][x])
                                rep+=UMENU_BANLAST[jid][x]+'\n'
                reply(t, s, u'Зобайнел: '+(rep if not rep.isspace() else u'0'))
                
register_command_handler(hnd_banlastmuc, 'банласт', ['все'], 0, 'Бан последних пользователей', 'банласт', ['банласт'])                


def hnd_ban_newbie(cl, g, jid):
        if g in BAN_NEWBIE and time.time()-BAN_NEWBIE[g]<3600:
                ban(cl, g, jid)

def hnd_nnb_ban_set(t, s, p):
        if not s[1] in GROUPCHATS:
                return
        global BAN_NEWBIE
        if g in BAN_NEWBIE and time.time()-BAN_NEWBIE[g]<3600:
                del BAN_NEWBIE[g]
                reply(t, s, u'Отключил автобан!')
        else:
                BAN_NEWBIE[g]=time.time()
                reply(t, s, u'Включен автобан нубов на 1 час!')
        write_file(BAN_NEWBIE_FILE, str(BAN_NEWBIE))

register_command_handler(hnd_nnb_ban_set, 'бани нубов', ['все'], 0, 'Включает автобан пользователей ранее не бывших в чате, смотрит по базе жидов, ранг не важен', 'бани нубов', ['бани нубов'])


def hnd_lev_nicks(g, n, reason, code, cl):
        global NICKS
        global NICKS_TIMER
        global NICKS_FILE
        jid = get_true_jid(g+'/'+n)
        if not g in NICKS:
                NICKS[g]={}
        try:
                if not 'all' in NICKS[g][jid]:
                        NICKS[g][jid]['all']=0
                NICKS[g][jid]['all']+=time.time()-NICKS[g][jid]['last']
        except:
                pass

register_leave_handler(hnd_lev_nicks)               
                

def hnd_msg_nicks(st, t, s, p):
        global NICKS
        jid = get_true_jid(s)
        try:
                if jid in NICKS[s[1]]:
                        NICKS[s[1]][jid]['m']+=1
        except:
                pass

register_message_handler(hnd_msg_nicks)


def hnd_nicks_inf(t, s, p):
        if not s[1] in GROUPCHATS:
                return
        if p.lower() == u'я':
                p = s[2]
        if p.lower() == u'ты':
                reply(t, s, u'Я бот Бастер')
                return
        ishere = False
        rep = ''
        #if not p in GROUPCHATS[s[1]]:
        #        pass
        n = 0
        for x in NICKS[s[1]]:
                ishere = False
                if x.count('@conference.'):
                        continue
                if p in NICKS[s[1]][x]['n']:
                        if p in GROUPCHATS[s[1]] and GROUPCHATS[s[1]][p]['jid'].split('/')[0]==x and GROUPCHATS[s[1]][p]['ishere']:
                                ishere = True
                        n+=1
                        rep+=(str(n)+') ' if n>1 else u'Информация о ')+p+u':\nНики - '+', '.join(NICKS[s[1]][x]['n'].keys())+u'\nВпервые увидел: '+datetime.datetime.fromtimestamp(NICKS[s[1]][x]['t']).strftime('%Y-%m-%d')
                        rep+=u'\nСообщений - '+str(NICKS[s[1]][x]['m'])+u'\nПоследний раз видел: '+(datetime.datetime.fromtimestamp(NICKS[s[1]][x]['last']).strftime('%m-%d %H:%M:%S') if not ishere else u'Онлайн прямо сейчас')+'\n'
                        rep+=u'Всего провел времени в конфе - '+timeElapsed(NICKS[s[1]][x].get('all',0))+'\n'

        if rep.isspace() or n==0:
                return
        reply(t, s, (u'Совпадений в никах '+str(n)+'\n' if n>1 else '')+rep)

register_command_handler(hnd_nicks_inf, 'кто', ['все'], 0, 'Показывает информацию о нике.', 'кто <ник>', ['кто вася'])

def hnd_see_show(t, s, p):
        if not s[1] in GROUPCHATS: return
        n = 0
        rep = ''
        for x in NICKS[s[1]]:
                ishere = False
                if x.count('@conference.'):
                        continue
                if p in NICKS[s[1]][x]['n']:
                        if p in GROUPCHATS[s[1]] and GROUPCHATS[s[1]][p]['jid'].split('/')[0]==x and GROUPCHATS[s[1]][p]['ishere']:
                                ishere = True
                        n+=1
                        rep+=(str(n)+') ' if n>1 else '')+u'Последний раз видел '+p+': '+(datetime.datetime.fromtimestamp(NICKS[s[1]][x]['last']).strftime('%m-%d %H:%M:%S') if not ishere else u'Онлайн прямо сейчас')+'\n'
        rep+=u'Всего список JID-ов побывавших в конференции: '+str(len([x for x in NICKS[s[1]] if not x.count('@conference.')]))
        reply(t, s, (rep if n>0 else u'Совпадений нет!'))

register_command_handler(hnd_see_show, 'seen', ['все'], 0, 'Показывает информацию о последнем заходе юзера в чат.', 'seen <ник>', ['seen вася'])
	
