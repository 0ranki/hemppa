from modules.common.module import BotModule
import requests
import json


class MatrixModule(BotModule):
    async def matrix_message(self, bot, room, event):
        json_weather = requests.get('http://weather.willab.fi/weather.json').text
        weather = json.loads(json_weather)
        winddir = 'pohjoisesta'
        if weather['winddir'] >= 23 and weather['winddir'] < 68:
            winddir = 'koillisesta'
        elif weather['winddir'] >= 68 and weather['winddir'] < 113:
            winddir = 'idästä'
        elif weather['winddir'] >= 113 and weather['winddir'] < 158:
            winddir = 'kaakosta'
        elif weather['winddir'] >= 158 and weather['winddir'] < 203:
            winddir = 'etelästä'
        elif weather['winddir'] >= 203 and weather['winddir'] < 248:
            winddir = 'lounaasta'
        elif weather['winddir'] >= 248 and weather['winddir'] < 293:
            winddir = 'lännestä'
        elif weather['winddir'] >= 293 and weather['winddir'] < 338:
            winddir = 'luoteesta'

        weathermsg = f"""\
        Lämpötila on tällä hetkellä {weather['tempnow']} astetta.

        Ilmankosteus on {weather['humidity']}% ja sadetta on odotettavissa
        seuraavan tunnin aikana {weather['precipitation1h']}mm
        ja tulevan vuorokauden aikana {weather['precipitation1d']}mm.
        
        Tuuli puhaltaa {winddir} nopeudella {weather['windspeed']}m/s, voimakkuus
        puuskissa on {weather['windspeedmax']}m/s"""

        await bot.send_text(room, weathermsg, event)

    def help(self):
        return 'Kertoo tämänhetkisen säätilan VTT:n Linnanmaan yksikön mittauspisteellä.'
