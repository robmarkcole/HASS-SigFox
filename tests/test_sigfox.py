"""Tests for the sigfox sensor."""
import re
import requests_mock
import unittest

from homeassistant.components.sensor.sigfox import (
    API_URL, CONF_API_LOGIN, CONF_API_PASSWORD)
from homeassistant.setup import setup_component
from tests.common import get_test_home_assistant

VALID_CONFIG = {
    'sensor': {
        'platform': 'sigfox',
        CONF_API_LOGIN: 'foo',
        CONF_API_PASSWORD: 'ebcd1234'}}


class TestUkTransportSensor(unittest.TestCase):
    """Test the uk_transport platform."""

    def setUp(self):
        """Initialize values for this testcase class."""
        self.hass = get_test_home_assistant()
        self.config = VALID_CONFIG

    def tearDown(self):
        """Stop everything that was started."""
        self.hass.stop()

    def test_invalid_credentials(self):
        """Test for a valid credentials."""

        self.assertTrue(
            setup_component(self.hass, 'sensor', VALID_CONFIG))

        with requests_mock.Mocker() as mock_req:
            url = re.compile(API_URL + 'devicetypes')
            mock_req.get(url, text='{}', status_code=401)
            self.assertTrue(
                setup_component(self.hass, 'sensor', {'sensor': self.config}))
        assert len(self.hass.states.entity_ids()) == 0
#        state = self.hass.states.get('sensor.mock_file_test_filesizetxt')
#        assert state.state == '0.0'
#        assert state.attributes.get('bytes') == 4
