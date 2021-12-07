from asyncio.exceptions import TimeoutError
from ipaddress import ip_address

import aiohttp.client_exceptions
from aiohttp import ClientSession
from aiohttp.client_exceptions import ContentTypeError
from requests.exceptions import RequestException


class BatMon:
    def __init__(self, batmon_ip):
        self.batmon_ip = batmon_ip
        try:
            ip_address(self.batmon_ip)
        except ValueError:
            raise ValueError('Not IPv4!')

    async def __request_info(self, api_method, ignore_timeout=False):
        async with ClientSession() as session:
            try:
                async with session.get('http://' + self.batmon_ip + api_method,
                                       timeout=5) as res:
                    if res.content_type == 'application/json':
                        json_data = await res.json()
                        return json_data
                    else:
                        return res.status
            except (TimeoutError,
                    ContentTypeError,
                    aiohttp.client_exceptions.ClientConnectorError):
                if ignore_timeout:
                    await session.close()
                else:
                    raise RequestException

    async def get_master_info(self):
        master_info = {'ip_address': self.batmon_ip}
        master_info.update(await self.__request_info('/getMasterInfo'))
        return master_info

    async def get_location(self):
        master_info = await self.get_master_info()
        return master_info['location']

    async def get_all_data(self):
        all_data = {}
        master_info = await self.get_master_info()
        all_data['master_info'] = master_info
        slaves_number = master_info['slaves']
        for battery in range(1, slaves_number + 1):
            battery_info = await self.__request_info('/getSlaveInfo={}'.format(battery))
            all_data[battery] = battery_info
        return all_data

    async def set_location(self, location):
        return await self.__request_info('/config?location={}'.format(location))

    async def set_slaves_number(self, slaves_number):
        return await self.__request_info('/config?slaves={}'.format(slaves_number))

    async def set_slave_address(self, slave_address):
        return await self.__request_info('/?set={}'.format(slave_address))

    async def factory_reset(self, save_mac=True):
        request = '/config?factory=Factory+reset'
        if save_mac:
            request += '&flag=Save+MAC'
        await self.__request_info(request, ignore_timeout=True)
