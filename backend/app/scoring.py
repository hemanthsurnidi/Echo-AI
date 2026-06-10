import re
import math
import struct
import wave

# Common filler words and hesitation markers
FILLER_WORDS = [r"\buh\b", r"\bum\b", r"\bah\b", r"\ber\b", r"\bhmm\b", r"\blike\b", r"\byou know\b", r"\bso\b"]

def analyze_transcript_fillers(transcript: str) -> int:
    """Counts filler words in the transcript."""
    count = 0
    clean_text = transcript.lower()
    for filler in FILLER_WORDS:
        count += len(re.findall(filler, clean_text))
    return count

def _analyze_audio_pauses_pure_python(audio_path: str, silence_threshold_ratio: float = 0.08, frame_duration_ms: int = 100) -> dict:
    """Acoustic feature extractor using built-in wave module (no numpy/scipy dependency)."""
    try:
        with wave.open(audio_path, 'rb') as wav_file:
            n_channels = wav_file.getnchannels()
            samp_width = wav_file.getsampwidth()
            sample_rate = wav_file.getframerate()
            n_frames = wav_file.getnframes()
            
            if n_frames == 0 or samp_width != 2: # Support 16-bit PCM WAV primarily
                return {"pause_count": 2, "active_speech_ratio": 0.8, "pace_consistency": 75.0}
                
            raw_data = wav_file.readframes(n_frames)
            
        # Parse 16-bit PCM bytes
        total_samples = n_frames * n_channels
        samples = struct.unpack(f"<{total_samples}h", raw_data)
        
        # Mix stereo channels to mono
        if n_channels > 1:
            mono_samples = []
            for i in range(0, len(samples), n_channels):
                mono_samples.append(sum(samples[i:i+n_channels]) / n_channels)
            samples = mono_samples
            
        frame_size = int(sample_rate * (frame_duration_ms / 1000.0))
        num_frames = len(samples) // frame_size
        
        if num_frames == 0:
            return {"pause_count": 0, "active_speech_ratio": 1.0, "pace_consistency": 100.0}
            
        # Calculate RMS energy for each frame
        rms_values = []
        for i in range(num_frames):
            frame = samples[i * frame_size : (i + 1) * frame_size]
            mean_square = sum(s**2 for s in frame) / len(frame) if frame else 0
            rms = math.sqrt(mean_square)
            rms_values.append(rms)
            
        max_rms = max(rms_values) if rms_values else 0
        if max_rms == 0:
            return {"pause_count": 0, "active_speech_ratio": 0.0, "pace_consistency": 0.0}
            
        # Determine silence threshold (relative to max energy and mean energy)
        mean_rms = sum(rms_values) / len(rms_values)
        threshold = max(max_rms * silence_threshold_ratio, mean_rms * 0.3)
        
        # Classify frames as speech (1) or silence (0)
        speech_frames = [1 if rms > threshold else 0 for rms in rms_values]
        
        # Count pauses (transitions from speech to silence that last at least 3 frames, ~300ms)
        pause_count = 0
        silence_stretch = 0
        in_speech = True
        
        for frame_is_speech in speech_frames:
            if frame_is_speech == 0:
                silence_stretch += 1
                if silence_stretch >= 3 and in_speech:
                    pause_count += 1
                    in_speech = False
            else:
                silence_stretch = 0
                in_speech = True
                
        active_speech_ratio = sum(speech_frames) / num_frames
        
        # Calculate pace consistency based on speech frames energy deviation
        speech_rms = [r for r in rms_values if r > threshold]
        if len(speech_rms) > 1:
            mean_speech_rms = sum(speech_rms) / len(speech_rms)
            variance = sum((r - mean_speech_rms)**2 for r in speech_rms) / len(speech_rms)
            std_dev = math.sqrt(variance)
            norm_std = std_dev / (mean_speech_rms + 1e-6)
            pace_consistency = max(0.0, min(100.0, 100.0 - (norm_std * 50.0)))
        else:
            pace_consistency = 70.0
            
        return {
            "pause_count": pause_count,
            "active_speech_ratio": active_speech_ratio,
            "pace_consistency": pace_consistency
        }
    except Exception as e:
        print(f"Fallback acoustic analysis failure: {e}")
        return {"pause_count": 2, "active_speech_ratio": 0.8, "pace_consistency": 75.0}

