import requests
import json
import os
from random import choice
import random
import sys
sys.path.append("..")

import time
# import jieba
# import pandas as pd
configuration = json.load(open("./config.json", encoding='utf-8'))
group = configuration["group"]
apikey = configuration["apikey"]
ban_words = configuration["ban_words"]
path = configuration["path"]
self_qq = configuration["self_qq"]

help_base = "超天酱v1.3：\n"
help_base += "(帮助功能改进,新增游戏组队功能,增加了一些台词)：\n"
help_base += "这里是帮助菜单,直接输入.help就能触发,下列指令如需@则会标出：\n"
help_base += "1.@超天酱发送'猫猫图'返回一张蓝色猫猫图\n"
help_base += "2.st功能已禁用\n"
#help_base += "2.@超天酱发送'st'或者'色图'返回一张se图,可以查找se图,5s后撤回,看setu的孩子有惩罚哦:\n"
#help_base += "最多两个关键词查找,格式为:st 关键词1 关键词2\n"
#help_base += "同时关键词可以多选,比如关键词1可以是 白丝|黑丝 ,|代表或\n"
help_base += "3.@超天酱发送关键词：比如贴贴，可以和我说话唷 \n"
help_base += "4.私聊超天酱发送'.创房'可以创建房间,群聊发送'.查房'可以搜索房间\n"
help_base += "私聊输入'.创房'查看规则,群聊发送'.查房 关键词1 关键词2'查房\n"
help_base += "查房最多添加两个关键词，第一个关键词为PC,NS,PS,3DS,XBOX\n"
help_base += "第二个关键词为世界,崛起,GU,XX,4G,其他。注意字母保持大写\n"
help_base += "5.发送'.r'可以roll点了：格式 .r num1 num2(必须是大于0的整数）或直接.r 此功能不用@\n"
help_base += "基于Go-cqhttp构建，使用ws协议,更多功能有待作者完善，作者直接摆烂 \n"
help_base += "感谢github上的Go-cqhttp贡献者以及yesbot贡献者you8023 \n"
help_base += "Go-cqhttp项目地址：https://github.com/Mrs4s/go-cqhttp \n"
help_base += "yesbot项目地址：https://github.com/you8023/YesBot_ws_Go_CQHTTP \n"


# help_base += "那么发送aaa就会返回bbb啦~\n"
# help_base += "可以发送rmaaa+bbb删除对话哦~\n"

def help_menu(msg):
    if msg in ['.help', '.菜单', '.帮助','/help','。help','。菜单','。帮助','/菜单','/帮助']:
        return [True, help_base]
    else:
        return [False]


'''
def add_data(msg,all_data):
    if msg.count("+") != 1:
        return [False]
    if "/" in msg or "|" in msg:
        return [True,"不能含有/或|呀~"]
    if msg.split("+")[1]=="":
        return [False]
    msg = msg.split("+")
    if len(msg[0])< 1:
        return [True,"得有内容呀~"]
    for row in all_data:
        if msg[0] == row[0]:
            if msg[1] in row[1]:
                return [True,"这句话我已经会辣，不用再教我啦~"]
            row[1].append(msg[1])
            save_data(all_data)
            return [True,"超天酱记住啦~"]
    all_data.append([msg[0], [msg[1]]])
    save_data(all_data)
    return [True,"超天酱记住啦~"]
'''


def save_data(all_data):  # 用于记录语录的
    f = open("./data/talk_data/words", "w", encoding='UTF-8')
    for row in all_data:
        temp = row[0] + "|" + "".join([i + "/" for i in row[1]])
        f.writelines(temp + "\n")
    f.close()

