import 'package:flutter/material.dart';
import 'screens/main_navigation.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const EchoApp());
}

class EchoApp extends StatefulWidget {
  const EchoApp({Key? key}) : super(key: key);

  @override
  State<EchoApp> createState() => _EchoAppState();
}

class _EchoAppState extends State<EchoApp> {
  bool _isDarkMode = true;

  void _toggleTheme() {
    setState(() {
      _isDarkMode = !_isDarkMode;
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Echo AI',
      debugShowCheckedModeBanner: false,
      
      // Premium dark mode configuration
      themeMode: _isDarkMode ? ThemeMode.dark : ThemeMode.light,
      
      darkTheme: ThemeData(
        brightness: Brightness.dark,
        primaryColor: const Color(0xFF8B5CF6), // Electric Purple
        scaffoldBackgroundColor: const Color(0xFF0A0B10), // Sleek Dark space
        cardColor: const Color(0xFF141625).withOpacity(0.6),
        dividerColor: Colors.white.withOpacity(0.08),
        iconTheme: const IconThemeData(color: Colors.white),
        textTheme: const TextTheme(
          bodyLarge: TextStyle(fontFamily: 'PlusJakartaSans', color: Colors.white),
          bodyMedium: TextStyle(fontFamily: 'PlusJakartaSans', color: Colors.white70),
        ),
        colorScheme: const ColorScheme.dark(
          primary: Color(0xFF8B5CF6),
          secondary: Color(0xFF14B8A6), // Teal accent
          background: Color(0xFF0A0B10),
          surface: Color(0xFF141625),
        ),
      ),
      
      // Clean light mode configuration
      theme: ThemeData(
        brightness: Brightness.light,
        primaryColor: const Color(0xFF7C3AED), // Slightly deeper purple
        scaffoldBackgroundColor: const Color(0xFFF8FAFC), // Sleek off-white slate
        cardColor: Colors.white.withOpacity(0.75),
        dividerColor: Colors.black.withOpacity(0.08),
        iconTheme: const IconThemeData(color: Colors.black87),
        textTheme: const TextTheme(
          bodyLarge: TextStyle(fontFamily: 'PlusJakartaSans', color: Colors.black87),
          bodyMedium: TextStyle(fontFamily: 'PlusJakartaSans', color: Colors.black54),
        ),
        colorScheme: const ColorScheme.light(
          primary: Color(0xFF7C3AED),
          secondary: Color(0xFF0D9488),
          background: Color(0xFFF8FAFC),
          surface: Colors.white,
        ),
      ),
      
      home: MainNavigation(
        isDarkMode: _isDarkMode,
        onThemeToggle: _toggleTheme,
      ),
    );
  }
}
