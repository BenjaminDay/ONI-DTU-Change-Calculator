from data.resource_reader import Elements, State
import logging

logger = logging.getLogger(__name__)

class Stats:
    def __init__(self, TC, SHC, mass, temp):
        self.k = TC #Thermal Conductivity
        self.c = SHC #Specific Heat Capacity
        self.m = mass #(kg)
        self.T = temp #starting(C)

    def tempChange(self, q_DTU):
        return(q_DTU / self.c) / (self.m * 1000)


class StatsBuilder: 
  def __init__(self, elements: Elements):
    self.elements = elements
    self.tempStats = Stats(-1, -1, -1, -274)

  
  def of(self, elementName: str, state: State):
    element = self.elements.get_element_by_name_and_state(elementName, state)
    self.tempStats.k = element['thermalConductivity']
    self.tempStats.c = element['specificHeatCapacity']
    return self

  def withMass(self, mass):
    self.tempStats.m = mass
    return self
  
  def at(self, temp):
    self.tempStats.T = temp
    return self

  def reset(self):
    self.tempStats = Stats(-1, -1, -1, -274)
    return self
  
  def build(self):
    if all(list(map(lambda key_value_pair: 
                    key_value_pair[0] == "T" or key_value_pair[1] > 0, # key_value_pair[0] == key, key_value_pair[1] == value
                    self.tempStats.__dict__.items()))) and self.tempStats.T > -274:
      stats = self.tempStats
      self.reset()
      return stats
    else:
      logger.error("Some values of the stats builder were not filled in.")
