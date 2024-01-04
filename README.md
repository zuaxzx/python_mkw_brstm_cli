
# Python MKW brstm cli

Small command line interface to convert wav file to brstm.
Conversion to brstm is currently done by VGAudioCli.

Will also add effects to the wav using pydub including:

- Multi channels
- Speed change
- Audio cut

## Usage

```shell
python main.py <track> <url/wav> <--options>
```
Note: For track see ``config.yml``

## Dependencies

- Python requirements.txt
- ffmpeg (Dependency of pydub) in PATH
- VGAudioCli (Conversion to brstm) in PATH
