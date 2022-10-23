from modules.common.module import BotModule
import requests


class MatrixModule(BotModule):
    def __init__(self,name):
        super().__init__(name)
        self.motionurl = 'http://192.168.1.220:8080'

    async def matrix_message(self, bot, room, event):
        args = event.body.split()
        args.pop(0)

        if args[0] == 'config':
            if args[1] == 'list':
                req_url = self.motionurl
                for arg in args:
                    req_url = f'{req_url}/{arg}'
                
                resp = requests.get(req_url)
                await bot.send_text(resp.content)

    def help(self):
        return 'Echoes back what user has said'
