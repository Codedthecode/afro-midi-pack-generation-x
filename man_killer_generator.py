#!/usr/bin/env python3
"""
MAN KILLER - Chord Progression Generator
Professional Afrobeats Track
Key: A Minor | BPM: 113 | Emotion: All (Heartbreak + Passion + Strength + Longing + Anger)
Progression: Am-F-C-G-Am-E-F-G (Professional 8-bar loop)
"""

class MIDIGenerator:
    def __init__(self, tempo=113, ticks_per_beat=480):
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
    
    def add_program_change(self, program=0):
        """Set instrument"""
        self.track_data.extend([0x00, 0xC0, program])
    
    def add_note(self, note, velocity=100, duration=480, delta_time=0):
        """Add a note with proper timing"""
        self.track_data.extend(self._variable_length_encode(delta_time))
        self.track_data.extend([0x90, note, velocity])
        self.track_data.extend(self._variable_length_encode(duration))
        self.track_data.extend([0x80, note, 0])
    
    def add_chord(self, notes, velocity=85, duration=960):
        """Add a chord (multiple notes at once)"""
        for i, note in enumerate(notes):
            self.track_data.extend(self._variable_length_encode(0))
            self.track_data.extend([0x90, note, velocity])
        
        self.track_data.extend(self._variable_length_encode(duration))
        for note in notes:
            self.track_data.extend([0x80, note, 0])
    
    def add_end_of_track(self):
        """End of track meta event"""
        self.track_data.extend([0x00, 0xFF, 0x2F, 0x00])
    
    def get_midi_bytes(self):
        """Generate complete MIDI file"""
        midi_data = bytearray()
        
        # Header chunk
        midi_data.extend(b'MThd')
        midi_data.extend([0x00, 0x00, 0x00, 0x06])
        midi_data.extend([0x00, 0x00])
        midi_data.extend([0x00, 0x01])
        midi_data.extend([
            (self.ticks_per_beat >> 8) & 0xFF,
            self.ticks_per_beat & 0xFF
        ])
        
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


def generate_man_killer_chords(bars=16, velocity=85):
    """
    Generate MAN KILLER chord progression
    
    Professional 8-bar loop: Am-F-C-G-Am-E-F-G
    Repeated for emotional journey
    
    Args:
        bars: Number of bars (default 16 = 2 full loops)
        velocity: MIDI velocity (volume) 0-127
    
    Returns:
        MIDI file bytes ready to download
    """
    gen = MIDIGenerator(tempo=113, ticks_per_beat=480)
    gen.add_tempo()
    gen.add_program_change(program=0)  # Acoustic Piano
    
    # Note mapping (A2 octave for deep, emotional feel)
    note_map = {
        'A': 45,   # A2 (root)
        'C': 48,   # C3
        'E': 52,   # E3
        'F': 53,   # F3
        'G': 55    # G3
    }
    
    # Chord definitions (triads: root, third, fifth)
    chords = {
        'Am': [45, 48, 52],      # A-C-E (A minor)
        'F': [53, 57, 60],       # F-A-C (F major)
        'C': [48, 52, 55],       # C-E-G (C major)
        'G': [55, 59, 62],       # G-B-D (G major)
        'E': [52, 56, 59],       # E-G#-B (E major)
    }
    
    # Professional 8-bar progression
    progression = ['Am', 'F', 'C', 'G', 'Am', 'E', 'F', 'G']
    
    # Half note duration (2 beats at 113 BPM = 960 ticks)
    half_note = 960
    
    # Generate progression for specified number of bars
    for bar in range(bars):
        chord_name = progression[bar % 8]
        chord_notes = chords[chord_name]
        
        # Play chord for half note (2 beats)
        gen.add_chord(chord_notes, velocity=velocity, duration=half_note)
    
    gen.add_end_of_track()
    return gen.get_midi_bytes()


def generate_man_killer_bass(bars=16, velocity=90):
    """
    Generate MAN KILLER bass line
    Deep A minor synth bass following chord progression
    """
    gen = MIDIGenerator(tempo=113, ticks_per_beat=480)
    gen.add_tempo()
    gen.add_program_change(program=33)  # Electric Bass
    
    # Bass notes (root of each chord in low octave)
    bass_notes = {
        'Am': 33,  # A1
        'F': 41,   # F1
        'C': 36,   # C1
        'G': 43,   # G1
        'E': 40,   # E1
    }
    
    progression = ['Am', 'F', 'C', 'G', 'Am', 'E', 'F', 'G']
    quarter_note = 480
    
    # Pattern: root note plays 4 times per bar (4 quarter notes)
    for bar in range(bars):
        chord_name = progression[bar % 8]
        bass_note = bass_notes[chord_name]
        
        for _ in range(4):
            gen.add_note(bass_note, velocity=velocity, duration=quarter_note, delta_time=0)
    
    gen.add_end_of_track()
    return gen.get_midi_bytes()


def generate_man_killer_melody(bars=16, velocity=95):
    """
    Generate MAN KILLER emotional melody
    Catchy hook that follows the emotional journey
    """
    gen = MIDIGenerator(tempo=113, ticks_per_beat=480)
    gen.add_tempo()
    gen.add_program_change(program=48)  # String ensemble (emotional)
    
    # Melody notes (A minor pentatonic scale for emotional feel)
    # Pattern changes based on chord progression for emotional journey
    
    # Heartbreak section (Am-F-C-G): Lower, sad melody
    heartbreak = [69, 71, 72, 71, 69, 67, 65, 67]  # A4-B4-C5-B4-A4-G4-F#4-G4
    
    # Strength section (Am-E-F-G): Higher, powerful melody
    strength = [76, 77, 76, 74, 76, 77, 79, 81]  # E5-F5-E5-D5-E5-F5-G5-A5
    
    quarter_note = 480
    progression = ['Am', 'F', 'C', 'G', 'Am', 'E', 'F', 'G']
    
    for bar in range(bars):
        if bar % 8 < 4:  # First 4 bars (heartbreak)
            melody_notes = heartbreak
        else:  # Second 4 bars (strength)
            melody_notes = strength
        
        for note in melody_notes:
            gen.add_note(note, velocity=velocity, duration=quarter_note // 2, delta_time=0)
    
    gen.add_end_of_track()
    return gen.get_midi_bytes()


# Generate all components
if __name__ == "__main__":
    print("🎵 MAN KILLER - Professional Afrobeats Track")
    print("=" * 60)
    print("\n📊 Track Specifications:")
    print("  Key: A Minor")
    print("  BPM: 113")
    print("  Progression: Am-F-C-G-Am-E-F-G (8-bar professional loop)")
    print("  Emotions: Heartbreak + Passion + Strength + Longing + Anger")
    print("  Reference: Dog Eat Dog by Odumodú Black")
    print("\n✅ Generating MIDI files...")
    
    # Generate components
    chords_midi = generate_man_killer_chords(bars=16)
    bass_midi = generate_man_killer_bass(bars=16)
    melody_midi = generate_man_killer_melody(bars=16)
    
    print(f"\n✅ Chord Progression: {len(chords_midi)} bytes")
    print(f"✅ Bass Line: {len(bass_midi)} bytes")
    print(f"✅ Melody: {len(melody_midi)} bytes")
    print("\n🎵 Ready to download from Copilot!")
