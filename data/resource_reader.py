from enum import Enum
from util.errors import get_FNF_error
import logging
import os
import re
import yaml

logger = logging.getLogger(__name__)
logging.basicConfig(level=os.getenv('LOG_LEVEL'))

elements_path = "OxygenNotIncluded_Data/StreamingAssets/elements"
strings_path  = "OxygenNotIncluded_Data/StreamingAssets/strings/strings_template.pot"

def get_element_name_translator(elementName: str):
  return f'msgctxt\s"{elementName}"'+r'[.\n]?msgid\s"(?:<link=\\".*\\">)?([^<>"]*)(?:<\/link>)?"'

class State(Enum):
  GAS     = "gas"
  LIQUID  = "liquid"
  SOLID   = "solid"
  SPECIAL = "special"

def read_file(file: str): 
  try:
    with open(file, mode='r') as unprocessed_stream: 
      try: 
        with open(f"{os.getenv('ONI_PATH')}/{strings_path}", mode='r') as strings_stream:
          content = strings_stream.read()
          elements: dict = yaml.safe_load(unprocessed_stream)['elements']
          for element in elements: 
            # resolve element name
            logger.debug(f"Looking for localisation name for {element['elementId']}")
            regex = get_element_name_translator(element['localizationID'])
            logger.debug(f"Attempting to search for localizationID {element['localizationID']} with regex {regex}")
            search_result = re.search(regex, content)
            if search_result is not None: 
              element['elementId'] = search_result.groups()[0]
              logger.debug(f"Found suitable localisation name for {element['elementId']}: {search_result.groups()[0]}")
            else: 
              logger.warning(f"Did not find a localisation name for {element['elementId']}")
      except FileNotFoundError: 
        logger.error(get_FNF_error(f"{os.getenv('ONI_PATH')}/{strings_path}"))
  except FileNotFoundError: 
    logger.error(get_FNF_error(file))

      
  return elements

def read_elements(state: State): 
  file = f"{os.getenv('ONI_PATH')}/{elements_path}/{state.value}.yaml"
  return read_file(file)

def find_element(element_name: str, collection): 
  print(f"Looking for {element_name}...")    
  try:
    return list(filter(lambda element: element_name.lower() in element.get("elementId").lower(), collection))[0]    
  except IndexError:
    logger.error(f"Did not find an element with name: {element_name.lower()}")

class Elements(): 
  def __init__(self): 
    self.gas     = read_elements(State.GAS)
    self.liquid  = read_elements(State.LIQUID)
    self.solid   = read_elements(State.SOLID)
    self.special = read_elements(State.SPECIAL)

  def get_element_by_name_and_state(self, name: str, state: State):
    elementId = f"{name.capitalize()}"

    if state == State.GAS:
      element = find_element(elementId, self.gas)
    elif state == State.LIQUID:
      element = find_element(elementId, self.liquid)
    elif state == State.SOLID:
      element = find_element(elementId, self.solid)
    else: # special
      element = find_element(elementId, self.special)
    
    return element

