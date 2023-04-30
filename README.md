# midi2fmf
MIDI to FMF file converter in Python
This allows you to convert MIDI (.mid) sheet music files into Flipper Music Files (.fmf)

This is based on a script by Sharkmare. [Repo](https://github.com/Sharkmare/Midi-to-fmf/)

# Usage
You can call this script through CLI:
```console
python midi2fmf.py Futurama_Theme
```
Futurama_Theme.mid -> Futurama_Theme.fmf

If you already have a .fmf with the same name, it is overwritten. This way, if you want to adjust downpitch, it's easier.
# Known issues
Sometimes the .fmf file will come out without notes or few notes, in which case you need to change the track number. This is because .midi files have multiple tracks and you might be on a track which does not have notes.
> There is a midi_merge.py file which will merge the tracks into a single track, but it is finnicky
## Dependencies
mido
