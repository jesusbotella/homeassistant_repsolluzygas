class RepsolLuzSensor(RepsolContractSensor):
  @property
  def name(self):
    """Return the name of the sensor."""
    return '{contract_type} Energy Consumption'.format(
      contract_type=self.contract.getContractType().capitalize()
    )

  @property
  def icon(self):
      return 'mdi:flash'

  @property
  def state(self):
      """Return the state of the sensor."""
      return round(self.contract.getConsumption()['Total_kWh_Cons'], 1)

  @property
  def device_state_attributes(self):
      """Return the state attributes."""
      return self.contract.getConsumption()
