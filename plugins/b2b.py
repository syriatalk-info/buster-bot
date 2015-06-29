# -*- coding: utf-8 -*-

B2B = {}

B2B_FILE = 'dynamic/b2b.txt'

db_file(B2B_FILE, dict)

def b2b_send_iq_(cljid=None, jid=None, list=True):
    dic = {}
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
        query.addContent(str(dic))
    
    reactor.callFromThread(dd, iq, CLIENTS[cljid])


def b2b_get_iq(iq, cljid):
    body = None
    global B2B
    if not iq:
        return
    if iq.getAttribute('type')!='set':
        return
    fromjid = iq.getAttribute('from')
    nsuri = iq.firstChildElement().uri
    if nsuri!= 'xmpp:iq:b2b': return
    try: body = [x for x in iq.children if not isinstance(x, basestring)][0].__dict__['children'][0]#element2dict(iq).get('query',None)#iq.firstChildElement()#(None if not hasattr(el,'children') else el.children)
    except: pass
    B2B[fromjid]={'t':time.time(),'body':body}
    if not body:
        #Пришел запрос на список без "тела" шлем ответ
        b2b_send_iq_(cljid,fromjid)
    else:
        pass


register_iq_handler(b2b_get_iq)


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
    reply(t, s, u'Отправляем запрос на '+p)
    b2b_send_iq_(s[3], p, list=False)
    tt=time.time()
    while time.time()-tt<15:
        time.sleep(1)
        if p in B2B and time.time()-B2B[p]['t']<300 and B2B[p]['body']:
            reply(t, s, u'Соединение успешно установленно!\nТеперь у '+p+u' я на подстраховке!\nСписок комнат:'+'\n'.join([x for x in B2B[p]['body'].keys() if x!='jid']))
            break

register_command_handler(hnd_make_b2b, 'подстрахуй', ['админ','мук','все'], 100, 'Команда может соединить несколько аналогичных ботов для подстраховки их работы. \nЕсли указанный в качестве параметра бот перестанет отвечать на запросы (упал VDS,отключили за неуплату и тд.), то тогда ваш бот его подменит зайдя в чаты.', 'подстрахуй <jid/ресурс>', ['подстрахуй bot@jab.ua/JabberBot'])
