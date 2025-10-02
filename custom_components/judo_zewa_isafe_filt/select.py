from homeassistant.components.select import SelectEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    api = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        VacationTypeSelect(api),
        MicroLeakSelect(api),
    ], True)

class VacationTypeSelect(SelectEntity):
    def __init__(self, api):
        self._api = api
        self._attr_name = "Vacation Mode Type"
        self._attr_options = ["Off","U1","U2","U3"]
        self._attr_current_option = "Off"

    async def async_select_option(self, option: str):
        value = self._attr_options.index(option)
        await self._api.set_vacation_type(value)
        self._attr_current_option = option
        self.async_write_ha_state()

class MicroLeakSelect(SelectEntity):
    def __init__(self, api):
        self._api = api
        self._attr_name = "Micro-Leak Mode"
        self._attr_options = ["Off","Report","Report+Close"]
        self._attr_current_option = "Off"

    async def async_select_option(self, option: str):
        value = self._attr_options.index(option)
        await self._api.set_microleak_setting(value)
        self._attr_current_option = option
        self.async_write_ha_state()

    async def async_update(self):
        data = await self._api.read_microleak_setting()
        if "data" in data:
            idx = int(data["data"],16)
            if idx < len(self._attr_options):
                self._attr_current_option = self._attr_options[idx]
