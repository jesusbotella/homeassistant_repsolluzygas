import logging

from homeassistant.helpers.entity import Entity
from homeassistant.const import (
    DEVICE_CLASS_POWER,
    ENERGY_KILO_WATT_HOUR
)

from .constants import DOMAIN
from contracts import RepsolGasSensor, RepsolLuzSensor

_LOGGER = logging.getLogger(__name__)

## Setup Method
def setup_platform(hass, config, add_entities, discovery_info=None):
  repsolManagerInstance = hass.data[DOMAIN]['repsolManagerInstance']

  contract_sensors = []
  for contract in repsolManagerInstance.getContracts():
    _LOGGER.info('Adding sensor for {contract_id}'.format(contract_id=contract.getContractId()))

    if contract.getContractType() == 'LUZ':
      contract_sensors.append(RepsolLuzSensor(contract))
    elif contract.getContractType() == 'GAS':
      contract_sensors.append(RepsolGasSensor(contract))

  add_entities(contract_sensors)
