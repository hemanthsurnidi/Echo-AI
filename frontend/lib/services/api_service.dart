import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/session.dart';

class ApiService {
  // Can be configured to remote production URL (e.g. Render app URL)
  static String baseUrl = 'http://localhost:8000';

  Future<DashboardMetrics> getDashboard() async {
    final response = await http.get(Uri.parse('$baseUrl/api/dashboard'));
    if (response.statusCode == 200) {
      return DashboardMetrics.fromJson(json.decode(response.body));
    } else {
      throw Exception('Failed to load dashboard metrics');
    }
  }

  Future<List<SpeechSession>> getSessions() async {
    final response = await http.get(Uri.parse('$baseUrl/api/sessions'));
    if (response.statusCode == 200) {
      final List<dynamic> data = json.decode(response.body);
      return data.map((json) => SpeechSession.fromJson(json)).toList();
    } else {
      throw Exception('Failed to load sessions list');
    }
  }

  Future<bool> deleteSession(String sessionId) async {
    final response = await http.delete(Uri.parse('$baseUrl/api/sessions/$sessionId'));
    return response.statusCode == 200;
  }

  Future<SpeechSession> analyzeAudio(List<int> audioBytes, double duration) async {
    final uri = Uri.parse('$baseUrl/api/analyze');
    final request = http.MultipartRequest('POST', uri);
    
    // Add audio file bytes as multipart
    final multipartFile = http.MultipartFile.fromBytes(
      'file',
      audioBytes,
      filename: 'recording.wav',
    );
    request.files.add(multipartFile);
    
    // Add text field metadata
    request.fields['duration'] = duration.toString();

    final streamedResponse = await request.send();
    final response = await http.Response.fromStream(streamedResponse);

    if (response.statusCode == 200) {
      return SpeechSession.fromJson(json.decode(response.body));
    } else {
      throw Exception('Failed to upload and analyze audio: ${response.body}');
    }
  }

  Future<String> getVoiceEffectUrl(String sessionId, String effect) async {
    final uri = Uri.parse('$baseUrl/api/voice-effect');
    final response = await http.post(
      uri,
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'session_id': sessionId,
        'effect': effect,
      }),
    );

    if (response.statusCode == 200) {
      final Map<String, dynamic> data = json.decode(response.body);
      // Return absolute path to the processed audio file
      return '$baseUrl${data['processed_audio']}';
    } else {
      throw Exception('Failed to apply voice effect: ${response.body}');
    }
  }
}
