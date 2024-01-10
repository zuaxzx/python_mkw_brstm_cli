
# Python MKW brstm cli

Small command line interface to convert wav file to brstm.
Conversion to brstm is currently done by VGAudioCli.

Following functionality is currently available:
- Convert youtube-url to brstm
- Convert wav file to brstm
- Adjust db gain
- Patch brstm
- Change speed for normal and fast lap each
- Cut audio for normal and fast lap each

## Installation

Add VGAudioCli and ffmpeg to your system PATH **or** define the _directory_ paths of the executable to the tools section of the yaml config in `config/config.yml`:

```yaml
tools:
  audiovg: C:/some/path/audiovg
  ffmpeg: C:/some/path/ffmpeg
```


## Usage

```shell
# Convert wav to brstm
./brstm_maker convert wav <file> ...

# Convert wav to brstm
./brstm_maker convert url <youtube-url> ...

# Patch brstm
./brstm_maker patch <brstm_file> <value>
```

Note: For tracks see ``config.yml``

## Dependencies

- ffmpeg (Dependency of pydub) in PATH
- VGAudioCli (Conversion to brstm) in PATH

### Further build dependencies

- Python requirements.txt