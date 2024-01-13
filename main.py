import argparse
import pathlib

from src.config_parser import ConfigParser
from src.yt_download import convert_mp4_to_wav, dl_mp4_from_yt
from src.audio_parser import AudioFileParser
from src.config import init_config, GeneralConfiguration
from src.brstm_patcher import patch_brstm

def append_files(wav_file: str, args: argparse.Namespace, files: list[AudioFileParser], config: GeneralConfiguration) -> None:

  # Track (normal and final)
  if args.track in config.track_mapping:
    
    # Determine channels using the mapping
    channels = config.channel_mapping.get(args.track, 2)
    
    if channels > 2:
      config.normal_track_abrev = config.normal_track_abrev.upper()
      config.final_track_abrev = config.final_track_abrev.upper()
    
    # Get the outfile name (no ending since wav and brstm are needed)
    brstm_file_n = config.track_mapping.get(args.track).replace('*', config.normal_track_abrev)
    brstm_file_f = config.track_mapping.get(args.track).replace('*', config.final_track_abrev)
    
    # Append normal lap audio
    files.append(
      AudioFileParser(
        infile=wav_file,
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
        infile=wav_file,
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
  elif args.track in config.misc_mapping:
    # Determine channels using the mapping
    channels = config.channel_mapping.get(args.track, 2)
    
    # Get the outfile name (no ending since wav and brstm are needed)
    misc_file = config.misc_mapping.get(args.track)
    
    # Append normal lap audio
    files.append(
      AudioFileParser(
        infile=wav_file,
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


def download_url(args: argparse.Namespace, config: GeneralConfiguration) -> str:
  temp_mp4 = pathlib.Path(config.temp_dir).joinpath("download.mp4")
  wav_file = pathlib.Path(config.temp_dir).joinpath("download.wav")
  dl_mp4_from_yt(args.audio, temp_mp4)
  convert_mp4_to_wav(temp_mp4, wav_file)
  temp_mp4.unlink()
  
  return wav_file

def convert_to_brstm(args: argparse.Namespace) -> None:
  config = init_config()
  
  files: list[AudioFileParser] = []
  
  if args.type == "url":
    wav_file = download_url(args, config)
  elif args.type == "wav":
    wav_file = args.audio
  else:
    raise Exception("Wrong type to convert given!")
  
  append_files(wav_file, args, files, config)
  
  for audio_parser in files:
    # Convert audio
    audio_parser.convert(config.out_dir, config.temp_dir)

def brstm_patch(args: argparse.Namespace) -> None:
  patch_brstm(args.brstm_file, args.brstm_patch)

def main() -> None:
  # Define arguments using the Argument parser
  parser = argparse.ArgumentParser()
  
  subparsers = parser.add_subparsers(required=True)
  
  parser_convert = subparsers.add_parser("convert")
  parser_patch = subparsers.add_parser("patch")
  
  parser_convert.add_argument('track', type=str, help='Track to convert to')
  parser_convert.add_argument('type', type=str, choices=["wav", "url"], help='Audio type. Valid options: "wav", "url" (YouTube)')
  parser_convert.add_argument('audio', type=str, help='Input wav file or youtube url')
  
  parser_convert.add_argument('--db_increase', type=float, default=0.0, help='Increase of db for the wav/brstm', required=False)
  parser_convert.add_argument('--cut_start', type=float, help='Time in seconds where to start [from frame 0]', required=False)
  parser_convert.add_argument('--cut_end', type=float, help='Time in seconds where to end [from frame 0]', required=False)
  parser_convert.add_argument('--speed', type=float, default=1, help='Speed increase of normal lap', required=False)
  parser_convert.add_argument('--fcut_start', type=float, help='Time in seconds where to start (final lap) [from frame 0]', required=False)
  parser_convert.add_argument('--fcut_end', type=float, help='Time in seconds where to end (final lap) [from frame 0]', required=False)
  parser_convert.add_argument('--fspeed', type=float, default=1, help='Speed increase of final lap', required=False)
  parser_convert.add_argument('--brstm_patch', type=int, default=100, help='Brstm volume value patch [0 - 127]', required=False)
  parser_convert.set_defaults(func=convert_to_brstm)
  
  parser_patch.add_argument('brstm_file', type=str, help='BRSTM file to patch')
  parser_patch.add_argument('brstm_patch', type=int, default=100, help='Brstm volume value patch [0 - 127]')
  parser_patch.set_defaults(func=brstm_patch)
  
  # Parse arguments defined
  args = parser.parse_args()
  args.func(args)
  
if __name__ == '__main__':
  main()
  
  

