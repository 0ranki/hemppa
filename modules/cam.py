import re
from modules.common.module import BotModule
import requests


class MatrixModule(BotModule):
    def __init__(self,name):
        super().__init__(name)
        self.motionurl = 'http://localhost:8080'
        self.cameras = []
        self.allowed_cmds = {
                            'config': ['list','set','get','write'],
                            'detection': ['status','connection','start','pause'], 
                            'action': ['eventstart','eventend','snapshot','restart','quit','end']
                            }
        self.restricted_cmds = ['list','set','get','write','start','pause','restart','quit','end']
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
        data['cameras'] = self.cameras
        return data

    def set_settings(self, data):
        super().set_settings(data)
        if data.get('motionurl'):
            self.motionurl = data['motionurl']
        if data.get('cameras'):
            self.cameras = data['cameras']

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

        elif args[0] == 'cameras':
            if args[1] == 'set':
                bot.must_be_owner(event)
                self.cameras = args[2:]
                bot.save_settings()
                await bot.send_text(room, "Updated camera id list")
            elif args[1] == 'get':
                camstr = ''
                if len(self.cameras) == 0:
                    await bot.send_text(room, "No camera ids configured")
                else:
                    for n, cam in enumerate(self.cameras):
                        camstr = camstr + cam
                        if n < len(self.cameras) - 1:
                            camstr = camstr + ","
                    await bot.send_text(room, f"Following camera ids are configured:\n{camstr}")

        else:
            cmdindex = 1
            try:
                # Check if first argument is numeric (camera id)
                camid = int(args[0])
                camid = str(camid)
            except ValueError:
                cmdindex = 0
                camid = '0'
            category = args[cmdindex]
            ## Quick commands start
            if category == 'now':
                await self.get_snapshot(camid, bot, room, event)
                return
            ## Quick commands end
            if category not in self.allowed_cmds: 
                await bot.send_text(room, f'Unknown category: "{args[1]}"', event)
                return
            cmdindex = cmdindex + 1
            if args[cmdindex] not in self.allowed_cmds[category]:
                await bot.send_text(room, f'Unknown command: "{args[cmdindex]}"', event)
                return
            command = args[cmdindex]
            req_url = f'{self.motionurl}/{camid}/{category}/{command}'
            if command in self.restricted_cmds:
                bot.must_be_owner(event)
            if category == 'config' and command == 'get':
                queryparam = args[cmdindex + 1]
                req_url = f'{req_url}?query={queryparam}'
            elif category == 'config' and command == 'set':
                param = args[cmdindex + 1]
                value = args[cmdindex + 2]
                req_url = f'{req_url}?{param}={value}'
            if camid != 0 and command == 'snapshot':
                await self.get_snapshot(camid, bot, room, event)
            resp = requests.get(req_url).text
            await bot.send_text(room, resp, event)

    async def get_snapshot(self, camid, bot, room, event):
        imgurl = f"{self.motionurl.replace(':8080',':8081')}/{camid}/current"
        self.logger.info(f"Fetching image from {imgurl}")
        await bot.upload_and_send_image(room, imgurl, event, no_cache=True)

    def help(self):
        return self.helptext.splitlines()[0]
