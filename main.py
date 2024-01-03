import argparse

from config_parser import ConfigParser

from audio_parser import AudioFileParser

def init_config() -> ConfigParser:
  # Parse yaml config
  return ConfigParser("./config.yml")

def run(args: argparse.Namespace) -> None:
  config_parser = init_config()
  
  # Define mapping dicts (2 mappings since tracks need normal and final)
  track_mapping = config_parser.get("tracks.brstm_track_mapping", dict)
  misc_mapping = config_parser.get("tracks.brstm_misc_mapping", dict)
  
  # Get channel track mapping
  channel_mapping = config_parser.get("tracks.multi_channel", dict)
  
  # Get the track abrev for normal and final lap
  normal_track_abrev: str = config_parser.get("tracks.abrev.normal")
  final_track_abrev: str = config_parser.get("tracks.abrev.final")
  
  files: list[AudioFileParser] = []
  
  # Track (normal and final)
  if args.track in track_mapping:
    
    # Determine channels using the mapping
    channels = channel_mapping.get(args.track, 2)
    
    if channels > 2:
      normal_track_abrev = normal_track_abrev.upper()
      final_track_abrev = final_track_abrev.upper()
    
    # Get the outfile name (no ending since wav and brstm are needed)
    brstm_file_n = track_mapping.get(args.track).replace('*', normal_track_abrev)
    brstm_file_f = track_mapping.get(args.track).replace('*', final_track_abrev)
    
    # Append normal lap audio
    files.append(
      AudioFileParser(
        infile=args.wav_file,
        outfile=brstm_file_n,
        speed_increase=args.speed,
        db_increase=args.db_increase,
        cut_offset_start=args.cut_start,
        cut_offset_end=args.cut_end,
        channels=channels,
        brstm_patch_value=args.brstm_patch
      )
    )
    
    # Append final lap audio
    files.append(
      AudioFileParser(
        infile=args.wav_file,
        outfile=brstm_file_f,
        speed_increase=args.fspeed,
        db_increase=args.db_increase,
        cut_offset_start=args.fcut_start or args.cut_start,
        cut_offset_end=args.fcut_end or args.fcut_end,
        channels=channels,
        brstm_patch_value=args.brstm_patch
      )
    )
      
  # Misc (normal)
  elif args.track in misc_mapping:
    # Determine channels using the mapping
    channels = channel_mapping.get(args.track, 2)
    
    # Get the outfile name (no ending since wav and brstm are needed)
    misc_file = misc_mapping.get(args.track)
    
    # Append normal lap audio
    files.append(
      AudioFileParser(
        infile=args.wav_file,
        outfile=misc_file,
        speed_increase=args.speed,
        db_increase=args.db_increase,
        cut_offset_start=args.cut_start,
        cut_offset_end=args.cut_end,
        channels=channels,
        brstm_patch_value=args.brstm_patch
      )
    )
  
  # Not available
  else:
    raise KeyError(f"Given track {args.track} does not exist!")
  
  out_dir = config_parser.get("output.dir")
  temp_dir = config_parser.get("output.temp_dir")
  for audio_parser in files:
    # Convert audio
    audio_parser.convert(out_dir, temp_dir)

def main() -> None:
  # Define arguments using the Argument parser
  parser = argparse.ArgumentParser()  
  
  parser.add_argument('track', type=str, help='Track to convert to')
  parser.add_argument('wav_file', type=str, help='Input wav file')
  
  parser.add_argument('--db_increase', type=float, default=0.0, help='Increase of db for the wav/brstm', required=False)
  parser.add_argument('--cut_start', type=float, help='Time in seconds where to start [from frame 0]', required=False)
  parser.add_argument('--cut_end', type=float, help='Time in seconds where to end [from frame 0]', required=False)
  parser.add_argument('--speed', type=float, default=1, help='Speed increase of normal lap', required=False)
  parser.add_argument('--fcut_start', type=float, help='Time in seconds where to start (final lap) [from frame 0]', required=False)
  parser.add_argument('--fcut_end', type=float, help='Time in seconds where to end (final lap) [from frame 0]', required=False)
  parser.add_argument('--fspeed', type=float, default=1, help='Speed increase of final lap', required=False)
  parser.add_argument('--brstm_patch', type=int, default=100, help='Brstm volume value patch [0 - 127]', required=False)
  
  # Parse arguments defined
  args = parser.parse_args()
  
  run(args)
  
if __name__ == '__main__':
  main()
  
  

