from homeassistant.components.button import ButtonEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    api = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        MicroLeakTestButton(api),
        LernmodusStartButton(api),
        ResetMessageButton(api),
    ], True)

class MicroLeakTestButton(ButtonEntity):
    def __init__(self, api):
        self._api = api
        self._attr_name = "Micro-Leakage Test"

    async def async_press(self):
        await self._api.start_microleak_test()

class LernmodusStartButton(ButtonEntity):
    def __init__(self, api):
        self._api = api
        self._attr_name = "Start Lernmodus"

    async def async_press(self):
        await self._api.start_lernmodus()

class ResetMessageButton(ButtonEntity):
    def __init__(self, api):
        self._api = api
        self._attr_name = "Reset Messages"

    async def async_press(self):
        await self._api.reset_messages()
