"""
Sensor for SigFox devices.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/sensor.sigfox/
"""
import logging
import datetime
import json
import voluptuous as vol
import requests

import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = datetime.timedelta(seconds=30)
API_URL = 'https://backend.sigfox.com/api/'
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
CONF_API_LOGIN = 'login'
CONF_API_PASSWORD = 'password'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_API_LOGIN): cv.string,
    vol.Required(CONF_API_PASSWORD): cv.string,
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the Tube sensor."""
    login = config[CONF_API_LOGIN]
    password = config[CONF_API_PASSWORD]
    sigfox = SigfoxData(login, password)
    auth = sigfox.auth
    devices = sigfox.devices

    sensors = []
    for device in devices:
        sensors.append(SigfoxDevice(device, auth))
    add_devices(sensors, True)


def epoch_to_datetime(epoch_time):
    """Take an ms since epoch and return datetime string."""
    value = datetime.datetime.fromtimestamp(epoch_time)
    return value.strftime(TIME_FORMAT)


class SigfoxData(object):
    """Class for interacting with the SigFox API."""
    def __init__(self, login, password):
        self._auth = requests.auth.HTTPBasicAuth(login, password)
        r = requests.get(API_URL + 'devicetypes', auth=self._auth)
        if r.status_code != 200:
            _LOGGER.warning(
                "Unable to login to Sigfox API: " + str(r.status_code))
        self._device_types = []
        self.get_device_types()
        self._devices = []
        self.get_devices()

    def get_device_types(self):
        """Get a list of device types."""
        url = API_URL + 'devicetypes'
        r = requests.get(url, auth=self._auth)
        for device in json.loads(r.text)['data']:
            self._device_types.append(device['id'])

    def get_devices(self):
        """Get the id of each device owned."""
        for unique_type in self._device_types:
            url = API_URL + 'devicetypes/' + unique_type + '/devices'
            r = requests.get(url, auth=self._auth)
            devices = json.loads(r.text)['data']
            for device in devices:
                self._devices.append(device['id'])

    @property
    def auth(self):
        """Return the authentification."""
        return self._auth

    @property
    def devices(self):
        """Return the list of devices."""
        return self._devices


class SigfoxDevice(Entity):
    """Class for single SigFox device, init with id from devices."""
    def __init__(self, device_id, auth):

        self._device_id = device_id
        self._auth = auth
        self._data = {}
        self._name = 'sigfox_' + device_id
        self._state = None

    def get_last_message(self):
        """Return the last message from a device."""
        url = API_URL + 'devices/' + self._device_id + '/messages?limit=1'
        r = requests.get(url, auth=self._auth)
        data = json.loads(r.text)['data'][0]
        payload = bytes.fromhex(data['data']).decode('utf-8')
        lat = data['rinfos'][0]['lat']
        lng = data['rinfos'][0]['lng']
        snr = data['snr']
        epoch_time = data['time']
        return {'lat': lat,
                'lng': lng,
                'payload': payload,
                'snr': snr,
                'time': epoch_to_datetime(epoch_time)
                }

    def update(self):
        """Fetch the latest message data."""
        self._data = self.get_last_message()
        self._state = self._data['payload']

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def device_state_attributes(self):
        """Return other details about the sensor state."""
        return self._data