global write_type
write_type=0
def create_room_intro(msg,user_id,ws):
    global write_type
    f = open("G:\\bot\\YesBot_ws_Go_CQHTTP\\room\\" + str(user_id) + ".txt", "a+",
             encoding='UTF-8')  # 对每个ID用户创建一个文件储存房间信息
    choosen1 = msg.find("PC") + msg.find("NS") + msg.find("PS") + msg.find("3DS") + msg.find("XBOX") #判断选项1是否正确
    choosen2 = msg.find("世界") + msg.find("崛起") + msg.find("GU") + msg.find("XX") + msg.find("4G") + msg.find("其他") #判断选项2是否正确
    if msg.find(".创房") == 0 and (choosen1 == -5 or choosen2 == -6): #指令0有 无指令1或无指令2 此时输入模式为0
        write_type = 0
        f.truncate(0) #创房时会清除原来文件内容
        intro = "欢迎使用自助创房功能,请输入指令选择您要创建房间的平台和游戏类型:\n"
        intro += "格式必须正确 如PC的冰原创房应当输入:'PC 世界'\n"
        intro += "PC  PC平台\n"
        intro += "NS  NS平台\n"
        intro += "PS  PS平台\n"
        intro += "3DS  3DS平台\n"
        intro += "XBOX  XBOX平台\n"
        intro += "世界  怪物猎人世界/冰原\n"
        intro += "崛起  怪物猎人崛起/破晓\n"
        intro += "GU  怪物猎人GU\n"
        intro += "XX  怪物猎人XX\n"
        intro += "4G  怪物猎人4G\n"
        intro += "其他  其他游戏\n"
        data = {
            'user_id': user_id,
            'message': intro
        }
        action = "send_msg"
        post_data1 = json.dumps({"action": action, "params": data})
        rev1 = ws.send(post_data1)
    elif choosen1 > -5 and choosen2 == -6 and write_type == 0: #只输入指令1 无指令2，此时输入模式变为1
        write_type = 1
        f.write(msg+' ') #写入信息
        intro = "请输入指令选择您要创建房间的游戏类型:\n"
        intro += "格式必须正确 如冰原创房应当输入:'世界'\n"
        intro += "世界  怪物猎人世界/冰原\n"
        intro += "崛起  怪物猎人崛起/破晓\n"
        intro += "GU  怪物猎人GU\n"
        intro += "XX  怪物猎人XX\n"
        intro += "4G  怪物猎人4G\n"
        intro += "其他  其他游戏\n"
        intro += "像P3，2G这些可以去游侠联机平台联机\n"
        data = {
            'user_id': user_id,
            'message': intro
        }
        action = "send_msg"
        post_data1 = json.dumps({"action": action, "params": data})
        rev1 = ws.send(post_data1)
    elif choosen2 > -6 and write_type == 1: #指令1已输入，只输入指令2，输入模式变为2
        write_type = 2
        f.write(msg+' ') #写入信息
        intro = "这是最后一步了,请输入您的房间号和房间描述,当前人数和最大人数:\n"
        intro += "格式:房间号 房间描述(不要带空格)\n"
        #intro += "格式:房间号 房间描述(不要带空格) 当前人数 最大人数\n"
        data = {
            'user_id': user_id,
            'message': intro
        }
        action = "send_msg"
        post_data1 = json.dumps({"action": action, "params": data})
        rev1 = ws.send(post_data1)
    elif choosen1 > -5 and choosen2 > -6 and write_type == 0: #指令1指令2都有，输入模式变为2
        write_type = 2
        f.write(msg+' ') #写入信息
        intro = "这是最后一步了,请输入您的房间号和房间描述,当前人数和最大人数:\n"
        intro += "格式:房间号 房间描述(不要带空格)\n"
        #intro += "格式:房间号 房间描述(不要带空格) 当前人数 最大人数\n"
        data = {
            'user_id': user_id,
            'message': intro
        }
        action = "send_msg"
        post_data1 = json.dumps({"action": action, "params": data})
        rev1 = ws.send(post_data1)
    elif write_type == 2:  #输入模式为2,最后输入房间
        write_type = 0
        words = msg.split(' ')  # 按空格分割信息,计数tag
        intro = "房间创建成功啦\n"
        intro += "在群内输入'.查房'可以查找到房间了\n"
        intro += "使用完之后记得私聊我输入'.删房'删除房间哦"
        f.write(words[0] + " " + words[1]+"\n")  # 写入信息
        #f.write(words[0]+" "+words[1]+" ("+words[2]+"/"+words[3]+")\n") #写入信息

        filedata = f.read(-1)  # 读取文件
        #group_id=msg['temp_source']
        group_message="一个新的房间被创建啦！大家快来联机吧\n"
        group_message +=filedata
        data = {
            'group_id': "简单粗暴自己填",
            'user_id': user_id,
            'message': group_message
        }
        action = "send_group_msg"
        post_data1 = json.dumps({"action": action, "params": data})
        rev1 = ws.send(post_data1)

        f.close()
        return [True,intro]
    elif msg.find(".删房")>=0 :
        write_type = 0
        f.truncate(0) #清除文件内容
    else :
        intro = "超天酱私聊功能仅为创房服务，请勿输入与创房无关内容\n"
        intro += "输入'.创房'来创建房间，格式出现错误建议重新开始创建"
        intro += "使用完之后记得私聊我输入'.删房'删除房间哦"
        f.close()
        return [True,intro]
    return [False]
    '''

    elif (msg.find(".创房") == 0 or choosen2 > -6) and choosen1 == -5: #指令0或指令2有 无指令1
        intro = "请输入指令选择您要创建房间的游戏类型:\n"
        intro += "格式必须正确 如PC的冰原创房应当输入:'.p1 .世界'\n"
        intro += ".p1  PC\n"
        intro += ".p2  NS\n"
        intro += ".p3  PS\n"
        intro += ".p4  3DS\n"
        intro += ".p5  XBOX\n"
        data = {
            'user_id': user_id,
            'message': intro
        }
        action = "send_msg"
        post_data1 = json.dumps({"action": action, "params": data})
        rev1 = ws.send(post_data1)
    '''

