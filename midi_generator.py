#!/usr/bin/env python3
"""
Afro MIDI Generator - Accurate Music Recreation
Generates MIDI files that match actual song patterns and timings
"""

import struct

class MIDIGenerator:
    def __init__(self, tempo=120, ticks_per_beat=480):
        self.tempo = tempo
        self.ticks_per_beat = ticks_per_beat
        self.track_data = bytearray()
        
    def _variable_length_encode(self, value):
        """Encode value as MIDI variable length quantity"""
        result = []
        result.append(value & 0x7F)
        value >>= 7
        while value:
            result.append((value & 0x7F) | 0x80)
            value >>= 7
        return bytes(reversed(result))
    
    def add_tempo(self):
        """Add tempo meta event"""
        microseconds = int(60_000_000 / self.tempo)
        self.track_data.extend([0x00, 0xFF, 0x51, 0x03])
        self.track_data.extend([
            (microseconds >> 16) & 0xFF,
            (microseconds >> 8) & 0xFF,
            microseconds & 0xFF
        ])
    
    def add_program_change(self, program=33):
        """Set instrument"""
        self.track_data.extend([0x00, 0xC0, program])
    
    def add_note(self, note, velocity=100, duration=480, delta_time=0):
        """Add a note with proper timing"""
        # Delta time for note on
        self.track_data.extend(self._variable_length_encode(delta_time))
        self.track_data.extend([0x90, note, velocity])
        
        # Delta time for note off
        self.track_data.extend(self._variable_length_encode(duration))
        self.track_data.extend([0x80, note, 0])
    
    def add_end_of_track(self):
        """End of track meta event"""
        self.track_data.extend([0x00, 0xFF, 0x2F, 0x00])
    
    def get_midi_bytes(self):
        """Generate complete MIDI file"""
        midi_data = bytearray()
        
        # Header chunk
        midi_data.extend(b'MThd')
        midi_data.extend([0x00, 0x00, 0x00, 0x06])  # Header length
        midi_data.extend([0x00, 0x00])  # Format type 0
        midi_data.extend([0x00, 0x01])  # Number of tracks
        midi_data.extend([
            (self.ticks_per_beat >> 8) & 0xFF,
            self.ticks_per_beat & 0xFF
        ])  # Ticks per beat
        
        # Track chunk
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


def generate_dumebi_bass_accurate(bars=8, velocity=90):
    """
    Generate accurate Dumebi by Rema bass line
    
    Song Details:
    - Key: F# minor (54 = F#3)
    - Tempo: 105 BPM
    - Time Signature: 4/4
    - Pattern: F# F# A B | F# F# C# B (repeating)
    - Duration: Quarter notes (480 ticks each)
    """
    gen = MIDIGenerator(tempo=105, ticks_per_beat=480)
    gen.add_tempo()
    gen.add_program_change(program=33)  # Electric Bass
    
    # MIDI note numbers for Dumebi
    notes = {
        'F#': 54,  # F#3 (lower bass register)
        'A': 57,   # A3
        'B': 59,   # B3
        'C#': 61   # C#4
    }
    
    # Exact pattern from Dumebi - one bar = 4 quarter notes
    pattern = ['F#', 'F#', 'A', 'B', 'F#', 'F#', 'C#', 'B']
    quarter_note = 480  # Standard quarter note duration
    
    for bar in range(bars):
        for i, note_name in enumerate(pattern):
            note = notes[note_name]
            # Each quarter note plays for exactly 480 ticks
            gen.add_note(note, velocity=velocity, duration=quarter_note, delta_time=0)
    
    gen.add_end_of_track()
    return gen.get_midi_bytes()


