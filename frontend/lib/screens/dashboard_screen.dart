import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../models/session.dart';
import '../widgets/glass_card.dart';
import '../widgets/metrics_chart.dart';

class DashboardScreen extends StatelessWidget {
  final DashboardMetrics? metrics;
  final List<SpeechSession> sessions;
  final bool isLoading;
  final Future<void> Function() onRefresh;
  final ValueChanged<SpeechSession> onSessionSelect;
  final ValueChanged<String> onSessionDelete;

  const DashboardScreen({
    Key? key,
    required this.metrics,
    required this.sessions,
    required this.isLoading,
    required this.onRefresh,
    required this.onSessionSelect,
    required this.onSessionDelete,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    if (isLoading && metrics == null) {
      return const Center(child: CircularProgressIndicator());
    }

    final total = metrics?.totalRecordings ?? 0;
    final wpm = metrics?.averageWpm ?? 0.0;
    final conf = metrics?.averageConfidence ?? 0.0;
    final comm = metrics?.averageCommunication ?? 0.0;
    final trends = metrics?.trends ?? [];

    return RefreshIndicator(
      onRefresh: onRefresh,
      child: SingleChildScrollView(
        physics: const AlwaysScrollableScrollPhysics(),
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Communication Dashboard',
              style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold, fontFamily: 'Outfit'),
            ),
            const SizedBox(height: 8),
            const Text(
              'Analyze speed, confidence, and fluency statistics to improve vocal delivery.',
              style: TextStyle(color: Colors.grey, fontSize: 14),
            ),
            const SizedBox(height: 30),
            
            // 4 Stats Cards in grid
            _buildStatsGrid(context, total, wpm, conf, comm),
            const SizedBox(height: 30),
            
            // Main content rows
            LayoutBuilder(
              builder: (context, constraints) {
                if (constraints.maxWidth > 900) {
                  return Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Expanded(flex: 3, child: _buildProgressChartSection(context, trends)),
                      const SizedBox(width: 24),
                      Expanded(flex: 2, child: _buildHistorySection(context)),
                    ],
                  );
                } else {
                  return Column(
                    children: [
                      _buildProgressChartSection(context, trends),
                      const SizedBox(height: 24),
                      _buildHistorySection(context),
                    ],
                  );
                }
              },
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildStatsGrid(BuildContext context, int total, double wpm, double confidence, double communication) {
    final double cardWidth = (MediaQuery.of(context).size.width - 48) / 2;

    return GridView.count(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      crossAxisCount: MediaQuery.of(context).size.width > 600 ? 4 : 2,
      crossAxisSpacing: 16,
      mainAxisSpacing: 16,
      childAspectRatio: MediaQuery.of(context).size.width > 600 ? 1.6 : 1.3,
      children: [
        _buildStatCard(
          context,
          'Total Sessions',
          total.toString(),
          Icons.graphic_eq,
          Colors.purple,
        ),
        _buildStatCard(
          context,
          'Average Speed',
          '${wpm.round()} WPM',
          Icons.speed,
          Colors.teal,
        ),
        _buildStatCard(
          context,
          'Avg Confidence',
          '${confidence.round()}/100',
          Icons.emoji_events,
          Colors.pink,
        ),
        _buildStatCard(
          context,
          'Avg Communication',
          '${communication.round()}/100',
          Icons.analytics,
          Colors.purpleAccent,
        ),
      ],
    );
  }

  Widget _buildStatCard(BuildContext context, String title, String value, IconData icon, Color color) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    return GlassCard(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.between,
            children: [
              Text(
                title,
                style: TextStyle(
                  fontSize: 12,
                  fontWeight: FontWeight.bold,
                  color: isDark ? Colors.grey[400] : Colors.grey[600],
                ),
              ),
              Icon(icon, color: color, size: 20),
            ],
          ),
          Text(
            value,
            style: const TextStyle(
              fontSize: 22,
              fontWeight: FontWeight.bold,
              fontFamily: 'Outfit',
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildProgressChartSection(BuildContext context, List<ChartDataPoint> trends) {
    return GlassCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.between,
            children: [
              const Text(
                'Intelligence Progress',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, fontFamily: 'Outfit'),
              ),
              Row(
                children: [
                  _buildLegendIndicator(Colors.teal, 'Communication'),
                  const SizedBox(width: 12),
                  _buildLegendIndicator(Colors.purple, 'Confidence'),
                ],
              )
            ],
          ),
          const SizedBox(height: 24),
          SizedBox(
            height: 220,
            child: MetricsChart(data: trends),
          ),
        ],
      ),
    );
  }

  Widget _buildLegendIndicator(Color color, String text) {
    return Row(
      children: [
        Container(
          width: 8,
          height: 8,
          decoration: BoxDecoration(shape: BoxShape.circle, color: color),
        ),
        const SizedBox(width: 6),
        Text(text, style: const TextStyle(fontSize: 10, color: Colors.grey)),
      ],
    );
  }

  Widget _buildHistorySection(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    
    return GlassCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'Session History',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, fontFamily: 'Outfit'),
          ),
          const SizedBox(height: 16),
          sessions.isEmpty
              ? const Padding(
                  padding: EdgeInsets.symmetric(vertical: 40.0),
                  child: Center(
                    child: Text('No sessions recorded yet.', style: TextStyle(color: Colors.grey)),
                  ),
                )
              : ListView.separated(
                  shrinkWrap: true,
                  physics: const NeverScrollableScrollPhysics(),
                  itemCount: sessions.length > 5 ? 5 : sessions.length, // Limit to recent 5
                  separatorBuilder: (context, index) => const SizedBox(height: 10),
                  itemBuilder: (context, index) {
                    final session = sessions[index];
                    final date = DateFormat('MMM dd, hh:mm a').format(session.timestamp);
                    return ListTile(
                      dense: true,
                      contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                        side: BorderSide(
                          color: isDark ? Colors.white10 : Colors.black12,
                        ),
                      ),
                      tileColor: isDark ? Colors.white.withOpacity(0.02) : Colors.black.withOpacity(0.01),
                      title: Text(
                        'Speech Session',
                        style: TextStyle(fontWeight: FontWeight.bold, color: isDark ? Colors.white : Colors.black87),
                      ),
                      subtitle: Text('$date \u2022 ${session.duration.toStringAsFixed(1)}s \u2022 ${session.wordCount} words'),
                      trailing: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                            decoration: BoxDecoration(
                              color: Colors.teal.withOpacity(0.15),
                              borderRadius: BorderRadius.circular(8),
                            ),
                            child: Text(
                              'Score: ${session.communicationScore}',
                              style: const TextStyle(color: Colors.teal, fontWeight: FontWeight.bold, fontSize: 11),
                            ),
                          ),
                          const SizedBox(width: 8),
                          IconButton(
                            icon: const Icon(Icons.delete_outline, size: 18, color: Colors.grey),
                            onPressed: () => onSessionDelete(session.sessionId),
                          ),
                        ],
                      ),
                      onTap: () => onSessionSelect(session),
                    );
                  },
                ),
        ],
      ),
    );
  }
}
