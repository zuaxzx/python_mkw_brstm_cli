import os
import pathlib

from src.config_parser import ConfigParser

from dataclasses import dataclass

@dataclass
class GeneralConfiguration:
  track_mapping: dict
  misc_mapping: dict
  channel_mapping: dict
  normal_track_abrev: str
  final_track_abrev: str
  out_dir: str
  temp_dir: str

def add_to_system_path(path: str) -> None:
  os.environ["PATH"] = f"{path}{os.pathsep}{os.environ['PATH']}"

def init_tools(config_parser: ConfigParser) -> None:
  
  c_audiovg = config_parser.get("tools.audiovg")
  c_ffmpeg = config_parser.get("tools.audiovg")
  
  if c_audiovg:
    audiovg = pathlib.Path(c_audiovg).resolve()
    add_to_system_path(audiovg)
  if c_ffmpeg:
    ffmpeg = pathlib.Path(c_ffmpeg).resolve()
    add_to_system_path(ffmpeg)
    
def init_config() -> GeneralConfiguration:
  # Parse yaml config
  config_parser = ConfigParser("./config/config.yml")

  # Init tools
  init_tools(config_parser)
  
  config = GeneralConfiguration(
    # Define mapping dicts (2 mappings since tracks need normal and final)
    config_parser.get("tracks.brstm_track_mapping", dict),
    config_parser.get("tracks.brstm_misc_mapping", dict),
    # Get channel track mapping
    config_parser.get("tracks.multi_channel", dict),
    # Get the track abrev for normal and final lap
    config_parser.get("tracks.abrev.normal"),
    config_parser.get("tracks.abrev.final"),
    # Get output and temp directory
    config_parser.get("output.dir"),
    config_parser.get("output.temp_dir")
  )
  
  return config
  
  
  
  

