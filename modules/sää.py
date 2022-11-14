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

        time = weather['timestamp'].split()[1]

        weathermsg = f"""Sää klo {time}:

        Lämpötila on tällä hetkellä {weather['tempnow']} astetta.
        Tulevan vuorokauden alin lämpötila on {weather['templo']} astetta
        ja ylin {weather['temphi']} astetta.

        Ilmankosteus on {weather['humidity']}%.
        
        Kuluneen tunnin sademäärä on {weather['precipitation1h']}mm
        ja kuluneen vuorokauden {weather['precipitation1d']}mm.
        
        Tuuli puhaltaa {winddir} nopeudella {weather['windspeed']}m/s
        voimakkuus puuskissa on {weather['windspeedmax']}m/s"""

        await bot.send_text(room, weathermsg, event)

    def help(self):
        return 'Kertoo tämänhetkisen säätilan VTT:n Linnanmaan yksikön mittauspisteellä.'
