import pathlib
import subprocess
import os

from brstm_patcher import patch_brstm

from pydub import AudioSegment, effects

class AudioFileParser:
  
  infile: str or None = None
  outfile: str or None = None
  
  def __init__(self, 
               infile: str,
               outfile: str,
               speed_increase: float = 1,
               db_increase: float = 0,
               cut_offset_start: float or None = 0,
               cut_offset_end: float or None = 0,
               channels: int = 2,
               # Not used for now - 8 bit signed value 
               brstm_patch_value: int = 0
  ) -> None:
    self.infile = pathlib.Path(infile).absolute()
    self.brstm_outfile = f"{outfile}.brstm"
    self.temp_wav_outfile = f"{outfile}.wav"
        
    self.speed_increase = speed_increase
    self.db_increase = db_increase
    self.cut_offset_start = cut_offset_start
    self.cut_offset_end = cut_offset_end
    
    if channels % 2:
      raise Exception("Unequal amount of channels is not supported!")
    
    self.channels = channels    
    self.brstm_patch_value = brstm_patch_value
  
  def apply_config_to_wav(self, temp_wav_outfile) -> None:
    audio: AudioSegment = AudioSegment.from_file(self.infile, format="wav")
    
    # Apply db gain
    if self.db_increase:
      audio += self.db_increase
    
    # Define default offset (in case not defined)
    slice_offset_start = 0
    slice_offset_end = len(audio)
    
    # Define start offset
    if self.cut_offset_start:
      slice_offset_start = int(self.cut_offset_start * 1000)
    
    # Define end offset
    if self.cut_offset_end:
      slice_offset_end = int(self.cut_offset_end * 1000)
    
    # Slice / Cut audio
    cut_audio = audio[slice_offset_start:slice_offset_end]
        
    # Speed up audio
    if self.speed_increase != 1:
      cut_audio = effects.speedup(cut_audio, self.speed_increase)
    
    # Check if channels are default value
    if self.channels > 2:
      # Split left and right channel to mono AudioSegment instances
      stereo_channels = cut_audio.split_to_mono()
      
      # Define empty container with channels to fill
      multi_channels: AudioSegment = []
      # Iter the amount of channels needed (divided by 2 since left and right - stereo)
      # For example (4 channels): 1 = left, 2 = right, 3 left, 4 = right
      for _ in range(0, int(self.channels / 2)):
        # Add channels to list
        multi_channels += stereo_channels
      
      # Create new AudioSegment instance with all channels
      cut_audio = AudioSegment.from_mono_audiosegments(*multi_channels)
    
    # Export the edited wave file - ToDo: Remove debug name
    cut_audio.export(temp_wav_outfile, format="wav")
  
  def convert(self, out_dir: str, temp_dir: str) -> None:
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(temp_dir, exist_ok=True)
    
    temp_wav_outfile = pathlib.Path(temp_dir).joinpath(os.path.basename(self.temp_wav_outfile))
    brstm_outfile = pathlib.Path(out_dir).joinpath(os.path.basename(self.brstm_outfile))
    
    # ToDo: Implement logger instead
    print("Generating [temp]:", temp_wav_outfile)
    self.apply_config_to_wav(temp_wav_outfile)
    
    # Define outfile
    print("Generating:", brstm_outfile)
    cmd = ["VGAudioCli", "-c", "-i", temp_wav_outfile, "-o", brstm_outfile]
    
    if self.brstm_patch_value:
      print("Apply brstm patch...")
      patch_brstm(brstm_outfile, self.brstm_patch_value)
      print("Done!")
    
    # convert temp file to brstm
    subprocess.check_output(cmd)