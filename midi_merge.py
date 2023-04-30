import mido

# Set the MIDI file path
midi_file = "example.mid"

# Open the MIDI file and get all tracks
midi = mido.MidiFile(midi_file)
tracks = midi.tracks

# Create a new track to hold the merged messages
merged_track = mido.MidiTrack()

# Set the tick resolution of the merged track to match the input MIDI file
merged_track.ticks_per_beat = midi.ticks_per_beat

# Create a dictionary to hold the pending messages for each channel
pending_messages = {}

# Iterate through each track and add its messages to the merged track
for track in tracks:
    # Reset the time for this track to 0
    time = 0
    # Iterate through each message in the track
    for message in track:
        # Update the time of the message with the current track time
        message.time += time
        # Check if the message is a note on or off event
        if message.type in ["note_on", "note_off"]:
            # Get the channel of the message
            channel = message.channel
            # Check if there are any pending messages for this channel
            if channel in pending_messages:
                # Iterate through the pending messages and add their time to the current time
                for pending_message in pending_messages[channel]:
                    pending_message.time += time
                # Add the pending messages to the merged track
                merged_track.extend(pending_messages[channel])
                # Remove the pending messages for this channel
                del pending_messages[channel]
            # Add the message to the pending messages for this channel
            if channel not in pending_messages:
                pending_messages[channel] = []
            pending_messages[channel].append(message)
        # For all other message types, add the message directly to the merged track
        else:
            merged_track.append(message)
        # Update the time for this track with the time of the current message
        time = message.time

# Add any remaining pending messages to the merged track
for channel in pending_messages:
    for message in pending_messages[channel]:
        message.time += time
    merged_track.extend(pending_messages[channel])

# Save the merged track to a new MIDI file
midi_merged = mido.MidiFile()
midi_merged.tracks.append(merged_track)
midi_merged.save("merged.mid")
