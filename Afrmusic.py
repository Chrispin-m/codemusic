import numpy as np
from pydub import AudioSegment
from pydub.playback import play


sample_rate = 44100  # Samples per second
tempo = 120  # Beats per minute
beat_duration = 60.0 / tempo  # Duration of a beat in seconds
num_bars = 8  

#create a sine wave
def generate_sine_wave(frequency, duration, sample_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    sine_wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    return np.int16(sine_wave * 32767)  # Convert to 16-bit PCM


def create_drum_beat():
    kick = generate_sine_wave(100, beat_duration, sample_rate)  # Kick drum
    snare = generate_sine_wave(200, beat_duration, sample_rate)  # Snare drum
    hi_hat = generate_sine_wave(10, beat_duration / 2, sample_rate)  # Hi-hat

    pattern = np.concatenate((
        kick, hi_hat, snare, hi_hat, kick, hi_hat, snare, hi_hat,
        snare, hi_hat, kick, hi_hat, snare, hi_hat, kick, hi_hat
    ))
    
    return np.tile(pattern, num_bars)

# percussion layer
def create_additional_percussion():
    mid_tom = generate_sine_wave(150, beat_duration, sample_rate)
    low_tom = generate_sine_wave(120, beat_duration, sample_rate)
    
    pattern = np.concatenate((
        mid_tom, np.zeros(len(mid_tom)), low_tom, np.zeros(len(low_tom)),
        low_tom, mid_tom, low_tom, np.zeros(len(mid_tom))
    ))
    
    return np.tile(pattern, num_bars)

def create_melody():
    scale = [220.0, 246.94, 261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25, 587.33, 659.25]
    melody = []
    
    
    for _ in range(num_bars):
        
        for note_index, duration_factor in zip(
            [0, 2, 4, 5, 7, 9, 7, 5, 4, 2, 0, 9, 7, 5, 4, 2, 0],
            [1, 0.5, 1, 1.5, 1, 0.75, 1, 1, 1, 1.25, 1, 0.5, 1, 1.25, 1, 0.75, 1]
        ):
            # Main note
            main_note = generate_sine_wave(scale[note_index], beat_duration * duration_factor, sample_rate)
            melody.append(main_note)
            
            if np.random.random() > 0.5:
                harmonic_note = generate_sine_wave(scale[(note_index + 4) % len(scale)], beat_duration * duration_factor, sample_rate)
                melody[-1] = melody[-1] + harmonic_note
    
    return np.concatenate(melody)

def create_music():
    rhythm = create_drum_beat()
    percussion = create_additional_percussion()
    melody = create_melody()
    
    
    max_length = max(len(rhythm), len(percussion), len(melody))
    rhythm = np.pad(rhythm, (0, max_length - len(rhythm)), 'constant')
    percussion = np.pad(percussion, (0, max_length - len(percussion)), 'constant')
    melody = np.pad(melody, (0, max_length - len(melody)), 'constant')
    
    
    music = rhythm + percussion + melody
    
    
    music = np.int16(music * (32767 / np.max(np.abs(music))))   
    audio_segment = AudioSegment(
        music.tobytes(),
        frame_rate=sample_rate,
        sample_width=music.dtype.itemsize,
        channels=1
    )
    audio_segment.export("iChrispin_music.wav", format="wav")
    return audio_segment

# Generate and play part
african_music = create_music()
play(african_music)
