import mido
import os # This is to delete the .fmf file before generation, so you don't need to keep deleting manually
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("filename", help="the name of the MIDI file to convert to FMF format")

# Optionals
parser.add_argument("-t", "--track", type=int, help="track number if multitrack midi (default: 0)")
parser.add_argument("-d", "--duration", type=int, help="sets the default note duration (default: 8)")
parser.add_argument("-o", "--octave", type=int, help="sets the octave (default: 4)")

args = parser.parse_args()

# Set the parameters for the Flipper Music Format output
filetype = "Flipper Music Format"
version = 0
duration = args.duration if args.duration else 8
octave = args.octave if args.octave else 4

# Set the MIDI file path and track number to be converted
midi_file = args.filename if args.filename[-4:] == ".mid" else args.filename + ".mid"
track_number = args.track if args.track else 0

# Open the MIDI file and get the specified track
midi = mido.MidiFile(midi_file)
track = midi.tracks[track_number]

# Get the tempo from the MIDI file
microseconds_per_quarter_note = 0
for message in track:
    if message.type == "set_tempo":
        microseconds_per_quarter_note = message.tempo
        break

# Calculate the BPM based on the tempo in the MIDI file
if microseconds_per_quarter_note > 0:
    ticks_per_beat = midi.ticks_per_beat
    microseconds_per_minute = 60_000_000
    bpm = round(microseconds_per_minute / (microseconds_per_quarter_note * ticks_per_beat))
else:
    # If no tempo event is found, prompt the user for the BPM
    bpm = int(input("No tempo event found. Please enter the BPM: "))
	
# Create a list to store the notes in Flipper Music Format
notes = []

# Iterate through each message in the MIDI track
for message in track:
    # Check if the message is a note on event
    if message.type == "note_on" and message.velocity != 0:
        # Get the pitch of the note
        pitch = message.note
        # Downpitch the pitch if requested by the user
        if downpitch.lower() == "y":
            pitch -= semitones
        # Convert the pitch to a note string in Flipper Music Format
        note_str = ""
        if pitch % 12 == 0:
            note_str = "C"
        elif pitch % 12 == 1:
            note_str = "C#"
        elif pitch % 12 == 2:
            note_str = "D"
        elif pitch % 12 == 3:
            note_str = "D#"
        elif pitch % 12 == 4:
            note_str = "E"
        elif pitch % 12 == 5:
            note_str = "F"
        elif pitch % 12 == 6:
            note_str = "F#"
        elif pitch % 12 == 7:
            note_str = "G"
        elif pitch % 12 == 8:
            note_str = "G#"
        elif pitch % 12 == 9:
            note_str = "A"
        elif pitch % 12 == 10:
            note_str = "A#"
        elif pitch % 12 == 11:
            note_str = "B"
        # Add the note to the list of notes
        notes.append(note_str + str(pitch // 12 + octave))

# Create the output file and write the Flipper Music Format data
output = midi_file[:-4] + ".fmf"
try:
	os.remove(output)
except:
	pass # File doesn't exist
with open(output, "w") as f:
    f.write(f"Filetype: {filetype}\n")
    f.write(f"Version: {version}\n")
    f.write(f"BPM: {bpm}\n")
    f.write(f"Duration: {duration}\n")
    f.write(f"Octave: {octave}\n")
    f.write("Notes: " + ", ".join(notes) + "\n")
