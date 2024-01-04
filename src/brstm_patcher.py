def patch_brstm(file: str, patch_value: int) -> None:
  """Patch the brstm volume value in the brstm

  Args:
      file (str): BRSTM file to parse
      patch_value (int): Integer representation of 8 bit value in brstm (0 - 127)

  Raises:
      ValueError: Patch value is not in range
  """
  # Always at this offset
  offset = 0x3F
  
  # Range check
  if patch_value > 127 or patch_value < 0:
    raise ValueError(f"Given patch value is invalid {patch_value}. Valid: 0 - 127")
  
  # Convert patch value to bytes
  value = bytes([patch_value])
  
  # Open the brstm
  with open(file, "r+b") as f:
    # Go to offset position
    f.seek(offset)
    # (Over)Write patch value
    f.write(value)