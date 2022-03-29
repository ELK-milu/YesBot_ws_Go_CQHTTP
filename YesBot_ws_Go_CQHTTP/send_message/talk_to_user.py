from send_message.word_detect import *
from random import choice
from data.talk_data.base_talk import others_answer
import random

#--------------------------------------------------------------------------------------聊天
def match(msg,talk_data):
	for row in talk_data:
		if msg.find(row[0]) >= 0:
			max=len(row[1]) - 1
			num = random.randint(0, max)
			return [True,row[1][num]]
	return [False,choice(others_answer["no_answer"])]

global room_type
room_type=0
def talk_to_user(rev,talk_data,ws):#这里可以DIY对私聊yes酱的操作
	msg=rev["raw_message"]
	user_id = rev['user_id']
	group_id = ""
	#--------------------------------------------------------------------------------------帮助页面
	if_help = help_menu(msg)
	if if_help[0] == True:
		return if_help[1]
	'''
	#--------------------------------------------------------------------------------------删除数据
	if_del = del_data(msg,talk_data)
	if if_del[0] == True:
		return if_del[1]
	#--------------------------------------------------------------------------------------添加数据
	if_add = add_data(msg,talk_data)
	if if_add[0] == True:
		return if_add[1]
	#--------------------------------------------------------------------------------------发送涩图
	if_setu = ghs_pic(msg)
	if if_setu[0] == True:
		return if_setu[1]
	#--------------------------------------------------------------------------------------发送R18
	if_setu = hs_pic(msg)
	if if_setu[0] == True:
		return if_setu[1]
	#--------------------------------------------------------------------------------------发送猫猫图
	if_setu = mao_pic(msg)
	if if_setu[0] == True:
		return if_setu[1]	
	'''
	#--------------------------------------------------------------------------------------发送创房信息
	if_create_room = create_room_intro(msg,user_id,ws)
	if if_create_room[0] == True:
		return if_create_room[1]

	return [False]

def talk_to_group_user(rev,talk_data, ws):#这里可以DIY对群聊中@yes酱的操作
	msg=rev["raw_message"]
	group_id = rev["group_id"]
	user_id=rev["user_id"]
	message_id = rev["message_id"]
	#--------------------------------------------------------------------------------------检测关键字禁言,优先级最高
	if_ban = detect_ban(msg,user_id,group_id,message_id, ws)
	if if_ban[0] == True:
		return if_ban[1]
	#--------------------------------------------------------------------------------------帮助页面
	if_help = help_menu(msg)
	if if_help[0] == True:
		return if_help[1]
	'''
	#--------------------------------------------------------------------------------------发送涩图
	if_setu = ghs_pic(msg, user_id, group_id, message_id, ws)
	if if_setu[0] == True:
		return if_setu[1]
	#--------------------------------------------------------------------------------------发送R18
	if_setu = hs_pic(msg)
	if if_setu[0] == True:
		return if_setu[1]
	'''
    #--------------------------------------------------------------------------------------发送猫猫图
	if_setu = mao_pic(msg)
	if if_setu[0] == True:
		return if_setu[1]
    #--------------------------------------------------------------------------------------发送roll点
	if_roll = roll_num(msg)
	if if_roll[0] == True:
		return if_roll[1]

	return match(msg, talk_data)[1]


def add_friends(rev, ws):#这里可以DIY对添加好友的操作
	print(rev)
	sender = rev['user_id']
	msg = rev['comment'].split('回答:')[1]
	if_add = add_friend(sender, msg, ws)
	obj = {
		'isOK': if_add[0],
		'flag': rev['flag'],
		'friendsName': if_add[1]
	}
	return obj

def talk_to_gourp(rev,talk_data, ws):#这里可以DIY对群聊的操作
	msg=rev["raw_message"]
	user_id=rev["user_id"]
	group_id=rev["group_id"]
	message_id = rev["message_id"]
	sender = rev["sender"]
	message_seq = rev["message_seq"]
	#--------------------------------------------------------------------------------------检测关键字禁言
	if_ban = detect_ban(msg,user_id,group_id,message_id, ws)
	if if_ban[0] == True:
		return if_ban[1]
	#--------------------------------------------------------------------------------------帮助页面
	if_help = help_menu(msg)
	if if_help[0] == True:
		return if_help[1]
	# --------------------------------------------------------------------------------------发送roll点
	if_roll = roll_num(msg)
	if if_roll[0] == True:
		return if_roll[1]
	#--------------------------------------------------------------------------------------撤回涩图
	if_chehui = ghs_del(msg, user_id, group_id, message_id, ws)
	if if_chehui[0] == True:
		return if_chehui[1]
	# --------------------------------------------------------------------------------------查找房间
	if_find_room = find_room(msg,group_id,ws)
	if if_find_room[0] == True:
		return if_find_room[1]

	'''
	# --------------------------------------------------------------------------------------查看群历史消息
	if_send_history = send_history(msg, group_id, ws)
	if if_send_history[0] == True:
		return if_send_history[1]
	'''





	#if match(msg,talk_data)[0]==True:
		#return match(msg,talk_data)[1]
	return ""