def find_room(msg,group_id,ws):
    if msg.find(".查房")>=0 :
        words = msg.split(' ')  # 按空格分割信息,计数tag
        path = "G:\\chaotianbot\\YesBot_ws_Go_CQHTTP\\room\\"  # 文件夹目录
        files = os.listdir(path)  # 得到文件夹下的所有文件名称
        message = "平台 游戏 房间号 房间描述\n"
        #message ="平台 游戏 房间号 房间描述 当前人数 最大人数\n"
        for file in files:  # 遍历文件夹
            keyword = 0 #作为找到关键词的标记
            position = path + str(file)  # 构造绝对路径
            with open(position, "r",encoding='UTF-8') as f : # 读取遍历的文件
                filedata = f.read(-1)  # 读取文件
                if len(words)>1 :
                    for word in words :
                        if filedata.find(str(word))>=0 :
                            keyword=1 #找到关键词标记一下该文件
                if keyword==1 and len(words)>1 : #关键词存在时
                    message = message + filedata  #找到关键词则读取该文件内容并输出
                elif len(words)==1 : #关键词不存在时
                    message = message + filedata  # 无关键词时直接输出
            f.close()
        data = {
            'group_id': group_id,
            'message': message
        }
        action = "send_group_msg"
        post_data1 = json.dumps({"action": action, "params": data})
        rev1 = ws.send(post_data1)




def del_data(del_data, all_data):
    if del_data[:2] != "rm":
        return [False]
    msg = del_data[2:].split("+")
    for i in range(len(all_data)):
        if msg[0] == all_data[i][0]:
            if len(all_data[i][1]) == 1:
                all_data.pop(i)
                save_data(all_data)
                return [True, "已经删除啦~"]
            all_data[i][1].remove(msg[1])
            save_data(all_data)
            return [True, "已经删除啦~"]
    return [True, "删除出错啦~"]


