from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    api = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        DeviceTypeSensor(api),
        SerialNumberSensor(api),
        FirmwareSensor(api),
        InstallDateSensor(api),
        TotalWaterSensor(api),
        DailyStatsSensor(api),
        WeeklyStatsSensor(api),
        MonthlyStatsSensor(api),
        YearlyStatsSensor(api),
    ], True)

class DeviceTypeSensor(SensorEntity):
    def __init__(self, api): self._api = api; self._attr_name = "Device Type"
    async def async_update(self): data = await self._api.get_device_type(); self._attr_native_value = data.get("data")

class SerialNumberSensor(SensorEntity):
    def __init__(self, api): self._api = api; self._attr_name = "Serial Number"
    async def async_update(self): data = await self._api.get_serial_number(); self._attr_native_value = data.get("data")

class FirmwareSensor(SensorEntity):
    def __init__(self, api): self._api = api; self._attr_name = "Firmware"
    async def async_update(self): data = await self._api.get_firmware(); self._attr_native_value = data.get("data")

class InstallDateSensor(SensorEntity):
    def __init__(self, api): self._api = api; self._attr_name = "Installation Date"
    async def async_update(self): data = await self._api.get_install_date(); self._attr_native_value = data.get("data")

class TotalWaterSensor(SensorEntity):
    def __init__(self, api):
        self._api = api
        self._attr_name = "Total Water Usage"
        self._attr_native_unit_of_measurement = "L"
    async def async_update(self):
        data = await self._api.total_water()
        self._attr_native_value = int(data.get("data","0"),16) if "data" in data else None

class DailyStatsSensor(SensorEntity):
    def __init__(self, api):
        self._api = api
        self._attr_name = "Daily Water Statistics"
        self._state = None
        self._attr_extra_state_attributes = {}

    @property
    def native_value(self): return self._state
    @property
    def extra_state_attributes(self): return self._attr_extra_state_attributes

    async def async_update(self):
        today = datetime.date.today()
        # encode date in device’s expected format
        payload = f"FB00{today.day:02X}{today.month:02X}{today.year:04X}"
        data = await self._api.daily_stats(payload)
        if "data" in data:
            values = {}
            raw = data["data"]
            for i in range(0, len(raw), 8):
                block = raw[i:i+8]
                if len(block) == 8:
                    liters = int(block, 16)
                    values[f"slot_{i//8}"] = liters
            self._attr_extra_state_attributes = values
            self._state = sum(values.values())

class WeeklyStatsSensor(SensorEntity):
    def __init__(self, api):
        self._api = api
        self._attr_name = "Weekly Water Statistics"
        self._state = None
        self._attr_extra_state_attributes = {}

    @property
    def native_value(self): return self._state
    @property
    def extra_state_attributes(self): return self._attr_extra_state_attributes

    async def async_update(self):
        today = datetime.date.today()
        kw = today.strftime("%W")
        # encode date in device’s expected format
        payload = f"FC00{kw:02X}{today.year:04X}"
        data = await self._api.weekly_stats(payload)
        if "data" in data:
            values = {}
            raw = data["data"]
            for i in range(0, len(raw), 8):
                block = raw[i:i+8]
                if len(block) == 8:
                    liters = int(block, 16)
                    values[f"day_{i//8}"] = liters
            self._attr_extra_state_attributes = values
            self._state = sum(values.values())

class MonthlyStatsSensor(SensorEntity):
    def __init__(self, api):
        self._api = api
        self._attr_name = "Monthly Water Statistics"
        self._state = None
        self._attr_extra_state_attributes = {}

    @property
    def native_value(self): return self._state
    @property
    def extra_state_attributes(self): return self._attr_extra_state_attributes

    async def async_update(self):
        today = datetime.date.today()
        # encode date in device’s expected format
        payload = f"FD00{today.month:02X}{today.year:04X}"
        data = await self._api.monthly_stats(payload)
        if "data" in data:
            values = {}
            raw = data["data"]
            for i in range(0, len(raw), 8):
                block = raw[i:i+8]
                if len(block) == 8:
                    liters = int(block, 16)
                    values[f"day_{i//8+1}"] = liters
            self._attr_extra_state_attributes = values
            self._state = sum(values.values())

class YearlyStatsSensor(SensorEntity):
    def __init__(self, api):
        self._api = api
        self._attr_name = "Yearly Water Statistics"
        self._state = None
        self._attr_extra_state_attributes = {}

    @property
    def native_value(self): return self._state
    @property
    def extra_state_attributes(self): return self._attr_extra_state_attributes

    async def async_update(self):
        today = datetime.date.today()
        # encode date in device’s expected format
        payload = f"FE00{today.year:04X}"
        data = await self._api.yearly_stats(payload)
        if "data" in data:
            values = {}
            raw = data["data"]
            for i in range(0, len(raw), 8):
                block = raw[i:i+8]
                if len(block) == 8:
                    liters = int(block, 16)
                    values[f"month_{i//8+1}"] = liters
            self._attr_extra_state_attributes = values
            self._state = sum(values.values())
