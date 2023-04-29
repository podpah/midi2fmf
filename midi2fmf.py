import mido
import sys # So you can call from CLI instead of changing script every time
import os # This is to delete the .fmf file before generation, so you don't need to keep deleting manually

# Set the parameters for the Flipper Music Format output
filetype = "Flipper Music Format"
version = 0
duration = 8
octave = 4

# Set the MIDI file path and track number to be converted
midi_file = sys.argv[1] + ".mid"
track_number = 1

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

# Ask the user if they want to downpitch the song
downpitch = input("Do you want to downpitch the song? (y/n) ")
if downpitch.lower() == "y":
    semitones = int(input("By how many semitones? "))

    # Adjust the octave based on the downpitch
    octave -= semitones // 12
elif downpitch.lower() == "n":
	pass
else: # In case you skip Y/N and just put the semitone amount
	print("Invalid response y/n")
	sys.exit()
	
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
output = sys.argv[1] + ".fmf"
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
