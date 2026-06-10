import 'package:flutter/material.dart';
import 'dashboard_screen.dart';
import 'recorder_screen.dart';
import '../models/session.dart';
import '../services/api_service.dart';
import '../services/audio_service.dart';

class MainNavigation extends StatefulWidget {
  final VoidCallback onThemeToggle;
  final bool isDarkMode;

  const MainNavigation({
    Key? key,
    required this.onThemeToggle,
    required this.isDarkMode,
  }) : super(key: key);

  @override
  State<MainNavigation> createState() => _MainNavigationState();
}

class _MainNavigationState extends State<MainNavigation> {
  int _currentIndex = 0;
  
  // Shared services
  final ApiService _apiService = ApiService();
  final AudioService _audioService = AudioService();
  
  // Shared state variables
  SpeechSession? _currentSession;
  DashboardMetrics? _metrics;
  List<SpeechSession> _sessions = [];
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _fetchData();
  }

  Future<void> _fetchData() async {
    setState(() => _isLoading = true);
    try {
      final metrics = await _apiService.getDashboard();
      final sessions = await _apiService.getSessions();
      setState(() {
        _metrics = metrics;
        _sessions = sessions;
        _isLoading = false;
      });
    } catch (e) {
      setState(() => _isLoading = false);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error connecting to backend: $e')),
      );
    }
  }

  void _onSessionSelected(SpeechSession session) {
    setState(() {
      _currentSession = session;
      _currentIndex = 1; // Direct redirect to Recorder/Playback screen
    });
  }

  Future<void> _onSessionDelete(String id) async {
    final success = await _apiService.deleteSession(id);
    if (success) {
      if (_currentSession?.sessionId == id) {
        setState(() => _currentSession = null);
      }
      _fetchData();
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Session deleted successfully.')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final width = MediaQuery.of(context).size.width;
    final isDesktop = width > 800;

    final List<Widget> screens = [
      DashboardScreen(
        metrics: _metrics,
        sessions: _sessions,
        isLoading: _isLoading,
        onRefresh: _fetchData,
        onSessionSelect: _onSessionSelected,
        onSessionDelete: _onSessionDelete,
      ),
      RecorderScreen(
        apiService: _apiService,
        audioService: _audioService,
        currentSession: _currentSession,
        onSessionAnalyzed: (session) {
          setState(() => _currentSession = session);
          _fetchData(); // Reload stats
        },
      ),
    ];

    return Scaffold(
      appBar: !isDesktop
          ? AppBar(
              title: const Text('Echo AI', style: TextStyle(fontWeight: FontWeight.bold, fontFamily: 'Outfit')),
              actions: [
                IconButton(
                  icon: Icon(widget.isDarkMode ? Icons.light_mode : Icons.dark_mode),
                  onPressed: widget.onThemeToggle,
                ),
                IconButton(
                  icon: const Icon(Icons.refresh),
                  onPressed: _fetchData,
                ),
              ],
            )
          : null,
      body: Row(
        children: [
          if (isDesktop) _buildSidebar(context),
          Expanded(
            child: screens[_currentIndex],
          ),
        ],
      ),
      bottomNavigationBar: !isDesktop
          ? BottomNavigationBar(
              currentIndex: _currentIndex,
              onTap: (index) => setState(() => _currentIndex = index),
              items: const [
                BottomNavigationBarItem(
                  icon: Icon(Icons.dashboard_outlined),
                  activeIcon: Icon(Icons.dashboard),
                  label: 'Dashboard',
                ),
                BottomNavigationBarItem(
                  icon: Icon(Icons.mic_none_outlined),
                  activeIcon: Icon(Icons.mic),
                  label: 'Recorder',
                ),
              ],
            )
          : null,
    );
  }

  Widget _buildSidebar(BuildContext context) {
    final theme = Theme.of(context);
    return Container(
      width: 250,
      decoration: BoxDecoration(
        color: theme.cardColor.withOpacity(0.5),
        border: Border(
          right: BorderSide(color: theme.dividerColor),
        ),
      ),
      child: Column(
        children: [
          const SizedBox(height: 40),
          // Sidebar Logo Header
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Container(
                width: 38,
                height: 38,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(10),
                  gradient: const LinearGradient(colors: [Colors.purple, Colors.teal]),
                ),
                child: const Icon(Icons.graphic_eq, color: Colors.white, size: 20),
              ),
              const SizedBox(width: 12),
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: const [
                  Text('Echo AI', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, fontFamily: 'Outfit')),
                  Text('SPEECH INTELLIGENCE', style: TextStyle(fontSize: 9, letterSpacing: 0.5, color: Colors.grey)),
                ],
              )
            ],
          ),
          const SizedBox(height: 40),
          // Navigation links
          _buildSidebarItem(0, Icons.dashboard_outlined, Icons.dashboard, 'Dashboard'),
          _buildSidebarItem(1, Icons.mic_none_outlined, Icons.mic, 'Recorder & Effects'),
          const Spacer(),
          // Dark mode Toggle button in footer
          ListTile(
            leading: Icon(widget.isDarkMode ? Icons.light_mode : Icons.dark_mode),
            title: Text(widget.isDarkMode ? 'Light Mode' : 'Dark Mode', style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w600)),
            onTap: widget.onThemeToggle,
          ),
          ListTile(
            leading: const Icon(Icons.refresh),
            title: const Text('Refresh Data', style: TextStyle(fontSize: 13, fontWeight: FontWeight.w600)),
            onTap: _fetchData,
          ),
          const SizedBox(height: 20),
        ],
      ),
    );
  }

  Widget _buildSidebarItem(int index, IconData outlineIcon, IconData filledIcon, String title) {
    final isSelected = _currentIndex == index;
    final theme = Theme.of(context);

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 4.0),
      child: InkWell(
        onTap: () => setState(() => _currentIndex = index),
        borderRadius: BorderRadius.circular(12),
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 12.0, horizontal: 16.0),
          decoration: BoxDecoration(
            color: isSelected ? theme.primaryColor.withOpacity(0.1) : Colors.transparent,
            borderRadius: BorderRadius.circular(12),
          ),
          child: Row(
            children: [
              Icon(
                isSelected ? filledIcon : outlineIcon,
                color: isSelected ? theme.primaryColor : theme.iconTheme.color?.withOpacity(0.7),
                size: 20,
              ),
              const SizedBox(width: 16),
              Text(
                title,
                style: TextStyle(
                  fontSize: 14,
                  fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                  color: isSelected ? theme.primaryColor : theme.textTheme.bodyMedium?.color?.withOpacity(0.8),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