def generate_chord_progression_accurate(key='C', progression_type='I-IV-V-I', bars=8, tempo=120, velocity=85):
    """
    Generate accurate chord progressions based on music theory
    
    Supported progressions:
    - I-IV-V-I: Classic/Traditional
    - I-V-vi-IV: Pop (Axis Theory)
    - vi-IV-I-V: Sad/Minor feel
    - I-IV-I-V: Afrobeats style
    - ii-V-I: Jazz standard
    - I-vi-IV-V: Doo-wop
    """
    gen = MIDIGenerator(tempo=tempo, ticks_per_beat=480)
    gen.add_tempo()
    gen.add_program_change(program=0)  # Acoustic Piano
    
    # Note mapping (C3 to B3 octave)
    note_map = {
        'C': 48, 'C#': 49, 'D': 50, 'D#': 51, 'E': 52, 'F': 53,
        'F#': 54, 'G': 55, 'G#': 56, 'A': 57, 'A#': 58, 'B': 59
    }
    
    # Chord triads (root, third, fifth intervals)
    chords = {
        'C': [0, 4, 7],     # C-E-G (Major)
        'Cm': [0, 3, 7],    # C-Eb-G (Minor)
        'D': [2, 6, 9],     # D-F#-A
        'Dm': [2, 5, 9],    # D-F-A
        'E': [4, 8, 11],    # E-G#-B
        'Em': [4, 7, 11],   # E-G-B
        'F': [5, 9, 12],    # F-A-C
        'Fm': [5, 8, 12],   # F-Ab-C
        'G': [7, 11, 14],   # G-B-D
        'Gm': [7, 10, 14],  # G-Bb-D
        'A': [9, 1, 5],     # A-C#-E
        'Am': [9, 0, 4],    # A-C-E
        'B': [11, 3, 7],    # B-D#-F#
        'Bm': [11, 2, 6]    # B-D-F#
    }
    
    # Roman numeral to scale degree mapping
    progressions = {
        'I-IV-V-I': [0, 5, 7, 0],          # 1-4-5-1
        'I-V-vi-IV': [0, 7, 9, 5],         # 1-5-6-4
        'vi-IV-I-V': [9, 5, 0, 7],         # 6-4-1-5
        'I-IV-I-V': [0, 5, 0, 7],          # 1-4-1-5
        'ii-V-I': [2, 7, 0],               # 2-5-1
        'I-vi-IV-V': [0, 9, 5, 7],         # 1-6-4-5
    }
    
    base_note = note_map.get(key[0], 48)
    is_minor = key.endswith('m')
    
    # Get progression offsets
    prog_offsets = progressions.get(progression_type, [0, 5, 7, 0])
    
    # Get chord intervals
    chord_key = key if is_minor else key
    chord_intervals = chords.get(chord_key, [0, 4, 7])
    
    half_note = 960  # Two quarter notes
    
    for bar in range(bars):
        for offset in prog_offsets:
            # Play all three notes of chord simultaneously
            for i, interval in enumerate(chord_intervals):
                note = base_note + offset + interval
                if i == 0:
                    # First note has delta time
                    gen.add_note(note, velocity=velocity, duration=half_note, delta_time=0)
                else:
                    # Other notes start at same time (delta_time=0)
                    gen.track_data.extend([0x00, 0x90, note, velocity])
            
            # Release all chord notes at once
            gen.track_data.extend([self._encode_delta(half_note)])
            for interval in chord_intervals:
                note = base_note + offset + interval
                gen.track_data.extend([0x80, note, 0])
    
    gen.add_end_of_track()
    return gen.get_midi_bytes()


def _encode_delta(value):
    """Helper to encode delta time"""
    result = []
    result.append(value & 0x7F)
    value >>= 7
    while value:
        result.append((value & 0x7F) | 0x80)
        value >>= 7
    return bytes(reversed(result))


# Quick access functions
def dumebi_bass(bars=8):
    """Generate Dumebi bass - just call with bars count"""
    return generate_dumebi_bass_accurate(bars=bars)


def chord_progression(key='C', progression='I-IV-V-I', bars=8, tempo=120):
    """Generate chord progression - specify key, progression, bars, tempo"""
    return generate_chord_progression_accurate(
        key=key,
        progression_type=progression,
        bars=bars,
        tempo=tempo
    )


if __name__ == "__main__":
    print("✅ Afro MIDI Generator - Accurate Edition")
    print("=" * 50)
    print("\n📊 Available Progressions:")
    print("  - I-IV-V-I (Classic)")
    print("  - I-V-vi-IV (Pop)")
    print("  - vi-IV-I-V (Sad)")
    print("  - I-IV-I-V (Afrobeats)")
    print("  - ii-V-I (Jazz)")
    print("  - I-vi-IV-V (Doo-wop)")
    print("\n🎵 Use functions: dumebi_bass() or chord_progression()")
