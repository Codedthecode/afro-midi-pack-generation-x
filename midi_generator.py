#!/usr/bin/env python3
"""
Afro MIDI Generator - Direct Download from Copilot
Generate Dumebi bass lines and chord progressions instantly
"""

import struct
import io

class MIDIGenerator:
    def __init__(self, tempo=120):
        self.tempo = tempo
        self.ticks_per_beat = 480
        self.track_data = []
        
    def add_tempo(self):
        """Add tempo to MIDI"""
        microseconds = int(60_000_000 / self.tempo)
        self.track_data.extend([0x00, 0xFF, 0x51, 0x03])
        self.track_data.extend([
            (microseconds >> 16) & 0xFF,
            (microseconds >> 8) & 0xFF,
            microseconds & 0xFF
        ])
    
    def add_program_change(self, program=33):
        """Set instrument (33 = Bass)"""
        self.track_data.extend([0x00, 0xC0, program])
    
    def add_note_on(self, note, velocity=100):
        """Turn note on"""
        self.track_data.extend([0x00, 0x90, note, velocity])
    
    def add_note_off(self, note, duration=480):
        """Turn note off with duration"""
        # Convert duration to variable length quantity
        if duration < 128:
            self.track_data.extend([duration, 0x80, note, 0])
        else:
            self.track_data.extend([0x83, 0x60, 0x80, note, 0])
    
    def add_end_of_track(self):
        """Mark end of track"""
        self.track_data.extend([0x00, 0xFF, 0x2F, 0x00])
    
    def get_midi_bytes(self):
        """Generate complete MIDI file"""
        midi_data = bytearray()
        
        # Header
        midi_data.extend(b'MThd')
        midi_data.extend([0, 0, 0, 6])  # Header length
        midi_data.extend([0, 0])  # Format type 0
        midi_data.extend([0, 1])  # Number of tracks
        midi_data.extend([0x01, 0xE0])  # Ticks per beat (480)
        
        # Track
        midi_data.extend(b'MTrk')
        track_length = len(self.track_data)
        midi_data.extend([
            (track_length >> 24) & 0xFF,
            (track_length >> 16) & 0xFF,
            (track_length >> 8) & 0xFF,
            track_length & 0xFF
        ])
        midi_data.extend(self.track_data)
        
        return bytes(midi_data)


def generate_dumebi_bass(bars=8, velocity=100):
    """Generate Dumebi by Rema bass line"""
    gen = MIDIGenerator(tempo=105)
    gen.add_tempo()
    gen.add_program_change(program=33)  # Bass
    
    notes = {'F#': 54, 'A': 57, 'B': 59, 'C#': 61}
    pattern = ['F#', 'F#', 'A', 'B', 'F#', 'F#', 'C#', 'B']
    
    for _ in range(bars):
        for note_name in pattern:
            note = notes[note_name]
            gen.add_note_on(note, velocity)
            gen.add_note_off(note, duration=480)
    
    gen.add_end_of_track()
    return gen.get_midi_bytes()


def generate_chord_progression(key='C', progression='I-IV-V-I', bars=8, tempo=120, velocity=100):
    """Generate chord progression"""
    gen = MIDIGenerator(tempo=tempo)
    gen.add_tempo()
    gen.add_program_change(program=33)  # Piano/Bass
    
    # Note mapping
    note_map = {
        'C': 48, 'C#': 49, 'D': 50, 'D#': 51, 'E': 52, 'F': 53,
        'F#': 54, 'G': 55, 'G#': 56, 'A': 57, 'A#': 58, 'B': 59
    }
    
    # Chord definitions
    chord_intervals = {
        'C': [0, 4, 7], 'Cm': [0, 3, 7],
        'D': [2, 6, 9], 'Dm': [2, 5, 9],
        'E': [4, 8, 11], 'Em': [4, 7, 11],
        'F': [5, 9, 12], 'Fm': [5, 8, 12],
        'G': [7, 11, 14], 'Gm': [7, 10, 14],
        'A': [9, 1, 5], 'Am': [9, 0, 4],
        'B': [11, 3, 7], 'Bm': [11, 2, 6]
    }
    
    # Progression patterns
    progressions = {
        'I-IV-V-I': [0, 5, 7, 0],
        'I-V-vi-IV': [0, 7, 9, 5],
        'vi-IV-I-V': [9, 5, 0, 7],
        'I-IV-I-V': [0, 5, 0, 7],
        'ii-V-I': [2, 7, 0],
        'I-vi-IV-V': [0, 9, 5, 7],
    }
    
    base_note = note_map[key[0]]
    prog_offsets = progressions.get(progression, [0, 5, 7, 0])
    intervals = chord_intervals.get(key, [0, 4, 7])
    
    for _ in range(bars):
        for offset in prog_offsets:
            # Play chord
            for interval in intervals:
                note = base_note + offset + interval
                gen.add_note_on(note, velocity)
            
            # Duration
            gen.track_data.extend([0x83, 0x60])  # Quarter note (480 ticks)
            
            # Release chord
            for interval in intervals:
                note = base_note + offset + interval
                gen.track_data.extend([0x80, note, 0])
    
    gen.add_end_of_track()
    return gen.get_midi_bytes()


# Example usage
if __name__ == "__main__":
    print("🎵 Afro MIDI Generator")
    print("=" * 40)
    
    # Generate Dumebi
    dumebi_midi = generate_dumebi_bass(bars=8)
    print(f"✅ Dumebi Bass: {len(dumebi_midi)} bytes")
    
    # Generate Chord Progression
    chord_midi = generate_chord_progression(key='C', progression='I-IV-V-I', tempo=120)
    print(f"✅ C Major Chords: {len(chord_midi)} bytes")
    
    print("\nUse the functions in Copilot to generate and download MIDI files!")