def detect_ban(msg, user_id, group_id, message_id, ws):
    if group_id not in group:
        return [False]
    for words in ban_words:
        if msg.find(words) >= 0 :
            data = {
                'group_id': group_id,
                'user_id': user_id,
                'message_id': message_id,
                'duration': 60
            }
            # cq_url = "ws://127.0.0.1:6700/set_group_ban"
            # requests.post(cq_url,data=data)
            action = "set_group_ban"
            post_data1 = json.dumps({"action": action, "params": data})
            post_data2 = json.dumps({"action": "delete_msg", "params": data})
            rev1 = ws.send(post_data1)
            rev2 = ws.send(post_data2)
            return [True, "不要说不该说的话啦~"]
    return [False]


def roll_num(msg):
    if msg.find('.r') == 0 or msg.find('。r') == 0 :
        try:
            msg = msg[3:]
            nums = msg.split(' ')  # 按空格分割信息,计数tag
            num1 = int(nums[0])
            print(num1)
            num2 = int(nums[1])
            print(num2)
            fin_num = random.randint(num1, num2)
            print(fin_num)
            return [True, "( " + str(num1) + " d " + str(num2) + " ): " + str(fin_num)]
        except Exception as e:
            print(e)
            fin_num = random.randint(1, 100)
            return [True, "( 1 d 100 ): " + str(fin_num) + "  默认掷点"]
    return [False]


def ghs_pic(msg, user_id, group_id, message_id, ws):
    if (msg.find('st') == 0) or (msg.find('色图') == 0):
        try:
            msg = msg[3:]
            tags = msg.split(' ')  # 按空格分割信息,计数tag
            req_url = "https://api.lolicon.app/setu/v2"
            params = {"tag": tags}
            # req_url = quote(url, safe=string.printable)  # safe表示可以忽略的字符

            res = requests.get(req_url, params=params)
            setu_title = res.json()['data'][0]['title']
            setu_url = res.json()['data'][0]['urls']['original']
            setu_pid = res.json()['data'][0]['pid']
            setu_author = res.json()['data'][0]['author']
            setu_url = "https://pixiv.runrab.workers.dev/" + setu_url[20:]  #手动添加代理
            local_img_url = "title:" + setu_title + "[CQ:image,file=" + setu_url + "] " + "     pid:" + str(
                setu_pid) + " 画师:" + setu_author + "   喜欢色色的孩子要接受惩罚哦~"
            data1 = {
                'group_id': group_id,
                'user_id': user_id,
                'message_id': message_id,
                'duration': 60,
                'message': local_img_url
            }
            # cq_url = "ws://127.0.0.1:6700/set_group_ban"
            # requests.post(cq_url,data=data)
            post_data1 = json.dumps({"action": "set_group_ban", "params": data1})
            post_data2 = json.dumps({"action": "delete_msg", "params": data1})
            rev1 = ws.send(post_data1)
            rev2 = ws.send(post_data2)
            return [True,local_img_url]

            '''
            post_data3 = json.dumps({"action": "send_group_msg", "params": data1})
            rev3 = ws.send(post_data3)
            #del_id=rev3['message_id']
            #print(del_id)
            print(rev3['message_id'])
            data2 = {
                'group_id': group_id,
                'user_id': user_id,
                'message_id': post_data3['message_id']
            }
            start = time.time()
            while(time.time() < start+5):
                action = "delete_msg"
            post_data4 = json.dumps({"action": "delete_msg", "params": data2}) #撤回自己的信息
            rev4 = ws.send(post_data4)
            '''
        except Exception as e:
            print(e)
            return [True, "找不到色图呢,你的XP好怪哦"]
    return [False]


