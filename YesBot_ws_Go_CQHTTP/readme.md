<p align="center">
  <a href="https://ishkong.github.io/go-cqhttp-docs/"><img src="https://i.loli.net/2021/01/28/XFrqchNZ5o2MOLB.jpg" width="200" height="200" alt="go-cqhttp"></a>
</p>


<div align="center">

# 进击的Yes酱-会发涩图的群管理机器人

_✨ 基于 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp)，使用[NoneBot](https://github.com/nonebot/nonebot2)标准的插件 ✨_

</div>

<p align="center">
  <a href="#">
    <img src="https://img.shields.io/badge/python-v3.7%2B-green" alt="license">
  </a>
  <a href="https://github.com/Yang9999999/Go-CQHTTP-YesBot">
    <img src="https://img.shields.io/badge/release-v1.0-red" alt="release">
  </a>
</p>




---
YesBot_ws_Go_CQHTTP 是采用python编写，基于Go-CQHTTP-YesBot二次开发，**可拓展的**，**适合新手**的入门级QQ机器人插件

感谢[原作者的yes酱](https://github.com/Yang9999999/Go-CQHTTP-YesBot)以及you8023分享的项目

ELK编写

## 目前拥有的功能

- 发送猫猫图返回一张猫猫图
- @机器人发送'st'或'色图'返回一张色图,此功能默认关闭
- 发送色图功能可以加入关键词,使用格式为'st 关键词1 关键词2'
- 检测关键字禁言
- @机器人可以与她对话,私聊调教功能被关闭
- 添加好友自动处理
- 可以私聊发送'.创房'创建房间,群内发送'.查房'可以查看房间,方便怪猎游戏群内组队
- 查房格式为'查房 关键词1 关键词2'
- ~~发送huangse获得R18涩图~~
- 发送'.r'可以roll点
- 更多功能待开发....

## 配置

配置信息在**config.json**中

```json
{
    "path":"/C:\\Users\\86175\\Desktop\\mybot\\pic\\mao\\",
	"ban_words":["科学上网","黑产","翻墙"], 
    "apikey":"xxxxxxxxxxxxxxxx",
    "group":[123456789,987654321],
    "self_qq":"2013996860"
}
```

分别为 

- 储存猫猫图的路径  Linux下为"/root/mybot1/pic/mao/"
- 禁言关键词
- 涩图API的apikey
- Yes酱管理的群号
- Yes酱的QQ号

## API

- 机器人采用的[涩图API](https://api.lolicon.app/#/setu)

## 编写目的

用于python学习和交流

~~造福群友~~(不是)
第一次学习用python做群机器人，很感谢原作者分享的项目，本人才疏学浅，编写的代码难免出现各类问题，还请各位自行修改

## 示例

![image.png](https://i.loli.net/2021/01/28/4pes3iQaO1yETGM.png)

![image.png](https://i.loli.net/2021/01/28/njycUxfBGpvm1QY.png)

![image.png](https://i.loli.net/2021/01/28/f4gV32lnivEACKT.png)

## 文档

https://www.jianshu.com/p/66318d7e26cf