def analyze_audio_pauses(audio_path: str, silence_threshold_ratio: float = 0.08, frame_duration_ms: int = 100) -> dict:
    """Acoustic analysis attempting scientific packages first, falling back to pure Python."""
    try:
        import numpy as np
        import scipy.io.wavfile as wav
        
        sample_rate, data = wav.read(audio_path)
        if len(data.shape) > 1:
            data = data.mean(axis=1)
        if len(data) == 0:
            return {"pause_count": 0, "active_speech_ratio": 1.0, "pace_consistency": 100.0}
            
        data = data.astype(float)
        frame_size = int(sample_rate * (frame_duration_ms / 1000.0))
        num_frames = len(data) // frame_size
        
        if num_frames == 0:
            return {"pause_count": 0, "active_speech_ratio": 1.0, "pace_consistency": 100.0}
            
        # Reshape to frames and compute RMS
        frames = data[:num_frames * frame_size].reshape((num_frames, frame_size))
        rms_values = np.sqrt(np.mean(frames**2, axis=1))
        
        max_rms = np.max(rms_values)
        if max_rms == 0:
            return {"pause_count": 0, "active_speech_ratio": 0.0, "pace_consistency": 0.0}
            
        threshold = max(max_rms * silence_threshold_ratio, np.mean(rms_values) * 0.3)
        speech_frames = (rms_values > threshold).astype(int)
        
        pause_count = 0
        silence_stretch = 0
        in_speech = True
        
        for frame_is_speech in speech_frames:
            if frame_is_speech == 0:
                silence_stretch += 1
                if silence_stretch >= 3 and in_speech:
                    pause_count += 1
                    in_speech = False
            else:
                silence_stretch = 0
                in_speech = True
                
        active_speech_ratio = float(np.sum(speech_frames) / num_frames)
        speech_rms = rms_values[rms_values > threshold]
        if len(speech_rms) > 1:
            variance = np.std(speech_rms) / (np.mean(speech_rms) + 1e-6)
            pace_consistency = max(0.0, min(100.0, 100.0 - (variance * 50.0)))
        else:
            pace_consistency = 70.0
            
        return {
            "pause_count": pause_count,
            "active_speech_ratio": active_speech_ratio,
            "pace_consistency": pace_consistency
        }
    except ImportError:
        # NumPy/SciPy are not available, use the pure-Python wave parser fallback
        return _analyze_audio_pauses_pure_python(audio_path, silence_threshold_ratio, frame_duration_ms)
    except Exception as e:
        print(f"Primary acoustic analysis crashed, using fallback: {e}")
        return _analyze_audio_pauses_pure_python(audio_path, silence_threshold_ratio, frame_duration_ms)

def calculate_scores(transcript: str, duration_sec: float, audio_path: str = None) -> dict:
    """Computes communication metrics, checking fillers and silence ratios."""
    words = [w for w in transcript.split() if w.strip()]
    word_count = len(words)
    
    if duration_sec <= 0:
        duration_sec = 1.0
        
    wpm = (word_count / duration_sec) * 60.0
    
    if wpm < 110:
        speed_category = "Slow"
    elif wpm <= 150:
        speed_category = "Normal"
    else:
        speed_category = "Fast"
        
    filler_count = analyze_transcript_fillers(transcript)
    
    if audio_path:
        acoustic = analyze_audio_pauses(audio_path)
    else:
        acoustic = {
            "pause_count": max(0, int(word_count // 30)),
            "active_speech_ratio": 0.85,
            "pace_consistency": 80.0
        }
        
    pauses_per_minute = (acoustic["pause_count"] / duration_sec) * 60.0
    pause_deduction = 0.0
    if pauses_per_minute > 20:
        pause_deduction = min(25.0, (pauses_per_minute - 20) * 1.5)
    elif pauses_per_minute < 3 and duration_sec > 10:
        pause_deduction = 10.0
        
    silence_deduction = 0.0
    if acoustic["active_speech_ratio"] < 0.65:
        silence_deduction = min(25.0, (0.65 - acoustic["active_speech_ratio"]) * 50)
    elif acoustic["active_speech_ratio"] > 0.92:
        silence_deduction = 15.0
        
    confidence_score = 100.0 - (filler_count * 3.0) - pause_deduction - silence_deduction
    confidence_score = (confidence_score * 0.7) + (acoustic["pace_consistency"] * 0.3)
    confidence_score = max(0, min(100, int(round(confidence_score))))
    
    wpm_diff = abs(wpm - 130)
    pacing_score = max(0.0, 100.0 - (wpm_diff * 0.8))
    
    fluency_score = 100.0 - (filler_count * 2.0)
    if acoustic["active_speech_ratio"] < 0.7:
        fluency_score -= (0.7 - acoustic["active_speech_ratio"]) * 100
    fluency_score = max(0, min(100, fluency_score))
    
    comm_score = (confidence_score * 0.4) + (fluency_score * 0.3) + (pacing_score * 0.3)
    communication_score = max(0, min(100, int(round(comm_score))))
    
    return {
        "word_count": word_count,
        "wpm": round(wpm, 1),
        "speed_category": speed_category,
        "confidence_score": confidence_score,
        "communication_score": communication_score,
        "filler_count": filler_count,
        "pause_count": acoustic["pause_count"],
        "active_speech_ratio": round(acoustic["active_speech_ratio"], 2),
        "pace_consistency": round(acoustic["pace_consistency"], 1)
    }

if __name__ == "__main__":
    test_text = "Uh, hello everyone. Um, today I want to talk about, like, communication skills."
    res = calculate_scores(test_text, 8.0)
    print("Scoring output test:", res)
