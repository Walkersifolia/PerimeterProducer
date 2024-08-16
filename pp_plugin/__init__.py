from mcdreforged.api.all import *
import time

PLUGIN_METADATA = {
    'id': 'pp',
    'version': '1.0.0',
    'name': 'PerimeterProducer',
    'description': 'A plugin with multiple functions',
    'author': 'WalkerTian',
    'link': 'https://github.com/Walkersifolia/PerimeterProducer'
}

DELAY = 0.1
Prefix = "!!pp"
CHUNK = 16
ABORT = False
WORKING = False
NEED_COMMIT = False

p1 = None
p2 = None
p3 = None
p4 = None

def on_info(server, info):
    global Prefix, DELAY
    global CHUNK, ABORT, WORKING, NEED_COMMIT
    global p1, p2, p3, p4
    content = info.content
    cmd = content.split()
    if len(cmd) == 0 or cmd[0] != Prefix:
        return
    del cmd[0]
    # !!perimeter abort
    if len(cmd) == 1 and cmd[0] == "abort":
        if not WORKING and not NEED_COMMIT:
            server.reply(info, "§c没有需要中断的操作")
            return
        ABORT = True
        NEED_COMMIT = False
        server.reply(info, "§c终止操作！")
        return
    # !!perimeter abort <length> <width>
    if len(cmd) == 3 and cmd[0] == "make":
        if WORKING:
            server.reply(info, "§c当前正在清理，请等待清理结束！")
        try:
            p1 = -int(cmd[1])/2 * CHUNK
            p2 = int(cmd[1])/2 * CHUNK
            p3 = -int(cmd[2])/2 * CHUNK
            p4 = int(cmd[2])/2 * CHUNK
        except:
            server.reply(info, "§c你输入的不是数字！")
        
        NEED_COMMIT = True
        server.reply(info, "§a请输入§6{} commit§a确认操作！".format(Prefix))

    if len(cmd) == 1 and cmd[0] == "commit":

        if not NEED_COMMIT:
            server.reply(info, "§c没有需要确认的操作")
            return

        server.say("§a开始操作！请在§c原地§a耐心等待，§c不要移动")
        NEED_COMMIT = False

        server.execute("carpet fillLimit 2000000")
        server.execute("carpet fillUpdates false")
        
        WORKING = True
        for i in range(0, 255):
            if ABORT:
                ABORT = False
                WORKING = False
                break
            y = 255 - i
            command = "execute at {} run fill ~{} {} ~{} ~{} {} ~{} air".format(info.player, p1, y, p3, p2, y, p4)
            server.say("正在替换第{}层".format(y))
            time.sleep(DELAY)
            server.execute(command)
        WORKING = False
        server.say("§a操作完成！")

def on_load(server: PluginServerInterface, old):
    server.register_help_message('!!pp', '快速生成空置域')
    server.logger.info('插件已加载！')