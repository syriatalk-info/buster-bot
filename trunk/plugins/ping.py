# -*- coding: utf-8 -*-

def ping_handler(t, s, p):
    if s[0].isdigit():
        reply(t, s, u'Команда работает только в сети Jabber')
        return
    jid = s[1]+'/'+s[2]
    if p:
        if s[1] in GROUPCHATS and p in GROUPCHATS[s[1]]:
            jid = s[1]+'/'+p
        else:
            jid = p
    packet = IQ(JAB, 'get')
    packet.addElement('query', 'jabber:iq:version')
    packet.addCallback(ping_result_handler, t, s, p, time.time())
    reactor.callFromThread(packet.send, jid)

def ping_result_handler(type, s, p, i, x):
    add=''
    ERROR={'400':u'Плохой запрос','401':u'Не авторизирован','402':u'Требуется оплата','403':u'Запрещено','404':u'Не найдено','405':u'Не разрешено','406':u'Не приемлемый','407':u'Требуется регистация','408':u'Время ожидания ответа вышло','409':u'Конфликт','500':u'Внутренняя ошибка сервера','501':u'Не реализовано','503':u'Сервис недоступен','504':u'Сервер удалил запрос по тайм-ауту'}
    if x['type'] == 'error':
        try: code = [c['code'] for c in x.children if (c.name=='error')]
        except: code = []
        if ' '.join(code) in ERROR: add=ERROR[' '.join(code)]
        reply(type, s, u'Не пингуется. '+' '.join(code)+' '+add)
        return
    elif x['type'] == 'result':
        t = time.time()
        rep = u'понг от '
	if p:
            rep += p
	else:
            rep += u'тебя'
	rep+=u' '+str(round(t-i, 3))+u' секунд'
        reply(type, s, rep)


def time_handler(t, s, p):
    jid = s[1]+'/'+s[2]
    if s[1] in GROUPCHATS and p:
        if p in GROUPCHATS[s[1]]:
            jid=s[1]+'/'+p
        else:
            jid=p
    packet = IQ(JAB, 'get')
    packet.addElement('query', 'jabber:iq:time')
    packet.addCallback(time_result_handler, t, s, p)
    reactor.callFromThread(packet.send, jid)

def time_result_handler(t, s, p, x):
    try:
        query = element2dict(x)['query']
        display = element2dict(query)['display']
        reply(t, s, display.children[0])
    except:
        reply(t, s, u'Невозможно определить время!')

def disco_handler(t, s, p):
    if p:
        if p.count(' '):
            n = p.split()
            p, grep = n[0], n[1]
        else:
            p, grep = p, ' '
        if not p.count('.'):
            p=p+'@conference.jabber.ru'
        packet = IQ(JAB, 'get')
        packet.addElement('query', 'http://jabber.org/protocol/disco#items')
        packet.addCallback(disco_result_handler_a, t, s, p, grep)
        reactor.callFromThread(packet.send, p)
    else: reply(t, s, u'и?')

def disco_result_handler_a(t, s, p, grep, x):
    if x['type'] == 'result':
        query = element2dict(x)['query']
        query = [i.attributes for i in query.children if i.__class__==domish.Element]
        if p.count('conference.') or p.count('chat.') or p.count('muc.'):
            if p.count('@'):
                r = [i.get('name') for i in query]
                r.sort()
            else:
                r = []
                for i in query:
                    try: g = re.search('^(.+)\(([0-9]+)\)$', i['name']).groups()
                    except: g = (i['name'], '0')
                    if int(g[1]) < 99: r.append((g[0], i['jid'], g[1]))
                r.sort(lambda x, y: cmp(int(y[2]), int(x[2])))
                r = ['%s - %s (%s)' % i for i in r]
        else:
            r = [i['jid'] for i in query]
            r.sort()
        if r: reply(t, s, u'Надискаверил:\n'+show_list(r, grep))
        else: reply(t, s, u'Пустое диско!')
    else: reply(t, s, u'Ошибка насяльника!')

def show_list(seq, grep=None, empty='[empty list]'):
 if len(seq) == 1: return seq[0]
 else:
  r = ''
  for i in range(len(seq)):
   r += '%s) %s\n' % (i+1, seq[i])
  if grep: r = '\n'.join([i for i in r.split('\n') if i.lower().count(grep.lower())])
  if not r: r = empty
  return r

register_command_handler(disco_handler, 'диско', ['все'], 0, 'Дискаверит конференцию или сервер.', 'диско чат', ['диско cool@conference.talkonaut.com'])
register_command_handler(time_handler, 'часики', ['все'], 0, 'часики', 'часики ник', ['часики вася'])
register_command_handler(ping_handler, 'пинг', ['все'], 0, 'пинг', 'пинг', ['пинг'])
