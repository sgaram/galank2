from SLACKBOT import *
from GALANK.ttypes import *
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup
from multiprocessing import Pool, Process
from humanfriendly import format_timespan, format_size, format_number, format_length
import time, random, asyncio, timeit, sys, json, codecs, threading, glob, re, string, os, requests, subprocess, six, urllib, urllib.parse, ast, pafy, youtube_dl
botStart = time.time()

# MID ADMIN JANGAN DI HAPUS
# HARGAI YANG BIKIN
# TAMBAHIN AJA MID KALIAN
# THANKS YA BUAT KALIAN
# KALAU BUKAN SUPPORT DARI KALIAN
# AKU GAK MUNGKIN KEK GINI/PASTI UDAH VAKUM BOT
# YANG MAU KEPO,IN[ADD AJA ID LINE DI BAWAH]
# DAN MAU NANYA SEKITAR TENTANG BOT
# [ADD ME]http://line.me/ti/p/%40ryp6149l

Galank = LineClient(authToken='TOKENMU SAYANG')
Galank.log("Auth Token : " + str(Galank.authToken))
channel = LineChannel(Galank)
Galank.log("Channel Access Token : " + str(channel.channelAccessToken))
#======================
Galank1 = LineClient(authToken='TOKENMU SAYANG')
Galank1.log("Auth Token : " + str(Galank1.authToken))
#======================
Galank2 = LineClient(authToken='TOKENMU SAYANG')
Galank2.log("Auth Token : " + str(Galank2.authToken))
#======================
settingsOpen = codecs.open("slackbot.json","r","utf-8")
poll = LinePoll(Galank)
clientProfile = Galank.getProfile()
clientSettings = Galank.getSettings()
mid = Galank.profile.mid
call = LineCall(Galank)
Amid = Galank1.getProfile().mid
Bmid = Galank2.getProfile().mid
KAC = [Galank,Galank1,Galank2]
Bots = [mid,Amid,Bmid]
pnharfbot = []
linkprotect = []
cancelprotect = {}
PROTECT = {}
settings = json.load(settingsOpen)
if settings["restartPoint"] != None:
    Galank.sendText(settings["restartPoint"], "Bot kembali aktif")
switch = {
    'winvite':False,
    'dinvite':False,
    'wblacklist':False,
    'dblacklist':False,
    'wpeki':False,
    'dpeki':False,
    'cp1':False,
    'cp2':False,
    'changePicture':False
}

myProfile = {
	"displayName": "",
	"statusMessage": "",
	"pictureStatus": ""
}
myProfile1 = {
	"displayName1": "",
	"statusMessage1": "",
	"pictureStatus1": ""
}
myProfile2 = {
	"displayName2": "",
	"statusMessage2": "",
	"pictureStatus2": ""
}
myProfile["displayName"] = clientProfile.displayName
myProfile["statusMessage"] = clientProfile.statusMessage
myProfile["pictureStatus"] = clientProfile.pictureStatus
myProfile1["displayName1"] = clientProfile.displayName
myProfile1["statusMessage1"] = clientProfile.statusMessage
myProfile1["pictureStatus1"] = clientProfile.pictureStatus
myProfile2["displayName2"] = clientProfile.displayName
myProfile2["statusMessage2"] = clientProfile.statusMessage
myProfile2["pictureStatus2"] = clientProfile.pictureStatus
def restartBot():
    print ("[ INFO ] BOT RESETTED")
    python = sys.executable
    os.execl(python, python, *sys.argv)
def autoRestart():
    if time.time() - botStart > int(settings["timeRestart"]):
        backupData()
        time.sleep(5)
        restartBot()
def logError(text):
    Galank.log("[ ERROR ] " + str(text))
    time = datetime.now()
def waktu(secs):
    mins, secs = divmod(secs,60)
    hours, mins = divmod(mins,60)
    return '%02d Jam %02d Menit %02d Detik' % (hours, mins, secs)
def download_page(url):
    try:
        headers = {}
        headers['User-Agent'] = random.choice(settings["userAgent"])
        req = urllib.request.Request(url, headers = headers)
        resp = urllib.request.urlopen(req)
        respData = str(resp.read())
        return respData
    except Exception as e:
        logError(e)
def _images_get_next_item(s):
    start_line = s.find('rg_di')
    if start_line == -1:    #If no links are found then give an error!
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        start_line = s.find('"class="rg_meta"')
        start_content = s.find('"ou"',start_line+70)
        end_content = s.find(',"ow"',start_content-70)
        content_raw = str(s[start_content+6:end_content-1])
        return content_raw, end_content
#Getting all links with the help of '_images_get_next_image'
def _images_get_all_items(page):
    items = []
    while True:
        item, end_content = _images_get_next_item(page)
        if item == "no_links":
            break
        else:
            items.append(item)      #Append all the links in the list named 'Links'
            page = page[end_content:]
    return items
