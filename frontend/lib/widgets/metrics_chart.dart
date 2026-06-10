import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import '../models/session.dart';

class MetricsChart extends StatelessWidget {
  final List<ChartDataPoint> data;

  const MetricsChart({
    Key? key,
    required this.data,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    if (data.length < 2) {
      return const Center(
        child: Text(
          'Need at least 2 sessions to display trend graph.',
          style: TextStyle(color: Colors.grey),
        ),
      );
    }

    final isDark = Theme.of(context).brightness == Brightness.dark;

    // Map trends points to FlSpot list
    final List<FlSpot> communicationSpots = [];
    final List<FlSpot> confidenceSpots = [];

    for (int i = 0; i < data.length; i++) {
      communicationSpots.add(FlSpot(i.toDouble(), data[i].communicationScore));
      confidenceSpots.add(FlSpot(i.toDouble(), data[i].confidenceScore));
    }

    return LineChart(
      LineChartData(
        gridData: FlGridData(
          show: true,
          drawVerticalLine: false,
          horizontalInterval: 25,
          getDrawingHorizontalLine: (value) {
            return FlLine(
              color: isDark ? Colors.white12 : Colors.black12,
              strokeWidth: 1,
              dashArray: [4, 4],
            );
          },
        ),
        titlesData: FlTitlesData(
          show: true,
          rightTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
          topTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
          bottomTitles: AxisTitles(
            sideTitles: SideTitles(
              showTitles: true,
              reservedSize: 22,
              interval: 1,
              getTitlesWidget: (value, meta) {
                int index = value.toInt();
                if (index >= 0 && index < data.length) {
                  // Only print subset of labels to prevent crowding
                  if (data.length <= 6 || index % (data.length ~/ 4) == 0 || index == data.length - 1) {
                    return Padding(
                      padding: const EdgeInsets.only(top: 6.0),
                      child: Text(
                        data[index].label,
                        style: TextStyle(
                          color: isDark ? Colors.grey[400] : Colors.grey[600],
                          fontSize: 9,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    );
                  }
                }
                return const SizedBox.shrink();
              },
            ),
          ),
          leftTitles: AxisTitles(
            sideTitles: SideTitles(
              showTitles: true,
              interval: 25,
              reservedSize: 28,
              getTitlesWidget: (value, meta) {
                return Text(
                  value.toInt().toString(),
                  style: TextStyle(
                    color: isDark ? Colors.grey[400] : Colors.grey[600],
                    fontSize: 9,
                    fontWeight: FontWeight.bold,
                  ),
                );
              },
            ),
          ),
        ),
        borderData: FlBorderData(show: false),
        minX: 0,
        maxX: (data.length - 1).toDouble(),
        minY: 0,
        maxY: 100,
        lineBarsData: [
          // Communication Line (Teal color)
          LineChartBarData(
            spots: communicationSpots,
            isCurved: true,
            color: Colors.teal,
            barWidth: 4,
            isStrokeCapRound: true,
            dotData: const FlDotData(show: true),
            belowBarData: BarAreaData(
              show: true,
              color: Colors.teal.withOpacity(0.1),
            ),
          ),
          // Confidence Line (Purple color)
          LineChartBarData(
            spots: confidenceSpots,
            isCurved: true,
            color: Colors.purple,
            barWidth: 3,
            isStrokeCapRound: true,
            dotData: const FlDotData(show: false),
            belowBarData: BarAreaData(
              show: true,
              color: Colors.purple.withOpacity(0.05),
            ),
          ),
        ],
      ),
    );
  }
}
