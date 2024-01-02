
class AudioFileParser:
  
  infile: str or None = None
  outfile: str or None = None
  
  def __init__(self, 
               infile: str,
               outfile: str,
               speed_increase: float = 1,
               db_increase: float = 0,
               cut_offset_start: float = 0,
               cut_offset_end: float = -1,
               # Not used for now - 8 bit signed value
               brstm_patch_value: int = 100
  ) -> None:
    self.infile = infile
    self.outfile = outfile
    
    self.speed_increase = speed_increase
    self.db_increase = db_increase
    self.cut_offset_start = cut_offset_start
    self.cut_offset_end = cut_offset_end
    self.brstm_patch_value = brstm_patch_value