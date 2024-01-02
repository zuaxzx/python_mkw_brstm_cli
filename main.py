import argparse
import subprocess
import pathlib

from config_parser import ConfigParser

from audio import AudioFileParser

def init_config() -> ConfigParser:
  # Parse yaml config
  return ConfigParser("./config.yml")

def init(container: list, args: argparse.Namespace) -> None:
  config_parser = init_config()
  
  # Define mapping dicts (2 mappings since tracks need normal and final)
  track_mapping = config_parser.get("tracks.brstm_track_mapping", dict)
  misc_mapping = config_parser.get("tracks.brstm_misc_mapping", dict)
  
  # Get the track abrev for normal and final lap
  normal_track_abrev = config_parser.get("tracks.abrev.normal")
  final_track_abrev = config_parser.get("tracks.abrev.final")
  
  track_abrev = args.track
  outfiles = []
  
  if track_abrev in track_mapping:
    brstm_file_n = f"{track_mapping.get(args.track).replace('*', normal_track_abrev)}.brstm"
    brstm_file_f = f"{track_mapping.get(args.track).replace('*', final_track_abrev)}.brstm"
    outfiles = [brstm_file_n, brstm_file_f]
    
  elif track_abrev in misc_mapping:
    misc_file = misc_mapping.get(args.track)
    outfiles = [brstm_file_n, brstm_file_f]
  
  else:
    raise KeyError(f"Given track {args.track} does not exist!")
  
  files: list[AudioFileParser] = []
  
  for outfile in outfiles:
    files.append(
      AudioFileParser(
        infile=args.wav_file,
        outfile=outfile,
      )
    )
  
  for audio_parser in files:
  
    print(audio_parser.infile)
    print(audio_parser.outfile)
    print(audio_parser.speed_increase)
    print(audio_parser.db_increase)
    print(audio_parser.cut_offset_start)
    print(audio_parser.cut_offset_end)
    print(audio_parser.brstm_patch_value)

def main() -> None:
  # Define arguments using the Argument parser
  parser = argparse.ArgumentParser()  
  
  parser.add_argument('track', type=str, help='Track to convert to')
  parser.add_argument('wav_file', type=str, help='Input wav file')
  
  # Parse arguments defined
  args = parser.parse_args()
  
  container = list()
  init(container, args)
  
  
  


if __name__ == '__main__':
  main()
  
  