def hs_pic(msg):
    if msg.find('来点大的') == 0:
        try:
            msg = msg[5:]
            tags = msg.split(' ')  # 按空格分割信息,计数tag
            req_url = "https://api.lolicon.app/setu/v2"
            # params = {"apikey":apikey,"r18":"1"}
            params = {"r18": "1", "tag": tags}
            res = requests.get(req_url, params=params)
            setu_title = res.json()['data'][0]['title']
            setu_url = res.json()['data'][0]['urls']['original']
            setu_pid = res.json()['data'][0]['pid']
            setu_author = res.json()['data'][0]['author']
            setu_url = "https://pixiv.runrab.workers.dev/" + setu_url[20:]

            local_img_url = "title:" + setu_title + "[CQ:image,file=" + setu_url + "]" + "     pid:" + str(
                setu_pid) + " 画师:" + setu_author + "   喜欢色色的孩子要接受惩罚哦~"
            return [True, local_img_url]
        except Exception as e:
            print(e)
            return [True, "找不到色图呢,你的XP好怪哦"]
    return [False]

def ghs_del(msg, user_id, group_id, message_id, ws): #在发出色图5S后撤回
    try:
        if msg.find("   喜欢色色的孩子要接受惩罚哦~") >= 0:
            did = msg.find("   喜欢色色的孩子要接受惩罚哦~")
            print(did)
            data = {
                'group_id': group_id,
                'user_id': user_id,
                'message_id': message_id
            }
            start = time.time()
            while (time.time() < start + 5):  # 延迟5s
                action = "delete_msg"
            post_data2 = json.dumps({"action": action, "params": data})  # 撤回自己的信息
            rev2 = ws.send(post_data2)
    except Exception as e:
        print(e)
    return [False]

def mao_pic(msg):
    if msg in ["来张猫猫图", "来张猫图", "猫图", "猫猫虫", "maomaochong", "猫猫图", "猫", "蓝皮猪", "蓝色猫猫虫", "猫猫", "蓝色猫猫", "咖波", "猫猫虫咖波"]:
        setu_list = os.listdir(path)
        local_img_url = "[CQ:image,file=file:///" + path + choice(setu_list) + "]"
        return [True, local_img_url]
    return [False]


'''
def send_forward(msg, group_id, ws, sender):
    group_msg = []
    for item in msg:
        each_msg = {
            "type": "node",
            "data": {
                "name": "互联网小天使超天酱",
                "uin": self_qq,
                "content": item
            }
        }
        group_msg.append(each_msg)
    data = {
        'group_id': group_id,
        'messages': group_msg
    }
    # print(data)
    # cq_url = "ws://127.0.0.1:5700/send_group_forward_msg"
    # rev3 = requests.post(cq_url,data=data)
    # print(rev3.json())
    action = "send_group_forward_msg"
    post_data = json.dumps({"action": action, "params": data})
    rev = ws.send(post_data)
    # print(rev)
    returnStr = "[CQ:at,qq={sender}]".format(sender=sender)
    return returnStr
'''
def send_history(msg, group_id, ws):

    data = {
        'message_seq': msg,
        'group_id': group_id
    }
    # print(data)
    # cq_url = "ws://127.0.0.1:5700/send_group_forward_msg"
    # rev3 = requests.post(cq_url,data=data)
    # print(rev3.json())
    action = "get_group_msg_history"
    post_data = json.dumps({"action": action, "params": data})
    rev = ws.send(post_data)
    # print(rev)
    #returnStr = "[CQ:at,qq={sender}]".format(sender=sender)
    return [True]

def send_private(msg, sender, ws):
    data = {
        'user_id': sender,
        'message': msg,
        'auto_escape': False
    }
    # cq_url = "ws://127.0.0.1:5700/send_private_msg"
    action = "send_private_msg"
    post_data = json.dumps({"action": action, "params": data})
    rev = ws.send(post_data)
    return rev


'''
def add_friend(sender, msg, ws):
    # if sender in admin_qq:
    #     return [True, '']
    try:
        print('add_friends')
        if msg == '想要的答案':
            return [True, ""]
        else:
            return [False, ""]
        # print(result)
        # if result != ():
        #     return [True, ""]
    except Exception as e:
        print(e)
    return [False, '']
'''
