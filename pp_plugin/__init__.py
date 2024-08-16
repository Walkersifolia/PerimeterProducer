from mcdreforged.api.all import *

PLUGIN_METADATA = {
    'id': 'pp',
    'version': '1.0.0',
    'name': 'PerimeterProducer',
    'description': 'A plugin with multiple functions',
    'author': 'WalkerTian',
    'link': 'https://github.com/Walkersifolia/PerimeterProducer'
}

def on_load(server: PluginServerInterface, old):
    server.register_help_message('!!pp', '快速生成空置域')
    server.logger.info('插件已加载！')

def on_player_command(server: PluginServerInterface, player: str, command: str):
    if command.startswith('!!pp'):
        args = command.split(' ')
        if len(args) == 3:
            try:
                x = int(args[1])
                y = int(args[2])
                clear_perimeter(server, player, x, y)
            except ValueError:
                server.reply(player, '请输入有效的数字。')
        else:
            server.reply(player, '用法：!!pp <x> <y>')

def clear_perimeter(server: PluginServerInterface, player: str, x: int, y: int):
    player_pos = server.get_player(player).pos
    half_size = (x - 1) // 2
    min_x = player_pos.x - half_size * 16
    max_x = player_pos.x + half_size * 16
    min_z = player_pos.z - half_size * 16
    max_z = player_pos.z + half_size * 16

    for i in range(256):
        for x in range(min_x, max_x, 16):
            for z in range(min_z, max_z, 16):
                server.execute(f'fill {x} {i} {z} {x + 15} {i} {z + 15} minecraft:air')

    server.reply(player, f'已清理以你当前位置为中心的 {x}x{y} 区块的空置区域。')

# 你可以根据需要添加更多函数或逻辑
