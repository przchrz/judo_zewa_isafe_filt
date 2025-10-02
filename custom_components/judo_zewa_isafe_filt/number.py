from homeassistant.components.number import NumberEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    api = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([SleepDurationNumber(api)], True)

class SleepDurationNumber(NumberEntity):
    def __init__(self, api):
        self._api = api
        self._attr_name = "Sleep Duration"
        self._attr_native_unit_of_measurement = "h"
        self._attr_native_min_value = 1
        self._attr_native_max_value = 10
        self._attr_native_step = 1
        self._state = None

    @property
    def native_value(self): return self._state

    async def async_set_native_value(self, value: float):
        await self._api.set_sleep_duration(int(value))
        self._state = value
        self.async_write_ha_state()

    async def async_update(self):
        data = await self._api.read_sleep_duration()
        if "data" in data:
            self._state = int(data["data"],16)
