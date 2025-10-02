import aiohttp
import async_timeout

class ZewaAPI:
    def __init__(self, ip, username, password):
        self._ip = ip
        self._auth = aiohttp.BasicAuth(username, password)

    async def _request(self, endpoint, method="get", data=None):
        url = f"http://{self._ip}/api/rest/{endpoint}"
        async with aiohttp.ClientSession(auth=self._auth) as session:
            with async_timeout.timeout(10):
                if method == "get":
                    async with session.get(url) as resp:
                        return await resp.json()
                else:
                    async with session.post(url, data=data) as resp:
                        return await resp.json()

    async def reset_messages(self): return await self._request("6300", "post")
    async def close_leakage(self): return await self._request("5100", "post")
    async def open_leakage(self): return await self._request("5200", "post")
    async def start_sleep(self): return await self._request("5400", "post")
    async def stop_sleep(self): return await self._request("5500", "post")
    async def start_vacation(self): return await self._request("5700", "post")
    async def stop_vacation(self): return await self._request("5800", "post")
    async def start_microleak_test(self): return await self._request("5C00", "post")
    async def start_lernmodus(self): return await self._request("5D00", "post")

    async def read_absence_limits(self): return await self._request("5E00")
    async def write_absence_limits(self, payload): return await self._request(payload, "post")
    async def set_leakage_settings(self, payload): return await self._request(payload, "post")
    async def set_sleep_duration(self, value): return await self._request(f"5300{value:02X}", "post")
    async def read_sleep_duration(self): return await self._request("6600")
    async def set_vacation_type(self, value): return await self._request(f"5600{value:02X}", "post")
    async def read_lernmodus_status(self): return await self._request("6400")
    async def read_microleak_setting(self): return await self._request("6500")
    async def set_microleak_setting(self, value): return await self._request(f"5B00{value:02X}", "post")
    async def read_absence_time(self): return await self._request("6000")
    async def write_absence_time(self, payload): return await self._request(payload, "post")
    async def delete_absence_time(self, value): return await self._request(f"6200{value:02X}", "post")

    async def get_device_type(self): return await self._request("FF00")
    async def get_serial_number(self): return await self._request("0600")
    async def get_firmware(self): return await self._request("0100")
    async def get_install_date(self): return await self._request("0E00")
    async def total_water(self): return await self._request("2800")
    async def read_datetime(self): return await self._request("5900")
    async def set_datetime(self, payload): return await self._request(payload, "post")

    async def daily_stats(self, payload): return await self._request(payload)
    async def weekly_stats(self, payload): return await self._request(payload)
    async def monthly_stats(self, payload): return await self._request(payload)
    async def yearly_stats(self, payload): return await self._request(payload)
