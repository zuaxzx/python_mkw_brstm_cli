import subprocess
import pytube
import pathlib

def convert_mp4_to_wav(infile: str, outfile: str):
  infile = pathlib.Path(infile).absolute()
  outfile = pathlib.Path(outfile).absolute()
  
  if outfile.exists():
    outfile.unlink()
    
  cmd = ["ffmpeg", "-i", infile, "-ab", "160k", "-ac", "2", "-ar", "48000", "-vn", outfile]
  subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def dl_mp4_from_yt(url: str, outfile: str):
  outfile = pathlib.Path(outfile).absolute()
  
  if outfile.exists():
    outfile.unlink()
  
  # Try to download video
  try:
    youtube = pytube.YouTube(url)
    audio = youtube.streams.filter(only_audio=True).first()
    
    print("Downloading:", url)
    audio.download(output_path=outfile.parent, filename=outfile.name)

    print("Downloaded:", outfile)
  
  # Exception while downloading
  except pytube.exceptions.PytubeError as e:
    print(f"Error while trying to download {url}:", e)