def mentionMembers(to, mid):
    try:
        arrData = ""
        textx = "[Mention {} User]\n".format(str(len(mid)))
        arr = []
        no = 1
        for i in mid:
            mention = "@x\n"
            slen = str(len(textx))
            elen = str(len(textx) + len(mention) - 1)
            arrData = {'S':slen, 'E':elen, 'M':i}
            arr.append(arrData)
            textx += mention
            if no < len(mid):
                no += 1
                textx += "? "
            else:
                try:
                    no = "╭═══╬╬═══╮[ {} ]╰═══╬╬═══╯".format(str(Galank.getGroup(to).name))
                except:
                    no = "╭═══╬╬═══╮[ Success ]╰═══╬╬═══╯"
        Galank.sendMessage(to, textx, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
    except Exception as error:
        logError(error)
        Galank.sendMessage(to, "[ INFO ] Error :\n" + str(error))
def backupData():
    try:
        backup = settings
        f = codecs.open('slackbot.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        return True
    except Exception as error:
        logError(error)
        return False
def help():
    helpMessage = "╭══════╬╬═══════╮\n●TΣΔM SLΔCҜβΩT●\n╰══════╬╬═══════╯\n╭══════╬╬═══════╮" + "\n" + \
                  "╠➣ NAME IN BOT " + clientProfile.displayName + " " + "\n" + \
                  "╠➣ Help" + "\n" + \
                  "╠➣ Settings" + "\n" + \
                  "╠➣ Me" + "\n" + \
                  "╠➣ Add" + "\n" + \
                  "╠➣ Creator" + "\n" + \
                  "╠➣ Gcreator" + "\n" + \
                  "╠➣ Speed" + "\n" + \
                  "╠➣ Responame" + "\n" + \
                  "╠➣ Tagall" + "\n" + \
                  "╠➣ Bot" + "\n" + \
                  "╠➣ Youtubemp4 *txt" + "\n" + \
                  "╠➣ Youtubemp3 *txt" + "\n" + \
                  "╠➣ Mybot" + "\n" + \
                  "╠➣ Spamcall" + "\n" + \
                  "╠➣ Clearban" + "\n" + \
                  "╠➣ Removechat" + "\n" + \
                  "╠➣ Setmypict" + "\n" + \
                  "╠➣ Setpict1" + "\n" + \
                  "╠➣ Setpict2" + "\n" + \
                  "╠➣ Setpictgroup" + "\n" + \
                  "╠➣ Restart" + "\n" + \
                  "╠➣ Crash" + "\n" + \
                  "╠══════════════" + "\n" + \
                  "╠➣ Kiss1 @" + "\n" + \
                  "╠➣ Kiss2 @" + "\n" + \
                  "╠➣ Kiss name @" + "\n" + \
                  "╠➣ Perkosa" + "\n" + \
                  "╠➣ Perkosaban" + "\n" + \
                  "╠➣ MyHeart" + "\n" + \
                  "╠➣ Mayhem" + "\n" + \
                  "╠➣ Masuk" + "\n" + \
                  "╠➣ Pamit" + "\n" + \
                  "╠➣ Reinvite" + "\n" + \
                  "╠➣ Leaveto *gid" + "\n" + \
                  "╠══════════════" + "\n" + \
                  "╠➣ Banned on" + "\n" + \
                  "╠➣ Unbanned on" + "\n" + \
                  "╠➣ Unbanned @" + "\n" + \
                  "╠➣ Banned @" + "\n" + \
                  "╠➣ Kick@ban" + "\n" + \
                  "╠➣ Banlist" + "\n" + \
                  "╠➣ Clearban" + "\n" + \
                  "╠══════════════" + "\n" + \
                  "╠➣ Protectlink on|off" + "\n" + \
                  "╠➣ Protectinvite on|off" + "\n" + \
                  "╠➣ Protect on|off" + "\n" + \
                  "╠➣ Namelock on|off" + "\n" + \
                  "╰══════╬╬═══════╯\nCREATOR:\nline.me/ti/p/~fuck.you__"
    return helpMessage
groupParam = ""
def SiriGetOut(targ):
    Galank.kickoutFromGroup(groupParam,[targ])
    Galank1.kickoutFromGroup(groupParam,[targ])
    Galank2.kickoutFromGroup(groupParam,[targ])
def byuh(targ):
    random.choice(KAC).kickoutFromGroup(groupParam,[targ])
def bot(op):
    global time
    global ast
    global groupParam
    try:
#-----------------------------------------------
        if op.type == 11:
            if op.param3 == '1':
                if op.param1 in settings['pname']:
                    try:
                        G = Galank.getGroup(op.param1)
                    except:
                        try:
                            G = Galank1.getGroup(op.param1)
                        except:
                            try:
                                G = Galank2.getGroup(op.param1)
                            except:
                                pass
                    G.name = settings['pro_name'][op.param1]
                    try:
                        Galank.updateGroup(G)
                    except:
                        try:
                            Galank1.updateGroup(G)
                        except:
                            try:
                                Galank2.updateGroup(G)
                            except:
                                pass
                    if op.param2 in Bots:
                        pass
                    elif op.param2 not in Bots:
                        pass
                    else:
                        try:
                            Galank1.kickoutFromGroup(op.param1,[op.param2])
                        except:
                            try:
                                Galank2.kickoutFromGroup(op.param1,[op.param2])
                            except:
                                pass
        if op.type == 25:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            # Check if in group chat or personal chat
            if msg.toType == 0 or msg.toType == 2:
                if msg.toType == 0:
                    to = receiver
                elif msg.toType == 2:
                    to = receiver
                if msg.contentType == 13:
                   if switch["wblacklist"] == True:
                       if msg.contentMetadata["mid"] in settings["blacklist"]:
                            Galank.sendText(to,"Succes add to blacklist")
                            switch["wblacklist"] = False
                       else:
                            settings["blacklist"][msg.contentMetadata["mid"]] = True
                            switch["wblacklist"] = False
                            Galank.sendText(to,"contact blacklist di tambahkan")
                            print([msg.contentMetadata["mid"]] + " ADD TO BLACKLIST")
                   elif switch["dblacklist"] == True:
                       if msg.contentMetadata["mid"] in settings["blacklist"]:
                            del settings["blacklist"][msg.contentMetadata["mid"]]
                            Galank.sendText(to,"Succes you whitelist")
                            switch["dblacklist"] = False
                            print([msg.contentMetadata["mid"]] + " ADD TO WHITELIST")
                       else:
                            switch["dblacklist"] = False
                            Galank.sendText(to,"not is blacklist")
                if msg.contentType == 0:
                    if text is None:
                        return
                    else:
                        if text.lower() == 'speed':
                            start = time.time()
                            elapsed_time = time.time() - start
                            Galank.sendText(to,"════SPEED BOTS═══\n" + "%seconds" % (elapsed_time) + "\n════●SLΔCҜβΩT●═══")
                            Galank1.sendText(to,"════SPEED BOTS═══\n" + "%seconds" % (elapsed_time) + "\n════●SLΔCҜβΩT●═══")
                            Galank2.sendText(to,"════SPEED BOTS═══\n" + "%seconds" % (elapsed_time) + "\n════●SLΔCҜβΩT●═══")
                        if text.lower() == "help":
                            helpMessage = help()
                            Galank.sendText(to, str(helpMessage))
                        elif text.lower() == 'tagall':
                            group = Galank.getGroup(msg.to)
                            k = len(group.members)//100
                            for j in range(k+1):
                                aa = []
                                for x in group.members:
                                    aa.append(x.mid)
                                try:
                                    arrData = ""
                                    textx = "╭═══╬╬═══╮[ Mention {} Members ]╰═══╬╬═══╯\n➠1 - ".format(str(len(aa)))
                                    arr = []
                                    no = 1
                                    b = 1
                                    for i in aa:
                                        b = b + 1
                                        end = "\n"
                                        mention = "@x\n"
                                        slen = str(len(textx))
                                        elen = str(len(textx) + len(mention) - 1)
                                        arrData = {'S':slen, 'E':elen, 'M':i}
                                        arr.append(arrData)
                                        textx += mention
                                        if no < len(aa):
                                            no += 1
                                            textx += str(b) + " - "
                                        else:
                                            try:
                                                no = "[ {} ]".format(str(Galank.getGroup(msg.to).name))

                                            except:
                                               no = "╭═══╬╬═══╮[ Success ]╰═══╬╬═══╯"
                                    msg.to = msg.to
                                    msg.text = textx
                                    msg.contentMetadata = {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}
                                    msg.contentType = 0
                                    Galank.sendMessage1(msg)
                                except Exception as e:
                                    Galank.sendText(msg.to,str(e))
                        elif text.lower() == 'bot':
                            group = Galank1.getGroup(msg.to)
                            k = len(group.members)//100
                            for j in range(k+1):
                                aa = []
                                for x in group.members:
                                    aa.append(x.mid)
                                try:
                                    arrData = ""
                                    textx = "     [ Mention {} Members ]    \n1 - ".format(str(len(aa)))
                                    arr = []
                                    no = 1
                                    b = 1
                                    for i in aa:
                                        b = b + 1
                                        end = "\n"
                                        mention = "@x\n"
                                        slen = str(len(textx))
                                        elen = str(len(textx) + len(mention) - 1)
                                        arrData = {'S':slen, 'E':elen, 'M':i}
                                        arr.append(arrData)
                                        textx += mention
                                        if no < len(aa):
                                            no += 1
                                            textx += str(b) + " - "
                                        else:
                                            try:
                                                no = "[ {} ]".format(str(Galank1.getGroup(msg.to).name))

                                            except:
                                               no = "[ Success ]"
                                    msg.to = msg.to
                                    msg.text = textx
                                    msg.contentMetadata = {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}
                                    msg.contentType = 0
                                    Galank1.sendMessage1(msg)
                                except Exception as e:
                                    Galank1.sendText(msg.to,str(e))
                        elif text.lower() == 'me':
                            Galank.sendContact(to, sender)
                        elif text.lower() == 'add':		
                            Galank.sendText(to,"╠══════════════")
                            Galank.sendContact(to, 'u78643d09e42a36836a17cc918963a8b7')# GALANK
                            Galank.sendContact(to, 'u290d3072b043ff4796a9a91f145931e0')# INNE
                            Galank.sendContact(to, 'uf8d981e0bc9184560956ced35c4372be')# RIANDO
                            Galank.sendText(to,"╠══════════════")
                        elif text.lower() == 'creator':		
                            Galank.sendText(to,"╠══════════════")
                            Galank.sendContact(to, 'u78643d09e42a36836a17cc918963a8b7')
                            Galank.sendText(to,"╠══════════════")
                        elif 'kiss1 ' in text.lower():
                           ulti0 = msg.text.replace("kiss1 ","")
                           ulti1 = ulti0.lstrip()
                           ulti2 = ulti1.replace("@","")
                           ulti3 = ulti2.rstrip()
                           _name = ulti3
                           gs = Galank.getGroup(msg.to)
                           ginfo = Galank.getGroup(msg.to)
                           gs.preventedJoinByTicket = False
                           Galank.updateGroup(gs)
                           invsend = 0
                           Ticket = Galank.reissueGroupTicket(msg.to)
                           Galank1.acceptGroupInvitationByTicket(msg.to,Ticket)
                           time.sleep(0.2)
                           targets = []
                           for s in gs.members:
                               if _name in s.displayName:
                                  targets.append(s.mid)
                           if targets == []:
                           	sendMessage(to,"user does not exist")
                           else:
                               for target in targets:
                                    try:
                                        Galank1.kickoutFromGroup(msg.to,[target])
                                        print((msg.to,[g.mid]))
                                    except:
                                        Galank1.leaveGroup(msg.to)
                                        gs = Galank.getGroup(msg.to)
                                        gs.preventedJoinByTicket = True
                                        Galank.updateGroup(gs)
                                        gs.preventedJoinByTicket(gs)
                                        Galank.updateGroup(gs)
                        elif 'kiss2 ' in text.lower():
                           ulti0 = msg.text.replace("kiss2 ","")
                           ulti1 = ulti0.lstrip()
                           ulti2 = ulti1.replace("@","")
                           ulti3 = ulti2.rstrip()
                           _name = ulti3
                           gs = Galank.getGroup(msg.to)
                           ginfo = Galank.getGroup(msg.to)
                           gs.preventedJoinByTicket = False
                           Galank.updateGroup(gs)
                           invsend = 0
                           Ticket = Galank.reissueGroupTicket(msg.to)
                           Galank2.acceptGroupInvitationByTicket(msg.to,Ticket)
                           time.sleep(0.2)
                           targets = []
                           for s in gs.members:
                               if _name in s.displayName:
                                  targets.append(s.mid)
                           if targets == []:
                           	sendMessage(to,"user does not exist")
                           else:
                               for target in targets:
                                    try:
                                        Galank2.kickoutFromGroup(msg.to,[target])
                                        print((msg.to,[g.mid]))
                                    except:
                                        Galank2.leaveGroup(msg.to)
                                        gs = Galank.getGroup(msg.to)
                                        gs.preventedJoinByTicket = True
                                        Galank.updateGroup(gs)
                                        gs.preventedJoinByTicket(gs)
                                        Galank.updateGroup(gs)
                        elif text.lower() == 'mayhem':
                            if msg.toType == 2:
                                gs = Galank.getGroup(msg.to)
                                gs = Galank1.getGroup(msg.to)
                                gs = Galank2.getGroup(msg.to)
                                targets = []
                                for g in gs.members:
                                    targets.append(g.mid)
                                targets.remove(mid)
                                if targets == []:
                                    Galank.sendText(msg.to,"kayak nya limit")
                                else:
                                    for target in targets:
                                      if target not in Bots:
                                        try:
                                            klist=[Galank,Galank1,Galank2]
                                            kicker=random.choice(klist)
                                            kicker.kickoutFromGroup(msg.to,[target])
                                            print (msg.to,[g.mid])
                                        except:
                                           pass
                        elif text.lower() == 'myheart':
                            if msg.toType == 2:
                                gs = Galank.getGroup(msg.to)
                                gs.preventedJoinByTicket = False
                                Galank.updateGroup(gs)
                                invsend = 0
                                Ticket = Galank.reissueGroupTicket(msg.to)
                                Galank1.acceptGroupInvitationByTicket(msg.to,Ticket)
                                Galank2.acceptGroupInvitationByTicket(msg.to,Ticket)
                                time.sleep(0.1)
                                targets = []
                                for g in gs.members:
                                    targets.append(g.mid)
                                targets.remove(mid)
                                if targets == []:
                                    Galank.sendText(msg.to,"KICK OUT BYE ●SLΔCҜβΩT●")
                                else:
                                    for target in targets:
                                      if target not in Bots:
                                        try:
                                            klist=[Galank,Galank1,Galank2]
                                            kicker=random.choice(klist)
                                            kicker.kickoutFromGroup(msg.to,[target])
                                            print (msg.to,[g.mid])
                                        except:
                                           pass
                        elif text.lower() == 'masuk':
                            G = Galank.getGroup(msg.to)
                            ginfo = Galank.getGroup(msg.to)
                            G.preventedJoinByTicket = False
                            Galank.updateGroup(G)
                            invsend = 0
                            Ti = Galank.reissueGroupTicket(msg.to)
                            Galank1.acceptGroupInvitationByTicket(to,Ti)
                            Galank2.acceptGroupInvitationByTicket(to,Ti)
                            G = Galank.getGroup(msg.to)
                            G.preventedJoinByTicket = True
                            G.preventedJoinByTicket(G)
                            Galank.updateGroup(G)
                        elif text.lower() == 'pamit':
                            Galank1.leaveGroup(msg.to)
                            Galank2.leaveGroup(msg.to)
                        elif text.lower() == 'reinvite':
                            Galank1.leaveGroup(msg.to)
                            Galank2.leaveGroup(msg.to)
                            G = Galank.getGroup(msg.to)
                            ginfo = Galank.getGroup(msg.to)
                            G.preventedJoinByTicket = False
                            Galank.updateGroup(G)
                            invsend = 0
                            Ti = Galank.reissueGroupTicket(msg.to)
                            Galank1.acceptGroupInvitationByTicket(to,Ti)
                            Galank2.acceptGroupInvitationByTicket(to,Ti)
                            G = Galank.getGroup(msg.to)
                            G.preventedJoinByTicket = True
                            G.preventedJoinByTicket(G)
                            Galank.updateGroup(G)
                        elif text.lower() == 'perkosa':
                            gs = Galank.getGroup(msg.to)
                            gs = Galank1.getGroup(msg.to)
                            gs = Galank2.getGroup(msg.to)
                            sirilist = [i.mid for i in gs.members if any(word in i.displayName for word in ["Doctor.A","Eliza","Parry","Rakko","しりちゃん","0","1","2","3","4","5","6","7","8","9"])]
                            if sirilist != []:
                                groupParam = msg.to
                                try:
                                    p = Pool(40)
                                    p.map(SiriGetOut,sirilist)
                                    p.close()
                                except:
                                    p.close()
                        elif text.lower() == 'kiss name ':
                                key = eval(msg.contentMetadata["MENTION"])
                                key["MENTIONEES"][0]["M"]
                                targets = []
                                for x in key["MENTIONEES"]:
                                    targets.append(x["M"])
                                for target in targets:
                                   groupParam = msg.to
                                   try:
                                       p = Pool(40)
                                       p.map(byuh,targets)
                                       p.close()
                                       p.terminate()
                                       p.join
                                   except Exception as error:
                                       p.close()
                                       return
                        elif 'leaveto ' in text.lower():
                            gids = msg.text.replace('leaveto ',"")
                            gid = Galank.getGroup(gids)
                            try:
                                Galank1.leaveGroup(gids)
                                Galank2.leaveGroup(gids)
                            except:
                                Galank1.sendText(to,"Succes leave to group " + gids.name)
                                Galank2.sendText(to,"Succes leave to group " + gids.name)
                        elif text.lower() == 'mybot':		
                            Galank.sendContact(to, Amid)
                            Galank.sendContact(to, Bmid)
                        elif text.lower() == 'spamcall':
                            if msg.toType == 2:
                                group = Galank.getGroup(to)
                                members = [mem.mid for mem in group.members]
                                call.acquireGroupCallRoute(to)
                                call.inviteIntoGroupCall(to, contactIds=members)
                                Galank.sendText(to, "Success melakukan panggilan group")
                        elif text.lower() == 'removechat':
                            Galank.removeAllMessages(op.param2)
                            Galank1.removeAllMessages(op.param2)
                            Galank2.removeAllMessages(op.param2)
                            Galank.sendText(to, "Delete chat succes bossQ")
                        elif 'youtubemp3 ' in text.lower():
                            try:
                                Galank.sendText(msg.to,"Waitting progress...")
                                textToSearch = (msg.text).replace('youtubemp3 ', "").strip()
                                query = urllib.parse.quote(textToSearch)
                                url = "https://www.youtube.com/results?search_query=" + query
                                response = urllib.request.urlopen(url)
                                html = response.read()
                                soup = BeautifulSoup(html, "html.parser")
                                results = soup.find(attrs={'class':'yt-uix-tile-link'})
                                dl = 'https://www.youtube.com' + results['href']
                                vid = pafy.new(dl)
                                stream = vid.audiostreams
                                for s in stream:
                                    start = timeit.timeit()
                                    vin = s.url
                                    img = vid.bigthumbhd
                                    hasil = vid.title
                                    hasil += '\n\nDi upload oleh ✍️ ' +str(vid.author)
                                    hasil += '\nDurasi ⏱️ ' +str(vid.duration)+ ' (' +s.quality+ ') '
                                    hasil += '\nDi Like sebanyak👍 ' +str(vid.rating)
                                    hasil += '\nDi tonton sebanyak 👬 ' +str(vid.viewcount)+ 'x '
                                    hasil += '\nDi upload pada 📆 ' +vid.published
                                    hasil += '\n\nWaktunya⏲️ %s' % (start)
                                    hasil += '\n\n Waitting proses mp3....'
                                Galank.sendAudioWithURL(msg.to,vin)
                                Galank.sendImageWithURL(msg.to,img)
                                Galank.sendText(msg.to,hasil)
                            except:
                                Galank.sendText(msg.to,"Gagal Mencari...")
                        elif 'youtubemp4 ' in text.lower():
                            try:
                                Galank.sendText(msg.to,"Waitting progress..")
                                textToSearch = (msg.text).replace('youtubemp4 ', "").strip()
                                query = urllib.parse.quote(textToSearch)
                                url = "https://www.youtube.com/results?search_query=" + query
                                response = urllib.request.urlopen(url)
                                html = response.read()
                                soup = BeautifulSoup(html, "html.parser")
                                results = soup.find(attrs={'class':'yt-uix-tile-link'})
                                dl = 'https://www.youtube.com' + results['href']
                                vid = pafy.new(dl)
                                stream = vid.streams
                                for s in stream:
                                    vin = s.url
                                    hasil = '● Informasi ●\n\n'
                                    hasil += '★Judul video★\n ' + vid.title
                                    hasil += '\n Tunggu loading selesai...'
                                Galank.sendVideoWithURL(msg.to,vin)
                                Galank.sendText(msg.to,hasil)
                                print("[Notif] Search Youtube Success")
                            except:
                                Galank.sendText(msg.to,"Gagal")
#=====COMMEND SETTINGS=======
                        elif text.lower() == 'banned on':
                            switch["wblacklist"] = True
                            Galank.sendText(to,"Send contact")
                        elif text.lower() == 'unbanned on':
                            switch["dblacklist"] = True
                            Galank.sendText(to,"Send contact")
                        elif text.lower() == 'clearban':
                            settings["blacklist"] = {}
                            Galank.sendText(to,"BLACKLIST ALL DELETED")
                        elif 'unbanned ' in text.lower():
                            if 'MENTION' in msg.contentMetadata.keys()!= None:
                                names = re.findall(r'@(\w+)', text)
                                mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                mentionees = mention['MENTIONEES']
                                lists = []
                                for mention in mentionees:
                                    if mention["M"] not in lists:
                                        lists.append(mention["M"])
                                for ls in lists:
                                    try:
                                        del settings["blacklist"][ls]
                                        Galank.sendText(to,"Done bossQ")
                                    except:
                                        Galank.sendText(to,"Error")
                        elif text.lower() == 'kickdia':
                            group = Galank.getGroup(msg.to)
                            gMembMids = [contact.mid for contact in group.members]
                            matched_list = []
                            for tag in wait["blacklist"]:
                                matched_list+=filter(lambda str: str == tag, gMembMids)
                            if matched_list == []:
                                Galank.sendText(to,"Tak ada yang berdosa")
                                return
                            for jj in matched_list:
                                try:
                                    random.choice(KAC).kickoutFromGroup(to,[jj])
                                    print((to,[jj]))
                                except:
                                    pass
                        elif text.lower() == 'crash':
                            Galank.sendContact(to, "'xxx")
                            Galank.sendText(to,"JANGAN MASUK GRUP INI KALO GAK KUAT")  
                        elif 'banned ' in text.lower():
                            if 'MENTION' in msg.contentMetadata.keys()!= None:
                                names = re.findall(r'@(\w+)', text)
                                mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                                mentionees = mention['MENTIONEES']
                                lists = []
                                for mention in mentionees:
                                    if mention["M"] not in lists:
                                        lists.append(mention["M"])
                                for ls in lists:
                                    try:
                                        settings["blacklist"][ls] = True
                                        Galank.sendText(to,"â¨ï¸TARGET BLACKLIST DI TAMBAHKANâ¨ï¸")
                                    except:
                                        Galank.sendText(to,"Error")
                        elif text.lower() == 'banlist':
                                if settings["blacklist"] == {}:
                                    Galank.sendText(to,"Noting blacklist...")
                                else:
                                    Galank.sendText(to,"Prossesing..")
                                    mc = "â ï¸ DAFTAR BLACKLIST â ï¸ \n\n"
                                    for mi_d in settings["blacklist"]:
                                        mc += "ð¤  " +Galank.getContact(mi_d).displayName + "\n"
                                    Galank.sendText(to,mc)
#=================+
                        elif text.lower() == 'gcreator':
                            try:
                                group = Galank.getGroup(msg.to)
                                GS = group.creator.mid
                                Galank.sendContact(to, GS)
                                Galank.sendText(msg.to,"PEMBUAT GRUP INI") 
                            except:
                                W = group.members[0].mid
                                Galank.sendContact(to, W)
                                Galank.sendText(msg.to,"PEMBUAT GRUP INI") 

#======PROTECT======#
                        elif text.lower() == 'protectlink on':
                                settings["linkprotect"][msg.to] = True
                                Galank.sendText(to,"GROUP QR ALREADY BLOCKED")
                                print("[PROTECT QR DI AKTIFKAN]")
                        elif text.lower() == 'protectlink off':
                                try:
                                    del settings["linkprotect"][msg.to]
                                    Galank.sendText(to,"QR CODE ALREADY UNBLOCKED")
                                except:
                                    Galank.sendText(to,"QR CODE DONE UNBLOCKED")
                                    print("[PROTECT QR DIMATIKAN]")
                        elif text.lower() == 'namelock on':
                            if msg.to in settings['pname']:
                                Galank.sendText(to,"GROUP NAME ALREADY BLOCKED")
                            else:
                                Galank.sendText(to,"GROUP NAME HAS BEN BLOCKED")
                                settings['pname'][msg.to] = True
                                settings['pro_name'][msg.to] = Galank.getGroup(msg.to).name
                        elif text.lower() == 'namelock off':
                            if msg.to in settings['pname']:
                                Galank.sendText(to,"GROUP NAME ALREADY UNBLOCKED")
                                del settings['pname'][msg.to]
                            else:
                                Galank.sendText(to,"GROUP NAME HAS BEN UNBLOCKED")          
                        elif text.lower() == 'protectinvite on':
                                settings["cancelprotect"][msg.to] = True
                                Galank.sendText(to,"GROUP INVITE ALREADY BLOCKED")
                                print("[PROTECT INVITE DI AKTIFKAN]")
                        elif text.lower() == 'protectinvite off':
                                try:
                                    del settings["cancelprotect"][msg.to]
                                    Galank.sendText(to,"GROUP INVITE ALREADY UNBLOCKED")
                                except:
                                    Galank.sendText(to,"GROUP INVITE HAS BEN UNBLOCKED")
                                    print("[PROTECT INVITE DIMATIKAN]")
                        elif text.lower() == 'protect on':
                             try:
                                settings["PROTECT"][msg.to] = True
                                Galank.sendText(to,"BLOCKED MEMBER ALREADY ACTIVE")
                                print("[Perintah]block kick")
                             except:
                                Galank.sendText(to,"BLOCKED MEMBER HAS BEN ACTIVE")
                        elif text.lower() == 'protect off':
                                try:
                                    del settings["PROTECT"][msg.to]
                                    Galank.sendText(to,"ALREADY UNBLOCKED MEMBER")
                                except:
                                    Galank.sendText(to,"BLOCKED MEMBER HAS BEN NON ACTIVE")
                                    print("[Perintah]Allow kick")
                        elif text.lower() == 'settings':
                                 md = "╭══════╬╬═══════╮\nSΣTTIΠGS PRΩTΣCTIΩΠ\n╰══════╬╬═══════╯\n╭══════╬╬═══════╮\n"
                                 if msg.to in settings["cancelprotect"]: md+="╠➣PROIVITE ON✔\n"
                                 else: md+="╠➣PROINVITE:OFF✖\n"
                                 if msg.to in settings["PROTECT"]: md+="╠➣PROTECT ON✔\n"
                                 else: md+="╠➣PROTECT:OFF✖\n"
                                 if msg.to in settings["linkprotect"]: md+="╠➣PROLINK ON✔\n"
                                 else: md+="╠➣PROLINK:OFF✖\n"
                                 if msg.to in settings["pname"]: md+="╠➣NAMELOCK ON✔\n"
                                 else: md+="╠➣NAMELOCK:OFF✖\n"
                                 Galank.sendText(to,md + "╰══════╬╬═══════╯\n●TΣΔM SLΔCҜβΩT●")
#=================+
                        elif text.lower() == 'setmypict':
                            switch["changePicture"] = True
                            Galank.sendText(to, "Send to pictures")
                        elif text.lower() == 'setpict1':
                            switch["cp1"] = True
                            Galank1.sendText(to, "Send asisten 1 pictures")
                        elif text.lower() == 'setpict2':
                            switch["cp2"] = True
                            Galank2.sendText(to, "Send asisten 2 pictures")
                        elif text.lower() == 'setpictgrup':
                            if msg.toType == 2:
                                if to not in settings["changeGroupPicture"]:
                                    settings["changeGroupPicture"].append(to)
                                Galank.sendText(to, "Send group pictures")
                        elif text.lower() == 'responame':
                            s1 = Galank1.getProfile()
                            s2 = Galank2.getProfile()
                            Galank1.sendText(msg.to, s1.displayName + " Already..")
                            Galank2.sendText(msg.to, s2.displayName + " Already..")
#---------------------------------------------------
                        elif msg.text in ['cancel']:
                            if msg.toType == 2:
                                group = Galank.getGroup(msg.to)
                                gMembMids = [contact.mid for contact in group.invitee]
                                for _mid in gMembMids:
                                    Galank.cancelGroupInvitation(msg.to,[_mid]) 
                elif msg.contentType == 1:
                    if switch["changePicture"] == True:
                        path = Galank.downloadObjectMsg(msg_id)
                        switch["changePicture"] = False
                        Galank.updateProfilePicture(path)
                        Galank.sendText(to, "PP diganti")
                    if msg.toType == 2:
                        if to in settings["changeGroupPicture"]:
                            path = Galank.downloadObjectMsg(msg_id)
                            settings["changeGroupPicture"].remove(to)
                            Galank.updateGroupPicture(to, path)
                            Galank.sendText(to, "Berhasil mengubah foto group")
                    if switch["cp1"] == True:
                        path = Galank.downloadObjectMsg(msg_id)
                        switch["cp1"] = False
                        Galank1.updateProfilePicture(path)
                        Galank1.sendText(to, "PP bot 1 diganti")
                    if switch["cp2"] == True:
                        path = Galank.downloadObjectMsg(msg_id)
                        switch["cp2"] = False
                        Galank2.updateProfilePicture(path)
                        Galank2.sendText(to, "PP bot 2 diganti")
        if op.type == 19:
            if mid in op.param3:
                print("Asist 1 backup selfbot")
                if op.param2 in Bots:
                    X = Galank1.getGroup(op.param1)
                    X.preventedJoinByTicket = False
                    Galank1.updateGroup(X)
                    Ti = Galank1.reissueGroupTicket(op.param1)
                    Galank.acceptGroupInvitationByTicket(op.param1,Ti)
                    Galank1.acceptGroupInvitationByTicket(op.param1,Ti)
                    Galank2.acceptGroupInvitationByTicket(op.param1,Ti)
                    X = Galank.getGroup(op.param1)
                    X.preventedJoinByTicket = True
                    Galank.updateGroup(X)
                    Ti = Galank.reissueGroupTicket(op.param1)
                else:
                    settings["blacklist"][op.param2] = True
                    print("Kicker has been blacklist")
                    try:
                        X = Galank1.getGroup(op.param1)
                        X.preventedJoinByTicket = False
                        Galank1.updateGroup(X)
                        Ti = Galank1.reissueGroupTicket(op.param1)
                        Galank.acceptGroupInvitationByTicket(op.param1,Ti)
                        Galank1.acceptGroupInvitationByTicket(op.param1,Ti)
                        Galank2.acceptGroupInvitationByTicket(op.param1,Ti)
                        X = Galank.getGroup(op.param1)
                        X.preventedJoinByTicket = True
                        Galank.updateGroup(X)
                        Ti = Galank.reissueGroupTicket(op.param1)
                        Galank1.kickoutFromGroup(op.param1,[op.param2])
                        print("Bots1 Joined openqr")
                    except:
                        pass
            if Amid in op.param3:
                print("Asist 1 backup selfbot")
                if op.param2 in Bots:
                    X = Galank2.getGroup(op.param1)
                    X.preventedJoinByTicket = False
                    Galank2.updateGroup(X)
                    Ti = Galank2.reissueGroupTicket(op.param1)
                    Galank.acceptGroupInvitationByTicket(op.param1,Ti)
                    Galank1.acceptGroupInvitationByTicket(op.param1,Ti)
                    Galank2.acceptGroupInvitationByTicket(op.param1,Ti)
                    X = Galank.getGroup(op.param1)
                    X.preventedJoinByTicket = True
                    Galank.updateGroup(X)
                    Ti = Galank.reissueGroupTicket(op.param1)
                else:
                    settings["blacklist"][op.param2] = True
                    print("Kicker has been blacklist")
                    try:
                        X = Galank2.getGroup(op.param1)
                        X.preventedJoinByTicket = False
                        Galank2.updateGroup(X)
                        Ti = Galank2.reissueGroupTicket(op.param1)
                        Galank.acceptGroupInvitationByTicket(op.param1,Ti)
                        Galank1.acceptGroupInvitationByTicket(op.param1,Ti)
                        Galank2.acceptGroupInvitationByTicket(op.param1,Ti)
                        X = Galank.getGroup(op.param1)
                        X.preventedJoinByTicket = True
                        Galank.updateGroup(X)
                        Ti = Galank.reissueGroupTicket(op.param1)
                        Galank2.kickoutFromGroup(op.param1,[op.param2])
                        print("Bots1 Joined openqr")
                    except:
                        pass
            if Bmid in op.param3:
                print("Asist 1 backup selfbot")
                if op.param2 in Bots:
                    X = Galank.getGroup(op.param1)
                    X.preventedJoinByTicket = False
                    Galank.updateGroup(X)
                    Ti = Galank.reissueGroupTicket(op.param1)
                    Galank.acceptGroupInvitationByTicket(op.param1,Ti)
                    Galank1.acceptGroupInvitationByTicket(op.param1,Ti)
                    Galank2.acceptGroupInvitationByTicket(op.param1,Ti)
                    X = Galank1.getGroup(op.param1)
                    X.preventedJoinByTicket = True
                    Galank1.updateGroup(X)
                    Ti = Galank1.reissueGroupTicket(op.param1)
                else:
                    settings["blacklist"][op.param2] = True
                    print("Kicker has been blacklist")
                    try:
                        X = Galank.getGroup(op.param1)
                        X.preventedJoinByTicket = False
                        Galank.updateGroup(X)
                        Ti = Galank.reissueGroupTicket(op.param1)
                        Galank.acceptGroupInvitationByTicket(op.param1,Ti)
                        Galank1.acceptGroupInvitationByTicket(op.param1,Ti)
                        Galank2.acceptGroupInvitationByTicket(op.param1,Ti)
                        X = Galank1.getGroup(op.param1)
                        X.preventedJoinByTicket = True
                        Galank1.updateGroup(X)
                        Ti = Galank1.reissueGroupTicket(op.param1)
                        Galank.kickoutFromGroup(op.param1,[op.param2])
                        print("Bots1 Joined openqr")
                    except:
                        pass
        if op.param3 == "4":
          if op.param1 in settings["linkprotect"]:
            if op.param1 in settings["PROTECT"]:
             if op.param2 not in Bots:
                pass
             else:
                 Galank.kickoutFromGroup(op.param1,[op.param2])
                 settings["blacklist"][op.param2] = True
                 Galank.reissueGroupTicket(op.param1)
                 X = Galank.getGroup(op.param1)
                 X.preventedJoinByTicket = True
                 Galank.updateGroup(X)
                 settings["blacklist"][op.param2] = True
            else:
             if op.param2 in Bots:
                pass
             else:
                 Galank.reissueGroupTicket(op.param1)
                 X = Galank.getGroup(op.param1)
                 X.preventedJoinByTicket = True
                 Galank.updateGroup(X)
        if op.type == 32:
          if op.param1 in settings["PROTECT"]:
            if op.param2 in Bots:
                pass
            else:
                Inviter = op.param3.replace("",',')
                InviterX = Inviter.split(",")
                contact = Galank.getContact(op.param2)
                Galank.kickoutFromGroup(op.param1,[op.param2])
                settings["blacklist"][op.param2] = True
        if op.type == 13:
         if op.param1 in settings["cancelprotect"]:
          if op.param1 in settings["PROTECT"]:
            if op.param2 not in Bots:
               pass
            else:
                Inviter = op.param3.replace("",',')
                InviterX = Inviter.split(",")
                for _mid in InviterX:
                    Galank.cancelGroupInvitation(op.param1,[_mid])
                Galank.kickoutFromGroup(op.param1,[op.param2])
                settings["blacklist"][op.param2] = True
          else:
            if op.param2 in Bots:
               pass
            else:
                Inviter = op.param3.replace("",',')
                InviterX = Inviter.split(",")
                for _mid in InviterX:
                    Galank.cancelGroupInvitation(op.param1,[_mid])
                Galank.cancelGroupInvitation(op.param1,InviterX)
        if op.type == 17:
            if mid in op.param3:
                    group = Galank.getGroup(msg.to)
                    gMembMids = [contact.mid for contact in group.members]
                    matched_list = []
                    for tag in settings["blacklist"]:
                        matched_list+=filter(lambda str: str == tag, gMembMids)
                    if matched_list == []:
                        Galank.sendText(to,"nothing blacklist")
                        return
                    for jj in matched_list:
                        Galank.kickoutFromGroup(to,[jj])
                        Galank1.kickoutFromGroup(to,[jj])
                        Galank2.kickoutFromGroup(to,[jj])
                    Galank.sendText(to,"done")
        if op.type == 17:
            if op.param2 in settings["blacklist"]:
            	if op.param2 not in Bots:
                   Galank.kickoutFromGroup(op.param1,[op.param2])
                   Galank.sendContact(op.param1,[op.param2])
                   Galank.sendText(op.param1,"di blacklist Babik...")
            else:
                pass
        if op.type == 26:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0 or msg.toType == 2:
                if msg.toType == 0:
                    to = sender
        backupData()
    except Exception as error:
        logError(error)
while True:
    try:
        autoRestart()
        ops = poll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
               # bot(op)
                # Don't remove this line, if you wan't get error soon!
                poll.setRevision(op.revision)
                thread1 = threading.Thread(target=bot, args=(op,))#self.OpInterrupt[op.type], args=(op,)
                #thread1.daemon = True
                thread1.start()
                thread1.join()
    except Exception as e:
        logError(e)
