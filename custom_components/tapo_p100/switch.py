from PyP100 import PyP100
import logging
from typing import Any, Dict
from typing_extensions import Required
import voluptuous as vol
import json
from homeassistant.components.switch import PLATFORM_SCHEMA, SwitchDevice
from homeassistant.const import CONF_IP_ADDRESS, CONF_USERNAME, CONF_NAME, CONF_PASSWORD
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.restore_state import RestoreEntity

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "tapo_p100"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_IP_ADDRESS): cv.string,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Perform the setup for Switchbot_press devices."""
    name = config.get(CONF_NAME)
    ip_address = config.get(CONF_IP_ADDRESS)
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)
    add_entities([Tapo_P100(ip_address, name, username, password)])

class Tapo_P100(SwitchDevice, RestoreEntity):
    def __init__(self, ip_address, name, username, password) -> None:
            self.state = None
            self._last_run_success = None
            self.ip_address = ip_address 
            self.name = name
            self.username = username
            self.password = password
            self._device = PyP100.P100(ip_address, username, password)
            self._device.handshake()
            self._device.login()

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
         
    def turn_on(self) -> None:
        self._device.turnOn()
  
    def turn_off(self) -> None:
        self._device.turnOff
    @property
    def assumed_state(self) -> bool:
        return False
    @property
    def is_on(self) -> bool:
        return json.loads(self._device.getDeviceInfo())["results"]["device_on"]
    @property
    def is_off(self) -> bool:
        return json.loads(self._device.getDeviceInfo())["results"]["device_on"]
    @property
    def name(self) -> str:
        return self._name    
 