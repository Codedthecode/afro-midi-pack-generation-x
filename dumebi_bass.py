#!/usr/bin/env python3
"""
Generate MIDI file for Dumebi by Rema - Bass Line
Key: F# minor
Tempo: 105 BPM

Usage:
    python dumebi_bass.py
"""

from mido import MidiFile, MidiTrack, Message
import os
from datetime import datetime

def generate_dumebi_bass(num_bars=8, output_name="dumebi_bass.mid"):
    """
    Generate a MIDI file with the Dumebi bass line.
    
    Args:
        num_bars (int): Number of bars to generate (default: 8)
        output_name (str): Output filename (default: dumebi_bass.mid)
    """
    
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

    # Bass pattern for Dumebi
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

    # Generate the specified number of bars
    velocity = 100  # Bass volume (0-127)

    for bar in range(num_bars):
        for note_name, duration in pattern:
            note_number = notes[note_name]
            
            # Note on
            track.append(Message('note_on', note=note_number, velocity=velocity, time=0))
            # Note off
            track.append(Message('note_off', note=note_number, velocity=velocity, time=duration))

    # Save the MIDI file
    midi.save(output_name)
    
    # Print success message
    print(f"\n✅ MIDI file created successfully!")
    print(f"📁 File: {output_name}")
    print(f"🎵 Song: Dumebi by Rema")
    print(f"🎹 Key: F# minor")
    print(f"⏱️  Tempo: 105 BPM")
    print(f"📊 Duration: {num_bars} bars")
    print(f"🔊 Instrument: Bass")
    print(f"⏰ Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\n💡 Next steps:")
    print(f"   1. Open your DAW (FL Studio, Ableton, Logic Pro, etc.)")
    print(f"   2. Import '{output_name}' into a track")
    print(f"   3. Assign a bass instrument")
    print(f"   4. Start producing! 🎧\n")


if __name__ == "__main__":
    # Generate default MIDI file (8 bars)
    generate_dumebi_bass()
    
    # Uncomment below to generate with custom settings:
    # generate_dumebi_bass(num_bars=16, output_name="dumebi_bass_extended.mid")
