import 'dart:async';
import 'dart:typed_data';
import 'package:record/record.dart';
import 'package:audioplayers/audioplayers.dart';
import 'package:http/http.dart' as http;

class AudioService {
  final _audioRecorder = AudioRecorder();
  final _audioPlayer = AudioPlayer();
  
  bool _isRecording = false;
  bool _isPaused = false;
  DateTime? _recordStartTime;
  DateTime? _pauseStartTime;
  Duration _accumulatedPauseDuration = Duration.zero;
  
  bool get isRecording => _isRecording;
  bool get isPaused => _isPaused;

  Future<void> startRecording() async {
    if (await _audioRecorder.hasPermission()) {
      
      // Standard PCM 16-bit WAV configuration
      await _audioRecorder.start(
        const RecordConfig(
          encoder: AudioEncoder.wav,
          sampleRate: 44100,
          numChannels: 1,
        ),
        path: '', // Saves to browser memory blob on Web
      );
      
      _recordStartTime = DateTime.now();
      _pauseStartTime = null;
      _accumulatedPauseDuration = Duration.zero;
      _isPaused = false;
      _isRecording = true;
    } else {
      throw Exception('Microphone permission denied');
    }
  }

  Future<void> pauseRecording() async {
    if (!_isRecording || _isPaused) return;
    await _audioRecorder.pause();
    _pauseStartTime = DateTime.now();
    _isPaused = true;
  }

  Future<void> resumeRecording() async {
    if (!_isRecording || !_isPaused) return;
    await _audioRecorder.resume();
    if (_pauseStartTime != null) {
      _accumulatedPauseDuration += DateTime.now().difference(_pauseStartTime!);
      _pauseStartTime = null;
    }
    _isPaused = false;
  }

  Future<RecordResult> stopRecording() async {
    if (!_isRecording) {
      throw Exception('Recording is not active');
    }

    if (_isPaused && _pauseStartTime != null) {
      _accumulatedPauseDuration += DateTime.now().difference(_pauseStartTime!);
      _pauseStartTime = null;
      _isPaused = false;
    }

    final path = await _audioRecorder.stop();
    _isRecording = false;
    
    final activeMilliseconds = DateTime.now().difference(_recordStartTime!).inMilliseconds - _accumulatedPauseDuration.inMilliseconds;
    final durationSec = activeMilliseconds > 0 ? activeMilliseconds / 1000.0 : 0.0;

    if (path == null) {
      throw Exception('Recording path was null. Failed to record.');
    }

    // On web, the path is a blob URL (e.g. blob:http://...)
    // We fetch the bytes from this blob URL to upload to the backend
    final response = await http.get(Uri.parse(path));
    if (response.statusCode == 200) {
      return RecordResult(
        bytes: response.bodyBytes,
        duration: durationSec,
      );
    } else {
      throw Exception('Failed to retrieve audio bytes from blob');
    }
  }

  Future<void> playAudio(String url) async {
    await _audioPlayer.stop();
    await _audioPlayer.play(UrlSource(url));
  }

  Future<void> stopAudio() async {
    await _audioPlayer.stop();
  }

  Future<void> pauseAudio() async {
    await _audioPlayer.pause();
  }

  Future<void> resumeAudio() async {
    await _audioPlayer.resume();
  }

  Stream<Duration> get onPositionChanged => _audioPlayer.onPositionChanged;
  Stream<Duration> get onDurationChanged => _audioPlayer.onDurationChanged;
  Stream<void> get onPlayerComplete => _audioPlayer.onPlayerComplete;

  void dispose() {
    _audioRecorder.dispose();
    _audioPlayer.dispose();
  }
}

class RecordResult {
  final Uint8List bytes;
  final double duration;

  RecordResult({required this.bytes, required this.duration});
}
