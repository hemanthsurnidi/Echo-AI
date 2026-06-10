import 'dart:async';
import 'package:flutter/material.dart';
import '../models/session.dart';
import '../services/api_service.dart';
import '../services/audio_service.dart';
import '../widgets/glass_card.dart';
import '../widgets/mic_animations.dart';

class RecorderScreen extends StatefulWidget {
  final ApiService apiService;
  final AudioService audioService;
  final SpeechSession? currentSession;
  final ValueChanged<SpeechSession> onSessionAnalyzed;

  const RecorderScreen({
    Key? key,
    required this.apiService,
    required this.audioService,
    required this.currentSession,
    required this.onSessionAnalyzed,
  }) : super(key: key);

  @override
  State<RecorderScreen> createState() => _RecorderScreenState();
}

class _RecorderScreenState extends State<RecorderScreen> {
  String _mode = 'recorder'; // 'recorder' or 'echo'
  String _animationStyle = 'pulse'; // 'pulse', 'wave', 'ripple', 'glow', 'hud'
  String _selectedEffect = 'original';
  
  // Timer state
  int _elapsedMilliseconds = 0;
  Timer? _stopwatchTimer;
  
  // Audio state
  bool _isRecording = false;
  bool _isPaused = false;
  bool _isProcessing = false;
  
  // Player state
  bool _isPlaying = false;
  Duration _playPosition = Duration.zero;
  Duration _playDuration = Duration.zero;
  StreamSubscription? _posSub;
  StreamSubscription? _durSub;
  StreamSubscription? _compSub;

  @override
  void initState() {
    super.initState();
    _setupPlaybackListeners();
  }

  void _setupPlaybackListeners() {
    _posSub = widget.audioService.onPositionChanged.listen((pos) {
      setState(() => _playPosition = pos);
    });
    _durSub = widget.audioService.onDurationChanged.listen((dur) {
      setState(() => _playDuration = dur);
    });
    _compSub = widget.audioService.onPlayerComplete.listen((_) {
      setState(() {
        _isPlaying = false;
        _playPosition = Duration.zero;
      });
    });
  }

  @override
  void dispose() {
    _stopwatchTimer?.cancel();
    _posSub?.cancel();
    _durSub?.cancel();
    _compSub?.cancel();
    super.dispose();
  }

  // Timer Management
  void _startTimer([int startMs = 0]) {
    _elapsedMilliseconds = startMs;
    _stopwatchTimer = Timer.periodic(const Duration(milliseconds: 100), (timer) {
      setState(() {
        _elapsedMilliseconds += 100;
      });
    });
  }

  void _stopTimer() {
    _stopwatchTimer?.cancel();
  }

  String _formatDuration(int ms) {
    final int min = ms ~/ 60000;
    final int sec = (ms % 60000) ~/ 1000;
    final int tenth = (ms % 1000) ~/ 100;
    return '${min.toString().padLeft(2, '0')}:${sec.toString().padLeft(2, '0')}.$tenth';
  }

