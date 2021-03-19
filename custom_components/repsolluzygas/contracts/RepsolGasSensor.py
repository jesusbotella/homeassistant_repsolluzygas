from .RepsolContractSensor import RepsolContractSensor

class RepsolGasSensor(RepsolContractSensor):
  @property
  def name(self):
    """Return the name of the sensor."""
    return '{contract_type} Last Invoice'.format(
      contract_type=self.contract.getContractType().capitalize()
    )

  @property
  def icon(self):
      """Icon to use in the frontend, if any."""
      return 'mdi:fire'

  @property
  def state(self):
      """Return the state of the sensor."""
      return self.contract.getLastInvoice()['total_power_kwh']

  @property
  def device_state_attributes(self):
      """Return the state attributes."""
      return self.contract.getLastInvoice()
