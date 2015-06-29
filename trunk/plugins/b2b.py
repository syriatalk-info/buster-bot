# -*- coding: utf-8 -*-

import ast

B2B = {}

B2B_STAT = {}

B2B_FILE = 'dynamic/b2b.txt'
B2B_WHERE_JOIN = 'dynamic/b2b_join.txt'

db_file(B2B_FILE, dict)
db_file(B2B_WHERE_JOIN, dict)

B2B_L = eval(read_file(B2B_WHERE_JOIN))

def b2b_send_iq_(cljid=None, jid=None, list=True):
    dic = {}
    more = []
    for x in GROUPCHATS.keys():
        dic[x]=get_bot_nick(x)
    dic['jid']=CLIENTS.keys()
    if not cljid or not jid: return
    if jid.split('/')[0] in CLIENTS.keys(): return
    
    iq = domish.Element(('jabber:client', 'iq'))
    iq['type'] = 'set'
    iq['id'] = str(random.randrange(1,9999))
    iq['to'] = jid
    query = iq.addElement('query', 'xmpp:iq:b2b')
    
    if list:
        if not jid in B2B_STAT.keys() or not B2B_STAT[jid]:
            try: more=[x for x in B2B[jid]['body']['jid'] if x != jid.split('/')[0]]
            except: pass
            B2B_STAT[jid]={'t':time.time(),'result':0, 'fail':0, 'more':more}
        else:
            B2B_STAT[jid]['t']=time.time()
        query.addContent(str(dic))
    
    reactor.callFromThread(dd, iq, CLIENTS[cljid])


def b2b_get_iq(iq, cljid):
    try:
        for x in B2B_STAT.keys():
            if time.time()-INFO['start']<300:
                break
            if time.time()-B2B_STAT[x]['result']>315 and time.time()-B2B_STAT[x]['t']>315:
                B2B_STAT[x]['fail']+=1
                if B2B_STAT[x]['more'] and len(B2B_STAT[x]['more'])<=B2B_STAT[x]['fail']:
                    new = B2B_STAT[x]['more'][B2B_STAT[x]['fail']-1]
                    b2b_send_iq_(cljid, new+'/'+x.split('/')[1], list=False)
                else:
                    db=eval(read_file(B2B_FILE))
                    #txt=eval(read_file(B2B_WHERE_JOIN))
                    B2B_L[x]={}
                    write_file(B2B_WHERE_JOIN, str(B2B_L))
                    for m in db[x].keys():
                        if m.count('@conference.') and not m in GROUPCHATS.keys():
                            hnd_join('privat',[cljid, cljid, cljid, cljid],m+' nick='+db[x][m])
                            time.sleep(5)
            else:
                if time.time()-B2B_STAT[x]['result']>300 and time.time()-B2B_STAT[x]['t']>300:
                    b2b_send_iq_(cljid, x, list=False)
    except: pass
    body = None
    global B2B
    if not iq:
        return
    if iq.getAttribute('type')!='set':
        return
    fromjid = iq.getAttribute('from')
    nsuri = iq.firstChildElement().uri
    if nsuri!= 'xmpp:iq:b2b': return
    try:
        if not fromjid in B2B_STAT.keys():
            return
        if fromjid in B2B_L:
            if fromjid in B2B:
                for k in B2B[fromjid].keys():
                    b2b_leave(k)
        body = [x for x in iq.children if not isinstance(x, basestring)][0].__dict__['children'][0]
        body = ast.literal_eval(body)
        for c in body.keys():
            if c in GROUPCHATS.keys():
                del body[c]
    except: pass
    B2B[fromjid]=body
    if not body:
        #Пришел запрос на список без "тела" шлем ответ
        b2b_send_iq_(cljid,fromjid)
    else:
        if fromjid in B2B_STAT.keys():
            B2B_STAT[fromjid]['result']=time.time()
            B2B_STAT[fromjid]['fail']=0
        write_file(B2B_FILE, str(B2B))


register_iq_handler(b2b_get_iq)


def hnd_b2b_init(*b):
    global B2B_STAT
    global B2B
    db=eval(read_file(B2B_FILE))
    B2B=db.copy()
    for x in db.keys():
        if not x in B2B_STAT.keys():
            B2B_STAT[x]={}

register_stage0_init(hnd_b2b_init)

def hnd_make_b2b(t, s, p):
    global B2B
    if not p:
        return
    if not p.count('/'):
        reply(t, s, u'JID нужно указывать с ресурсом учитывая верхний и нижний регистр!\nнапр. boteg@jabber.ru/JabberBot')
        return
    ss = p.split('/')[0]
    if ss.lower() in CLIENTS.keys():
        reply(t, s, u'Епанулся что-ли? Это мой JID!')
        return
    if p in B2B.keys():
        del B2B[p]
        write_file(B2B_FILE, str(B2B))
        reply(t, s, u'Удалил '+p)
        return
    reply(t, s, u'Отправляем запрос на '+p)
    if not p in B2B_STAT.keys():
        B2B_STAT[p]={}
    b2b_send_iq_(s[3], p, list=False)
    tt=time.time()
    while time.time()-tt<15:
        time.sleep(1)
        if p in B2B and B2B[p]:
            reply(t, s, u'Соединение успешно установленно!\nТеперь у '+p+u' я на подстраховке!\nСписок комнат:\n'+'\n'.join([x for x in B2B[p].keys() if x!='jid']))
            write_file(B2B_FILE, str(B2B))
            break
    else:
        reply(t, s, p+u' не отвечает на запрос!')

def b2b_leave(muc):
    file = 'dynamic/chatroom.list'
    db = eval(read_file(file))
    botjid = [x for x in db.keys() if hasattr(db[x], 'keys') and muc in db[x].keys()]
    if "JOIN_TIMER" in globals().keys() and muc in JOIN_TIMER.keys():
        del JOIN_TIMER[parameters]
    if muc in GROUPCHATS.keys():
        del GROUPCHATS[muc]
    if botjid:
        botjid = botjid[0]
        if muc in db[botjid].keys():
            del db[botjid][muc]
            write_file(file, str(db))
    leave(muc, '', botjid)

register_command_handler(hnd_make_b2b, 'подстрахуй', ['админ','мук','все'], 100, 'Команда может соединить несколько аналогичных ботов для подстраховки их работы. \nЕсли указанный в качестве параметра бот перестанет отвечать на запросы (упал VDS,отключили за неуплату и тд.), то тогда ваш бот его подменит зайдя в чаты.\nДля удаления JID-а повторно указываем его в качестве параметра', 'подстрахуй <jid/ресурс>', ['подстрахуй bot@jab.ua/JabberBot'])
