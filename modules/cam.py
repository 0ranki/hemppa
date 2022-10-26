import re
from modules.common.module import BotModule
import requests


class MatrixModule(BotModule):
    def __init__(self,name):
        super().__init__(name)
        self.motionurl = 'http://192.168.1.220:8080'
        self.allowed_cmds = {
                            'config': ['list','set','get','write'],
                            'detection': ['status','connection','start','pause'], 
                            'action': ['eventstart','eventend','snapshot','restart','quit','end']
                            }
        self.helptext = """Control the motion daemon.
        Available commands:
        - config list|set|get|write
        - detection status|connection|start|pause
        - action eventstart|eventend|snapshot|restart|quit|end
        - url get|set <motionurl>
        
        Usage: '!cam <id> category command'

        <id> is the numerical id of the camera. Use 0 for all cameras.
        If <id> is omitted, 0 is assumed."""

    def get_settings(self):
        data = super().get_settings()
        data['motionurl'] = self.motionurl
        return data

    def set_settings(self, data):
        super().set_settings(data)
        if data.get('motionurl'):
            self.motionurl = data['motionurl']

    async def matrix_message(self, bot, room, event):
        args = event.body.split()
        args.pop(0)
        if args[0] == 'help':
            await bot.send_text(room, self.helptext, event)
            return

        elif args[0] == 'url':
            if args[1] == 'set':
                newurl = args[2]
                bot.must_be_owner(event)
                self.motionurl = newurl
                bot.save_settings()
                await bot.send_text(room, f"Motion API URL set to {self.motionurl}")
            elif args[1] == 'get':
                await bot.send_text(room, f"Motion URL is currently {self.motionurl}")

        else:
            recvd_camid = 1
            try:
                # Check if first argument is numeric (camera id)
                camid = int(args[0])
                camid = str(camid)
            except ValueError:
                recvd_camid = 0
                camid = '0'
            if args[recvd_camid] not in self.allowed_cmds: 
                await bot.send_text(room, f'Unknown category: "{args[1]}"', event)
                return
            category = args[recvd_camid]
            recvd_camid = recvd_camid + 1
            if args[recvd_camid] not in self.allowed_cmds[category]:
                await bot.send_text(room, f'Unknown command: "{args[recvd_camid]}"', event)
                return
            command = args[recvd_camid]
            req_url = f'{self.motionurl}/{camid}/{category}/{command}'
            resp = requests.get(req_url).text
            await bot.send_text(room, resp, event)

    def help(self):
        return self.helptext.splitlines()[0]
