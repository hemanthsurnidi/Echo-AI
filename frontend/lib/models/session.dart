class SpeechSession {
  final String sessionId;
  final DateTime timestamp;
  final String transcript;
  final int wordCount;
  final double wpm;
  final String speedCategory;
  final int confidenceScore;
  final int communicationScore;
  final double duration;
  final String audioFilename;

  SpeechSession({
    required this.sessionId,
    required this.timestamp,
    required this.transcript,
    required this.wordCount,
    required this.wpm,
    required this.speedCategory,
    required this.confidenceScore,
    required this.communicationScore,
    required this.duration,
    required this.audioFilename,
  });

  factory SpeechSession.fromJson(Map<String, dynamic> json) {
    return SpeechSession(
      sessionId: json['session_id'] as String,
      timestamp: DateTime.parse(json['timestamp'] as String),
      transcript: json['transcript'] as String,
      wordCount: json['word_count'] as int,
      wpm: (json['wpm'] as num).toDouble(),
      speedCategory: json['speed_category'] as String,
      confidenceScore: json['confidence_score'] as int,
      communicationScore: json['communication_score'] as int,
      duration: (json['duration'] as num).toDouble(),
      audioFilename: json['audio_filename'] as String,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'session_id': sessionId,
      'timestamp': timestamp.toIso8601String(),
      'transcript': transcript,
      'word_count': wordCount,
      'wpm': wpm,
      'speed_category': speedCategory,
      'confidence_score': confidenceScore,
      'communication_score': communicationScore,
      'duration': duration,
      'audio_filename': audioFilename,
    };
  }
}

class DashboardMetrics {
  final int totalRecordings;
  final double averageWpm;
  final double averageConfidence;
  final double averageCommunication;
  final List<ChartDataPoint> trends;
  final List<SpeechSession> recentSessions;

  DashboardMetrics({
    required this.totalRecordings,
    required this.averageWpm,
    required this.averageConfidence,
    required this.averageCommunication,
    required this.trends,
    required this.recentSessions,
  });

  factory DashboardMetrics.fromJson(Map<String, dynamic> json) {
    var trendList = json['wpm_trend'] as List? ?? [];
    List<ChartDataPoint> parsedTrends = trendList
        .map((item) => ChartDataPoint.fromJson(item as Map<String, dynamic>))
        .toList();

    var sessionsList = json['recent_sessions'] as List? ?? [];
    List<SpeechSession> parsedSessions = sessionsList
        .map((item) => SpeechSession.fromJson(item as Map<String, dynamic>))
        .toList();

    return DashboardMetrics(
      totalRecordings: json['total_recordings'] as int,
      averageWpm: (json['average_wpm'] as num).toDouble(),
      averageConfidence: (json['average_confidence'] as num).toDouble(),
      averageCommunication: (json['average_communication'] as num).toDouble(),
      trends: parsedTrends,
      recentSessions: parsedSessions,
    );
  }
}

class ChartDataPoint {
  final String label;
  final double wpm;
  final double confidenceScore;
  final double communicationScore;

  ChartDataPoint({
    required this.label,
    required this.wpm,
    required this.confidenceScore,
    required this.communicationScore,
  });

  factory ChartDataPoint.fromJson(Map<String, dynamic> json) {
    return ChartDataPoint(
      label: json['label'] as String,
      wpm: (json['wpm'] as num).toDouble(),
      confidenceScore: (json['confidence_score'] as num).toDouble(),
      communicationScore: (json['communication_score'] as num).toDouble(),
    );
  }
}
