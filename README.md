# midi2fmf
MIDI to FMF file converter in Python.
This allows you to convert MIDI (.mid) sheet music files into Flipper Music Files (.fmf)

# Usage
You can call this script through CLI (P.S. you can add or omit the .mid):
```console
python midi2fmf.py Futurama_Theme
```
You can also pass params through:
```console
python midi2fmf.py Futurama_Theme -o 3 -d 16
```
### Params
| Syntax      | Description                                                     |Default      |
| --- | --- | --- |
| Octave      | Interval between pitches 1-16                                   |4            |
| Duration    | Note duration 1-128                                             |8            |
| Track       | Track number. You only need to change if on a multi track midi  |0            |

Futurama_Theme.mid -> Futurama_Theme.fmf
If you already have a .fmf with the same name, it is overwritten. This way, if you want to adjust downpitch, it's easier.
# Known issues
Sometimes the .fmf file will come out without notes or few notes, in which case you need to change the track number. This is because .midi files have multiple tracks and you might be on a track which does not have notes.
> There is a midi_merge.py file which will merge the tracks into a single track, but it is finnicky

## FMF format breakdown [Credit](https://github.com/Tonsil/flipper-music-files)

.fmf files should have the following format:

```
Filetype: Flipper Music Format
Version: 0
BPM: <integer beats per minute>
Duration: <default note duration>
Octave: <default octave>
Notes: <comma-delimited list of notes>
```

### Note Format

`<duration><note|rest><sharp><octave><dots>`

- **duration**: Number between 1 & 128, defaults to project duration. 1 is a full note, 2 is a half note, 4 is quarter note, etc. (i.e. 1/d)
- **note**: A through G or P for pause (rest)
- **sharp**: # or omitted
- **octave**: Between 1 & 16, defaults to project octave
- **dots**: Between 1 & 16 '.' characters. Each dot makes the note 150% of its length. (1.5^n)

#### Examples:

- `8C4` - Eight note pitch of C, fourth octave
- `4A#5.` - Dotted quarter note pitch of A sharp, fifth octave
- `2P` - Half note rest

This repository is based on a script by Sharkmare. [Repo](https://github.com/Sharkmare/Midi-to-fmf/)

## Dependencies
mido
