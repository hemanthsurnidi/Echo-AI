import 'dart:ui';
import 'package:flutter/material.dart';

class GlassCard extends StatelessWidget {
  final Widget child;
  final double blur;
  final double borderRadius;
  final EdgeInsetsGeometry padding;
  final Color? color;
  final Border? border;

  const GlassCard({
    Key? key,
    required this.child,
    this.blur = 16.0,
    this.borderRadius = 20.0,
    this.padding = const EdgeInsets.all(24.0),
    this.color,
    this.border,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    
    final defaultColor = isDark
        ? Colors.white.withOpacity(0.05)
        : Colors.white.withOpacity(0.4);

    final defaultBorder = Border.all(
      color: isDark
          ? Colors.white.withOpacity(0.08)
          : Colors.black.withOpacity(0.06),
      width: 1.0,
    );

    return ClipRRect(
      borderRadius: BorderRadius.circular(borderRadius),
      child: BackdropFilter(
        filter: ImageFilter.blur(sigmaX: blur, sigmaY: blur),
        child: Container(
          padding: padding,
          decoration: BoxDecoration(
            color: color ?? defaultColor,
            borderRadius: BorderRadius.circular(borderRadius),
            border: border ?? defaultBorder,
            boxShadow: [
              BoxShadow(
                color: Colors.black.withOpacity(0.05),
                blurRadius: 20,
                offset: const Offset(0, 10),
              )
            ],
          ),
          child: child,
        ),
      ),
    );
  }
}
