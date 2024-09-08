import datetime
import sys

if "/config/pyscript_modules" not in sys.path:
    sys.path.append("/config/pyscript_modules")

import myconfig

class Contact:
    def __init__(self, name, bd) -> None:
        self.name = name
        self.birthdate = bd[:4]
        if len(bd) == 6 :
            self.age = str(datetime.datetime.now().year - int(f"19{bd[-2:]}"))
        else:
            self.age = "unknown"

def date2stringshort(date) -> str:
    assert isinstance(date, datetime.datetime)
    return f"{date:%d%m}"

def update_sensor(sensor, shortdate, birthdays) -> None:
    state.set(var_name = sensor, value = None, new_attributes={})
    state.setattr(f"{sensor}.icon", "mdi:calendar-star")
    if shortdate in birthdays.keys():
        state.setattr("sensor.today_birthdays.icon", "mdi:calendar-star")
        for evt in birthdays[shortdate]:
            log.debug(f"{shortdate} - it is {evt["name"]} birthday ({evt["age"]})")
            state.setattr(f"{sensor}.{evt["name"]}", evt["age"])

""" Everyday at 00:01 """
@time_trigger("startup", "cron(1 0 * * *)")
def get_birthdays() -> None:
    contacts = []
    today = datetime.datetime.now()
    tomorrow = today + datetime.timedelta(days = 1)

    myShortToday = date2stringshort(today)
    myShortTomorrow = date2stringshort(tomorrow)

    for contact in myconfig.contacts:
        contacts.append(Contact(contact["name"], contact["bd"]))

    birthdays = {}
    for contact in contacts:
        if not contact.birthdate in birthdays.keys():
            birthdays[contact.birthdate] = []
        birthdays[contact.birthdate].append({"name": contact.name, "age": contact.age})

    update_sensor("sensor.today_birthdays",    myShortToday,    birthdays)
    update_sensor("sensor.tomorrow_birthdays", myShortTomorrow, birthdays)