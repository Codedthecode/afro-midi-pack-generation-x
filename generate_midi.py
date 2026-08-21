#!/usr/bin/env python3
"""
Quick MIDI Generator for Dumebi by Rema
Run this script to generate dumebi_bass.mid instantly
"""

from mido import MidiFile, MidiTrack, Message

def generate_dumebi_midi(bars=8, filename="dumebi_bass.mid"):
    """Generate Dumebi bass MIDI file"""
    
    midi = MidiFile()
    midi.ticks_per_beat = 480
    track = MidiTrack()
    midi.tracks.append(track)

    # Set tempo (105 BPM)
    tempo = int(60_000_000 / 105)
    track.append(Message('set_tempo', tempo=tempo))
    track.append(Message('program_change', program=33, time=0))

    # Bass notes: F#=54, A=57, B=59, C#=61
    notes = {'F#': 54, 'A': 57, 'B': 59, 'C#': 61}
    pattern = ['F#', 'F#', 'A', 'B', 'F#', 'F#', 'C#', 'B']

    for bar in range(bars):
        for note in pattern:
            track.append(Message('note_on', note=notes[note], velocity=100, time=0))
            track.append(Message('note_off', note=notes[note], velocity=100, time=480))

    midi.save(filename)
    return filename

if __name__ == "__main__":
    file = generate_dumebi_midi(bars=8)
    print(f"✅ Generated: {file}")
    print("Ready to drag into FL Studio!")