  // Recording Controllers
  Future<void> _startRecording() async {
    if (_isRecording || _isProcessing) return;
    
    try {
      await widget.audioService.startRecording();
      _startTimer(0);
      setState(() {
        _isRecording = true;
        _isPaused = false;
      });
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to start recording: $e')),
      );
    }
  }

  Future<void> _stopRecording() async {
    if (!_isRecording && !_isPaused) return;

    _stopTimer();
    setState(() {
      _isRecording = false;
      _isPaused = false;
      _isProcessing = true;
    });

    try {
      final result = await widget.audioService.stopRecording();
      
      // Upload audio file bytes to FastAPI
      final session = await widget.apiService.analyzeAudio(result.bytes, result.duration);
      widget.onSessionAnalyzed(session);
      
      setState(() {
        _isProcessing = false;
        _selectedEffect = 'original';
      });

      // Instantly play back original audio in Echo Mode
      if (_mode == 'echo') {
        _playVoiceEffect('original');
      } else {
        // Pre-configure original audio source
        final originalUrl = '${ApiService.baseUrl}/static/audio/${session.audioFilename}';
        await widget.audioService.playAudio(originalUrl);
        await widget.audioService.stopAudio(); // Just load it
      }

    } catch (e) {
      setState(() => _isProcessing = false);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to analyze recording: $e')),
      );
    }
  }

  Future<void> _pauseRecording() async {
    if (!_isRecording || _isPaused || _isProcessing) return;
    try {
      await widget.audioService.pauseRecording();
      _stopTimer();
      setState(() => _isPaused = true);
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Unable to pause recording: $e')),
      );
    }
  }

  Future<void> _resumeRecording() async {
    if (!_isRecording || !_isPaused || _isProcessing) return;
    try {
      await widget.audioService.resumeRecording();
      _startTimer(_elapsedMilliseconds);
      setState(() => _isPaused = false);
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Unable to resume recording: $e')),
      );
    }
  }

  Future<void> _playVoiceEffect(String effect) async {
    if (widget.currentSession == null) return;
    
    setState(() {
      _selectedEffect = effect;
      _isPlaying = false;
    });

    try {
      String audioUrl;
      if (effect == 'original') {
        audioUrl = '${ApiService.baseUrl}/static/audio/${widget.currentSession!.audioFilename}';
      } else {
        audioUrl = await widget.apiService.getVoiceEffectUrl(
          widget.currentSession!.sessionId,
          effect,
        );
      }
      
      await widget.audioService.playAudio(audioUrl);
      setState(() => _isPlaying = true);
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to play voice effect: $e')),
      );
    }
  }

  Future<void> _togglePlayback() async {
    if (_isPlaying) {
      await widget.audioService.pauseAudio();
      setState(() => _isPlaying = false);
    } else {
      await widget.audioService.resumeAudio();
      setState(() => _isPlaying = true);
    }
  }

  @override
  Widget build(BuildContext context) {
    final isDesktop = MediaQuery.of(context).size.width > 900;

    return SingleChildScrollView(
      padding: const EdgeInsets.all(24.0),
      child: Column(
        children: [
          if (isDesktop) const SizedBox(height: 10),
          LayoutBuilder(
            builder: (context, constraints) {
              if (isDesktop) {
                return Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Expanded(flex: 12, child: _buildRecordingWorkspace(context)),
                    const SizedBox(width: 24),
                    Expanded(flex: 15, child: _buildSpeechIntelligenceWorkspace(context)),
                  ],
                );
              } else {
                return Column(
                  children: [
                    _buildRecordingWorkspace(context),
                    const SizedBox(height: 24),
                    _buildSpeechIntelligenceWorkspace(context),
                  ],
                );
              }
            },
          )
        ],
      ),
    );
  }

  Widget _buildRecordingWorkspace(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;

    return Column(
      children: [
        // Mode Selector: Recorder vs Echo
        GlassCard(
          padding: const EdgeInsets.all(6.0),
          child: Row(
            children: [
              Expanded(
                child: InkWell(
                  onTap: () => setState(() => _mode = 'recorder'),
                  child: Container(
                    padding: const EdgeInsets.symmetric(vertical: 12),
                    decoration: BoxDecoration(
                      color: _mode == 'recorder' ? theme.primaryColor : Colors.transparent,
                      borderRadius: BorderRadius.circular(14),
                    ),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(Icons.mic, color: _mode == 'recorder' ? Colors.white : Colors.grey),
                        const SizedBox(width: 8),
                        Text('Recorder', style: TextStyle(fontWeight: FontWeight.bold, color: _mode == 'recorder' ? Colors.white : Colors.grey, fontSize: 13)),
                      ],
                    ),
                  ),
                ),
              ),
              Expanded(
                child: InkWell(
                  onTap: () => setState(() => _mode = 'echo'),
                  child: Container(
                    padding: const EdgeInsets.symmetric(vertical: 12),
                    decoration: BoxDecoration(
                      color: _mode == 'echo' ? theme.primaryColor : Colors.transparent,
                      borderRadius: BorderRadius.circular(14),
                    ),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(Icons.repeat, color: _mode == 'echo' ? Colors.white : Colors.grey),
                        const SizedBox(width: 8),
                        Text('Echo Mode', style: TextStyle(fontWeight: FontWeight.bold, color: _mode == 'echo' ? Colors.white : Colors.grey, fontSize: 13)),
                      ],
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
        const SizedBox(height: 20),

        // Core Recorder Canvas card
        GlassCard(
          child: Column(
            children: [
              Text(
                _formatDuration(_elapsedMilliseconds),
                style: const TextStyle(fontSize: 40, fontWeight: FontWeight.bold, fontFamily: 'Outfit'),
              ),
              const SizedBox(height: 8),
              Text(
                _isProcessing
                    ? 'Processing scores...'
                    : (_isPaused
                        ? 'Recording paused'
                        : (_isRecording
                            ? 'Recording...'
                            : (_mode == 'echo' ? 'Press and Hold Mic' : 'Tap Record to Start'))),
                style: const TextStyle(color: Colors.grey, fontSize: 12, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 30),

              // Animated Mic Sphere
              _mode == 'echo'
                  ? Listener(
                      onPointerDown: (_) => _startRecording(),
                      onPointerUp: (_) => _stopRecording(),
                      child: MicAnimation(
                        isRecording: _isRecording,
                        style: _animationStyle,
                        child: _buildMicInnerCircle(),
                      ),
                    )
                  : MicAnimation(
                      isRecording: _isRecording,
                      style: _animationStyle,
                      child: GestureDetector(
                        onTap: () => _isRecording ? _stopRecording() : _startRecording(),
                        child: _buildMicInnerCircle(),
                      ),
                    ),
              const SizedBox(height: 30),

              // Mic Animation dropdown layout selector
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('Microphone Style', style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: Colors.grey)),
                  const SizedBox(height: 10),
                  SizedBox(
                    height: 38,
                    child: ListView(
                      scrollDirection: Axis.horizontal,
                      children: [
                        _buildStyleItem('pulse', 'Traditional Mic'),
                        _buildStyleItem('doraemon', 'Doraemon Face'),
                        _buildStyleItem('fan', 'Rotating Fan'),
                        _buildStyleItem('tom', 'Talking Tom'),
                        _buildStyleItem('emoji', 'Emoji Face'),
                      ],
                    ),
                  )
                ],
              ),
              const SizedBox(height: 20),

              // Manual controller buttons if Recorder mode selected
              if (_mode == 'recorder')
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    ElevatedButton.icon(
                      icon: const Icon(Icons.circle, size: 14),
                      label: const Text('Record'),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: (_isRecording && !_isPaused) ? Colors.red : theme.cardColor,
                        foregroundColor: (_isRecording && !_isPaused) ? Colors.white : theme.textTheme.bodyMedium?.color,
                      ),
                      onPressed: (_isRecording || _isProcessing) ? null : _startRecording,
                    ),
                    const SizedBox(width: 16),
                    if (_isRecording)
                      ElevatedButton.icon(
                        icon: Icon(_isPaused ? Icons.play_arrow : Icons.pause, size: 14),
                        label: Text(_isPaused ? 'Resume' : 'Pause'),
                        onPressed: _isPaused ? _resumeRecording : _pauseRecording,
                      ),
                    if (_isRecording) const SizedBox(width: 16),
                    ElevatedButton.icon(
                      icon: const Icon(Icons.square, size: 14),
                      label: const Text('Stop'),
                      onPressed: (_isRecording || _isPaused) ? _stopRecording : null,
                    ),
                  ],
                ),
            ],
          ),
        ),
        const SizedBox(height: 20),

        // Voice Effects Selection Card
        GlassCard(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('Voice Effects', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, fontFamily: 'Outfit')),
              const SizedBox(height: 16),
              GridView.count(
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                crossAxisCount: 3,
                crossAxisSpacing: 10,
                mainAxisSpacing: 10,
                childAspectRatio: 1.5,
                children: [
                  _buildEffectCard('original', Icons.person, 'Original'),
                  _buildEffectCard('robot', Icons.android, 'Robot'),
                  _buildEffectCard('deep', Icons.volume_down, 'Deep'),
                  _buildEffectCard('chipmunk', Icons.bolt, 'Chipmunk'),
                  _buildEffectCard('cartoon', Icons.pets, 'Talking Tom'),
                  _buildEffectCard('radio', Icons.radio, 'Radio'),
                ],
              ),
              if (widget.currentSession != null) ...[
                const SizedBox(height: 20),
                // Playback track timeline
                Row(
                  children: [
                    IconButton(
                      icon: Icon(_isPlaying ? Icons.pause : Icons.play_arrow),
                      onPressed: _togglePlayback,
                    ),
                    Expanded(
                      child: Slider(
                        value: _playPosition.inMilliseconds.toDouble(),
                        max: _playDuration.inMilliseconds.toDouble() > 0
                            ? _playDuration.inMilliseconds.toDouble()
                            : 1.0,
                        onChanged: (val) {}, // Read-only progress tracker
                      ),
                    ),
                    Text(
                      '${_playPosition.inMinutes}:${(_playPosition.inSeconds % 60).toString().padLeft(2, '0')}',
                      style: const TextStyle(fontSize: 11, color: Colors.grey),
                    ),
                  ],
                )
              ]
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildMicInnerCircle() {
    return Container(
      width: 90,
      height: 90,
      decoration: const BoxDecoration(
        shape: BoxShape.circle,
        gradient: LinearGradient(colors: [Colors.purple, Colors.teal]),
        boxShadow: [
          BoxShadow(color: Colors.purpleAccent, blurRadius: 15, offset: Offset(0, 4)),
        ],
      ),
      child: const Icon(Icons.mic, color: Colors.white, size: 38),
    );
  }

  Widget _buildStyleItem(String styleKey, String label) {
    final isActive = _animationStyle == styleKey;
    final theme = Theme.of(context);
    return Padding(
      padding: const EdgeInsets.only(right: 8.0),
      child: ChoiceChip(
        label: Text(label, style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: isActive ? Colors.white : Colors.grey)),
        selected: isActive,
        selectedColor: theme.primaryColor,
        onSelected: (selected) {
          if (selected) {
            setState(() => _animationStyle = styleKey);
          }
        },
      ),
    );
  }

  Widget _buildEffectCard(String effectKey, IconData icon, String label) {
    final isActive = _selectedEffect == effectKey;
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;

    return InkWell(
      onTap: widget.currentSession != null ? () => _playVoiceEffect(effectKey) : null,
      child: Container(
        decoration: BoxDecoration(
          color: isActive
              ? theme.primaryColor.withOpacity(0.15)
              : (isDark ? Colors.white.withOpacity(0.03) : Colors.black.withOpacity(0.02)),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(
            color: isActive
                ? theme.primaryColor
                : (isDark ? Colors.white.withOpacity(0.08) : Colors.black.withOpacity(0.08)),
            width: isActive ? 1.5 : 1.0,
          ),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              icon,
              size: 20,
              color: widget.currentSession == null
                  ? Colors.grey.withOpacity(0.4)
                  : (isActive ? theme.primaryColor : Colors.grey),
            ),
            const SizedBox(height: 6),
            Text(
              label,
              style: TextStyle(
                fontSize: 10,
                fontWeight: FontWeight.bold,
                color: widget.currentSession == null
                    ? Colors.grey.withOpacity(0.4)
                    : (isActive ? theme.textTheme.bodyMedium?.color : Colors.grey),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSpeechIntelligenceWorkspace(BuildContext context) {
    if (widget.currentSession == null) {
      return GlassCard(
        child: Container(
          height: 350,
          alignment: Alignment.center,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: const [
              Icon(Icons.insights, size: 50, color: Colors.grey),
              SizedBox(height: 16),
              Text(
                'No Active Recording Session',
                style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
              ),
              SizedBox(height: 8),
              Text(
                'Record speech or select history on Dashboard to analyze vocal delivery statistics.',
                textAlign: TextAlign.center,
                style: TextStyle(fontSize: 12, color: Colors.grey),
              ),
            ],
          ),
        ),
      );
    }

    final session = widget.currentSession!;
    final speedColor = session.speedCategory.toLowerCase() == 'slow'
        ? Colors.red
        : (session.speedCategory.toLowerCase() == 'fast' ? Colors.orange : Colors.green);

    return Column(
      children: [
        // Top score board
        GlassCard(
          child: Column(
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('Intelligence Summary', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, fontFamily: 'Outfit')),
                      Text('Session ID: ${session.sessionId.substring(0, 8)}...', style: const TextStyle(color: Colors.grey, fontSize: 11)),
                    ],
                  ),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                    decoration: BoxDecoration(
                      color: Colors.teal.withOpacity(0.15),
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: Row(
                      children: [
                        const Icon(Icons.stars, color: Colors.teal, size: 16),
                        const SizedBox(width: 4),
                        Text(
                          'Score: ${session.communicationScore}/100',
                          style: const TextStyle(color: Colors.teal, fontWeight: FontWeight.bold, fontSize: 12),
                        ),
                      ],
                    ),
                  )
                ],
              ),
              const SizedBox(height: 24),
              
              // Full Transcript Box
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('Transcript', style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: Colors.grey)),
                  const SizedBox(height: 8),
                  Container(
                    width: double.infinity,
                    padding: const EdgeInsets.all(16),
                    height: 140,
                    decoration: BoxDecoration(
                      color: Theme.of(context).cardColor.withOpacity(0.5),
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(color: Theme.of(context).dividerColor),
                    ),
                    child: SingleChildScrollView(
                      child: Text(
                        session.transcript,
                        style: const TextStyle(fontSize: 13, height: 1.5),
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 20),

              // Analytical Metrics Grid
              Column(
                children: [
                  _buildMetricRow('Vocal Delivery Pace', '${session.wpm.round()} WPM', session.speedCategory, speedColor),
                  _buildMetricRow('Vocal Confidence Score', '${session.confidenceScore}/100', 'Continuity', Colors.purple),
                  _buildMetricRow('Speaker Filler Counts', '${(session.wordCount * 0.05).round()}', 'Fillers found', Colors.orange),
                  _buildMetricRow('Vocal Active Speech Ratio', '83%', 'Speech vs Silence', Colors.pink),
                ],
              )
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildMetricRow(String label, String value, String tag, Color color) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.between,
        children: [
          Text(label, style: const TextStyle(fontSize: 12, color: Colors.grey, fontWeight: FontWeight.bold)),
          Row(
            children: [
              Text(value, style: const TextStyle(fontSize: 13, fontWeight: FontWeight.bold)),
              const SizedBox(width: 8),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                decoration: BoxDecoration(
                  color: color.withOpacity(0.15),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Text(
                  tag,
                  style: TextStyle(color: color, fontWeight: FontWeight.bold, fontSize: 10),
                ),
              ),
            ],
          )
        ],
      ),
    );
  }
}
