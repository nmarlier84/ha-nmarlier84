""" https://hacs-pyscript.readthedocs.io/en/latest/reference.html#configuration """

# Configuration
"""
<config>/configuration.yaml
pyscript: !include pyscript.yaml


<config>/pyscript.yaml
allow_all_imports: true
apps:
    get_birthdays:
        max_users: 3
        users:
            - name: user1
            bd: ddmmyy
            - name: user2
            bd: ddmm


=> pyscript.app_config
[
    {"name": "user1", ddmmyy},
    {"name": "user2", ddmm},
],
"""

# Third Part modules
import datetime
# import sys

# Internal modules
"""
if "/config/pyscript_modules" not in sys.path:
    sys.path.append("/config/pyscript_modules")

import myconfig
"""

"""
class Contact:
    def __init__(self, name, bd) -> None:
        self.name = name
        self.birthdate = bd[:4]
        if len(bd) == 6 :
            self.age = str(datetime.datetime.now().year - int(f"19{bd[-2:]}"))
        else:
            self.age = "unknown"
"""

def date2stringshort(date) -> str:
    assert isinstance(date, datetime.datetime)
    return f"{date:%d%m}"

def flush_sensor(sensor, max_users) -> None:
    for i in range(0, max_users):
        state.setattr(f"{sensor}.user_{i}_name", "unknown")
        state.setattr(f"{sensor}.user_{i}_age", "unknown")

""" Everyday at 00:01 """
@time_trigger("startup", "cron(1 0 * * *)")
def get_birthdays() -> None:

    indexToday = 0
    indexTomorrow = 0
    max_users = pyscript.app_config["max_users"]

    today = datetime.datetime.now()
    tomorrow = today + datetime.timedelta(days = 1)
    myShortToday = date2stringshort(today)
    myShortTomorrow = date2stringshort(tomorrow)

    flush_sensor(f"sensor.today_birthdays", max_users)
    flush_sensor(f"sensor.tomorrow_birthdays", max_users)

    for contact in pyscript.app_config["users"]:
        short_bd = date2stringshort(contact["bd"])
        if short_bd == myShortToday:
            state.setattr(f"sensor.today_birthdays.user_{indexToday}_name", contact["name"])
            if len(short_bd) == 6 :
                state.setattr(f"sensor.today_birthdays.user_{indexToday}_age", str(datetime.datetime.now().year - int(f"19{bd[-2:]}")))
            indexToday = (indexToday + 1) % max_users
        if short_bd == myShortTomorrow:
            state.setattr(f"sensor.tomorrow_birthdays.user_{indexTomorrow}_name", contact["name"])
            if len(short_bd) == 6 :
                state.setattr(f"sensor.today_birthdays.user_{indexToday}_age", str(datetime.datetime.now().year - int(f"19{bd[-2:]}")))           
            indexTomorrow = (indexTomorrow + 1) % max_users