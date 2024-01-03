import argparse
import subprocess
import pathlib

from config_parser import ConfigParser

from audio_parser import AudioFileParser

def init_config() -> ConfigParser:
  # Parse yaml config
  return ConfigParser("./config.yml")

def run(container: list, args: argparse.Namespace) -> None:
  config_parser = init_config()
  
  # Define mapping dicts (2 mappings since tracks need normal and final)
  track_mapping = config_parser.get("tracks.brstm_track_mapping", dict)
  misc_mapping = config_parser.get("tracks.brstm_misc_mapping", dict)
  
  # Get the track abrev for normal and final lap
  normal_track_abrev = config_parser.get("tracks.abrev.normal")
  final_track_abrev = config_parser.get("tracks.abrev.final")
  
  track_abrev = args.track
  outfiles = []
  
  # Track (normal and final)
  if track_abrev in track_mapping:
    brstm_file_n = f"{track_mapping.get(args.track).replace('*', normal_track_abrev)}.brstm"
    brstm_file_f = f"{track_mapping.get(args.track).replace('*', final_track_abrev)}.brstm"
    outfiles = [brstm_file_n, brstm_file_f]
  
  # Misc (normal)
  elif track_abrev in misc_mapping:
    misc_file = misc_mapping.get(args.track)
    outfiles = [misc_file]
  
  # Not available
  else:
    raise KeyError(f"Given track {args.track} does not exist!")
  
  files: list[AudioFileParser] = []
  
  for outfile in outfiles:
    
    channels = 2
    
    files.append(
      AudioFileParser(
        infile=args.wav_file,
        outfile=outfile,
        speed_increase=1,
        db_increase=args.db_increase,
        cut_offset_start=args.cut_start,
        cut_offset_end=args.cut_end,
        channels=channels,
        brstm_patch_value=args.brstm_patch
      )
    )
  
  for audio_parser in files:
    audio_parser.convert()

def main() -> None:
  # Define arguments using the Argument parser
  parser = argparse.ArgumentParser()  
  
  parser.add_argument('track', type=str, help='Track to convert to')
  parser.add_argument('wav_file', type=str, help='Input wav file')
  
  parser.add_argument('--db_increase', type=float, default=0.0, help='Increase of db for the wav/brstm', required=False)
  parser.add_argument('--cut_start', type=float, help='Time in seconds where to start [from frame 0]', required=False)
  parser.add_argument('--cut_end', type=float, help='Time in seconds where to end [from frame 0]', required=False)
  parser.add_argument('--brstm_patch', type=int, default=100, help='Brstm volume value patch [0 - 127]', required=False)
  
  # Parse arguments defined
  args = parser.parse_args()
  
  container = list()
  run(container, args)
  
  
  


if __name__ == '__main__':
  main()
  
  

