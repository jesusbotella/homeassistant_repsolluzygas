class RepsolContractSensor(Entity):
  """Implementation of the Repsol Contract Sensor"""

  def __init__(self, contract):
    """Initialize the sensor."""
    self.contract = contract

  @property
  def unique_id(self):
      """Return an unique ID."""
      return '{contract_type}{contract_id}'.format(
        contract_type=self.contract.getContractType(),
        contract_id=self.contract.getContractId()
      ).lower()

  @property
  def device_class(self):
      """Return the device class of this entity."""
      return DEVICE_CLASS_POWER

  @property
  def unit_of_measurement(self):
      """Return the unit of measurement of this entity, if any."""
      return ENERGY_KILO_WATT_HOUR

  def update(self):
      """Get the latest data from the DHT and updates the states."""
      _LOGGER.info('Updating sensor for {contract_id}'.format(contract_id=self.contract.getContractId()))
      self.contract.update()
