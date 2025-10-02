from homeassistant.components.switch import SwitchEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    api = hass.data[DOMAIN][entry.entry_id]
    entities = [
        LeakageSwitch(api),
        SleepSwitch(api),
        VacationSwitch(api),
    ]
    async_add_entities(entities, True)

class LeakageSwitch(SwitchEntity):
    def __init__(self, api):
        self._api = api
        self._attr_name = "Leakage Protection"
        self._attr_is_on = False

    async def async_turn_on(self):
        await self._api.open_leakage()
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self):
        await self._api.close_leakage()
        self._attr_is_on = False
        self.async_write_ha_state()

class SleepSwitch(SwitchEntity):
    def __init__(self, api):
        self._api = api
        self._attr_name = "Sleep Mode"
        self._attr_is_on = False

    async def async_turn_on(self):
        await self._api.start_sleep()
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self):
        await self._api.stop_sleep()
        self._attr_is_on = False
        self.async_write_ha_state()

class VacationSwitch(SwitchEntity):
    def __init__(self, api):
        self._api = api
        self._attr_name = "Vacation Mode"
        self._attr_is_on = False

    async def async_turn_on(self):
        await self._api.start_vacation()
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self):
        await self._api.stop_vacation()
        self._attr_is_on = False
        self.async_write_ha_state()
