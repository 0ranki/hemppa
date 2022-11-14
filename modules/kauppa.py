from modules.common.module import BotModule


class MatrixModule(BotModule):
    async def matrix_message(self, bot, room, event):
        rawlist = event.body.split(' ', 1)
        rawlist.pop(0)

        mdlist = list()
        rawlist = rawlist[0].splitlines()
        for item in rawlist:
            mdlist.append('- [ ] ' + item)
        
        self.logger.debug(mdlist)

        await bot.send_text(room, "\n".join(mdlist), event)

    def help(self):
        return 'Formats the list given as arguments to a Markdown checkbox list'
