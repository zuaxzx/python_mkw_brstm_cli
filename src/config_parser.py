import yaml
import typing

class ConfigParser:
  file = None
  yml_stream = None
  
  def __init__(self, infile: str) -> None:
    # Set infile
    self.file = infile
    
    # Safe load yaml
    with open(self.file, "r") as f:
      self.yml_stream= yaml.safe_load(f)
      
  def get(self, mpath: str, init_type: typing.Any = str) -> typing.Any:
    # mpath: "a.b.c"
    
    # All sections to parse in correct order
    sections = mpath.split(".")
    # Current yaml index item to parse
    item = self.yml_stream
        
    # Parse data recursively
    for section in sections:
      item = item.get(section)
        
    # Return initialized item
    return init_type(item)
