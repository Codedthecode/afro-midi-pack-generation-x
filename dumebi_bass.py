#!/usr/bin/env python3
"""
Generate MIDI file for Dumebi by Rema - Bass Line
Key: F# minor
Tempo: 105 BPM
"""

from mido import MidiFile, MidiTrack, Message
import os

# Create a new MIDI file
midi = MidiFile()
midi.ticks_per_beat = 480

# Add a track
track = MidiTrack()
midi.tracks.append(track)

# Set tempo (105 BPM)
tempo_in_microseconds = int(60_000_000 / 105)
track.append(Message('program_change', program=33, time=0))  # Bass program
track.append(Message('control_change', control=121, value=0, time=0))  # Reset all controllers
track.append(Message('set_tempo', tempo=tempo_in_microseconds, time=0))

# Define the bass notes (in MIDI note numbers)
# F# = 54 (octave 3)
# A = 57
# B = 59
# C# = 61

notes = {
    'F#': 54,
    'A': 57,
    'B': 59,
    'C#': 61,
}

# Bass pattern for Dumebi (simplified)
# Pattern: F# - F# - A - B | F# - F# - C# - B
# Using quarter notes (480 ticks = quarter note at 480 ticks_per_beat)

pattern = [
    ('F#', 480),   # Quarter note
    ('F#', 480),   # Quarter note
    ('A', 480),    # Quarter note
    ('B', 480),    # Quarter note
    ('F#', 480),   # Quarter note
    ('F#', 480),   # Quarter note
    ('C#', 480),   # Quarter note
    ('B', 480),    # Quarter note
]

# Generate 8 bars (8 repetitions of the 8-note pattern)
velocity = 100  # Bass volume
num_bars = 8

for bar in range(num_bars):
    for note_name, duration in pattern:
        note_number = notes[note_name]
        
        # Note on
        track.append(Message('note_on', note=note_number, velocity=velocity, time=0))
        # Note off
        track.append(Message('note_off', note=note_number, velocity=velocity, time=duration))

# Save the MIDI file
output_path = 'dumebi_bass.mid'
midi.save(output_path)
print(f"✓ MIDI file created successfully: {output_path}")
print(f"  Key: F# minor")
print(f"  Tempo: 105 BPM")
print(f"  Duration: 8 bars")
print(f"  Instrument: Bass")
