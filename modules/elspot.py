from modules.common.module import BotModule
from nordpool import elspot
from datetime import datetime, date
import pytz


class MatrixModule(BotModule):
    def __init__(self,name):
        super().__init__(name)
        self.country = None
        self.timezone = None
        self.price_history = []
        self.updated = None

    def get_settings(self):
        data = super().get_settings()
        data['country'] = self.country
        data['timezone'] = self.timezone
        data['price_history'] = self.price_history
        data['updated'] = self.updated
        return data

    def set_settings(self,data):
        super().set_settings(data)
        if data.get('country'):
            self.country = data['country']
        if data.get('timezone'):
            self.timezone = data['timezone']
        if data.get('price_history'):
            self.price_history = data['price_history']
        if data.get('updated'):
            self.updated = data['updated']

    async def matrix_message(self, bot, room, event):
        args = event.body.split()
        args.pop(0)

        if len(args) >= 2 and args[0] == 'config':
            if args[1] == 'country':
                if len(args) >= 3:
                    bot.must_be_owner(event)
                    self.country = args[2]
                    self.logger.info(f"Changing country to {args[2]}")
                    bot.save_settings()
                    await bot.send_text(room, f"Elspot will fetch prices for {args[2]}", event)
                    return
                else:
                    await bot.send_text(room, f"A country must be specified. Currently configured {self.country}", event)
                    return
            elif args[1] == 'timezone':
                if len(args) >= 3:
                    bot.must_be_owner(event)
                    self.logger.info(f"Changing timezone to {args[2]}")
                    self.timezone = args[2]
                    bot.save_settings()
                    await bot.send_text(room, f"Elspot will show times in {args[2]}", event)
                    return
                else:
                    await bot.send_text(room, f"A timezone must be specified. Currently configured {self.timezone}", event)
                    return
        elif len(args) == 1 and args[0] == 'config':
            await bot.send_text(room, f"Currently configured to show prices for {self.country} in {self.timezone} timezone", event)

        if len(args) == 0 and self.country is not None and self.timezone is not None:
            self.logger.info(f"Fetching current price for {self.country}, using timezone {self.timezone}")
            UTC = pytz.timezone('UTC')
            LOCAL = pytz.timezone(self.timezone)
            local_today = datetime.now(LOCAL)
            utc_today = datetime.now(UTC)
            utc_todaystr = date.strftime(utc_today, "%Y-%m-%d")
            utc_curhour = date.strftime(utc_today, "%H")
            prices_spot = elspot.Prices()
            prices = prices_spot.hourly(areas=[self.country],end_date=utc_todaystr)
            price = str(prices['areas']['FI']['values'][int(utc_curhour)]['value']/1000) + " € / kWh"
            msg = f"Nord Pool spot price at {local_today}: {price}"
            await bot.send_text(room, msg, event)
        

    def help(self):
        return 'Electricity spot prices'
