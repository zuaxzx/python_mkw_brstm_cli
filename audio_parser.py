import os
import shutil
import pathlib

from pydub import AudioSegment

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
               brstm_patch_value: int = 100
  ) -> None:
    self.infile = pathlib.Path(infile).absolute()
    self.outfile = outfile
    
    self.speed_increase = speed_increase
    self.db_increase = db_increase
    self.cut_offset_start = cut_offset_start
    self.cut_offset_end = cut_offset_end
    
    if channels % 2:
      raise Exception("Unequal amount of channels is not supported!")
    
    self.channels = channels    
    self.brstm_patch_value = brstm_patch_value
  
  def apply_config_to_wav(self) -> None:
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
      slice_offset_end = int(self.cut_offset_start * 1000)
    
    # Slice / Cut audio
    cut_audio = audio[slice_offset_start:slice_offset_end]
    
    # Check if channels are default value
    if self.channels > 2:
      # Split left and right channel to mono AudioSegment instances
      stereo_channels = cut_audio.split_to_mono()
      
      # Define empty container with channels to fill
      multi_channels: AudioSegment = []
      # Iter the amount of channels needed (divided by 2 since left and right)
      for _ in range(0, int(self.channels / 2)):
        # Add channels to list
        multi_channels += stereo_channels
      
      # Create new AudioSegment instance with all channels
      cut_audio = AudioSegment.from_mono_audiosegments(*multi_channels)
    
    # Export the edited wave file - ToDo: Remove debug name
    cut_audio.export("./exported_infile.wav", format="wav")
  
  def convert(self) -> None:
    self.apply_config_to_wav()
    
    # convert temp file to brstm
    
    # delete temp file
  