import 'dart:async';
import 'dart:math' as math;
import 'package:flutter/material.dart';

class MicAnimation extends StatefulWidget {
  final bool isRecording;
  final String style; // 'pulse', 'doraemon', 'fan', 'tom', 'emoji'
  final Widget child;

  const MicAnimation({
    Key? key,
    required this.isRecording,
    required this.style,
    required this.child,
  }) : super(key: key);

  @override
  State<MicAnimation> createState() => _MicAnimationState();
}

class _MicAnimationState extends State<MicAnimation> with TickerProviderStateMixin {
  late AnimationController _pulseController;
  late AnimationController _rotateController;
  
  // Interactive Tom States
  bool _isTomSlapped = false;
  bool _isTomDizzy = false;
  double _tomRotation = 0.0;
  Offset _tomOffset = Offset.zero;
  
  // Emoji cycling
  Timer? _emojiTimer;
  int _emojiIndex = 0;

  @override
  void initState() {
    super.initState();
    
    _pulseController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 900),
    );
    
    _rotateController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 350),
    );

    if (widget.isRecording) {
      _startAnimations();
    }
  }

  @override
  void didUpdateWidget(covariant MicAnimation oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (widget.isRecording != oldWidget.isRecording) {
      if (widget.isRecording) {
        _startAnimations();
      } else {
        _stopAnimations();
      }
    }
  }

  void _startAnimations() {
    _pulseController.repeat(reverse: true);
    _rotateController.repeat();
    
    if (widget.style == 'emoji') {
      _emojiIndex = 0;
      _emojiTimer?.cancel();
      _emojiTimer = Timer.periodic(const Duration(milliseconds: 180), (timer) {
        setState(() {
          _emojiIndex = (_emojiIndex + 1) % 6; // 6 expressions
        });
      });
    }
  }

  void _stopAnimations() {
    _pulseController.stop();
    _pulseController.reset();
    _rotateController.stop();
    _rotateController.reset();
    _emojiTimer?.cancel();
    _emojiTimer = null;
  }

  @override
  void dispose() {
    _pulseController.dispose();
    _rotateController.dispose();
    _emojiTimer?.cancel();
    super.dispose();
  }

  // Talking Tom slap interactions
  void _handleTomTap(TapUpDetails details, Size size) {
    if (_isTomDizzy) return; // Dizzy animation lock

    final localY = details.localPosition.dy;
    final relativeY = localY / size.height;

    if (relativeY < 0.35) {
      // Forehead Tap -> Dizzy Spin Head Roll
      _triggerTomDizzy();
    } else {
      // Cheek/Face Tap -> Slap Wobble
      _triggerTomSlap();
    }
  }

  void _triggerTomSlap() {
    setState(() {
      _isTomSlapped = true;
      _tomRotation = -0.25; // Tilt face
      _tomOffset = const Offset(-6, 2);
    });

    Future.delayed(const Duration(milliseconds: 150), () {
      if (mounted) {
        setState(() {
          _isTomSlapped = false;
          _tomRotation = 0.0;
          _tomOffset = Offset.zero;
        });
      }
    });
  }

  void _triggerTomDizzy() {
    setState(() {
      _isTomDizzy = true;
    });

    // Animate head roll spin
    AnimationController spinner = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1100),
    );
    spinner.addListener(() {
      if (mounted) {
        setState(() {
          _tomRotation = spinner.value * 2 * math.pi;
        });
      }
    });
    spinner.forward().then((_) {
      if (mounted) {
        setState(() {
          _isTomDizzy = false;
          _tomRotation = 0.0;
        });
      }
      spinner.dispose();
    });
  }

  @override
  Widget build(BuildContext context) {
    if (!widget.isRecording && widget.style != 'doraemon' && widget.style != 'fan' && widget.style != 'tom' && widget.style != 'emoji') {
      return Center(child: widget.child);
    }

    switch (widget.style.toLowerCase()) {
      case 'doraemon':
        return _buildDoraemonStyle();
      case 'fan':
        return _buildFanStyle();
      case 'tom':
        return _buildTomStyle();
      case 'emoji':
        return _buildEmojiStyle();
      case 'pulse':
      default:
        return _buildPulseStyle();
    }
  }

  Widget _buildPulseStyle() {
    return AnimatedBuilder(
      animation: _pulseController,
      builder: (context, child) {
        final val = _pulseController.value;
        return Stack(
          alignment: Alignment.center,
          children: [
            Container(
              width: 90 + (50 * val),
              height: 90 + (50 * val),
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: Theme.of(context).primaryColor.withOpacity(0.4 * (1.0 - val)),
              ),
            ),
            widget.child,
          ],
        );
      },
    );
  }

  Widget _buildDoraemonStyle() {
    return AnimatedBuilder(
      animation: _pulseController,
      builder: (context, child) {
        final double scale = widget.isRecording 
            ? 0.9 + (0.35 * _pulseController.value) 
            : 1.0;
        return Transform.scale(
          scale: scale,
          child: SizedBox(
            width: 95,
            height: 95,
            child: CustomPaint(
              painter: DoraemonFacePainter(),
            ),
          ),
        );
      },
    );
  }

  Widget _buildFanStyle() {
    return AnimatedBuilder(
      animation: _rotateController,
      builder: (context, child) {
        final double angle = widget.isRecording 
            ? _rotateController.value * 2 * math.pi 
            : 0.0;
        return SizedBox(
          width: 95,
          height: 95,
          child: CustomPaint(
            painter: RotatingFanPainter(angle: angle),
          ),
        );
      },
    );
  }

  Widget _buildTomStyle() {
    const size = Size(100, 100);
    return GestureDetector(
      onTapUp: (details) => _handleTomTap(details, size),
      child: Transform.translate(
        offset: _tomOffset,
        child: Transform.rotate(
          angle: _tomRotation,
          child: SizedBox(
            width: size.width,
            height: size.height,
            child: CustomPaint(
              painter: TomFacePainter(
                isSlapped: _isTomSlapped,
                isDizzy: _isTomDizzy,
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildEmojiStyle() {
    return SizedBox(
      width: 95,
      height: 95,
      child: CustomPaint(
        painter: EmojiFacePainter(
          expressionIndex: widget.isRecording ? _emojiIndex : 0,
        ),
      ),
    );
  }
}

class DoraemonFacePainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final radius = size.width / 2;

    final paintBlue = Paint()..color = const Color(0xFF3B82F6)..style = PaintingStyle.fill;
    final paintWhite = Paint()..color = Colors.white..style = PaintingStyle.fill;
    final paintRed = Paint()..color = const Color(0xFFEF4444)..style = PaintingStyle.fill;
    final paintBlack = Paint()..color = const Color(0xFF0F172A)..style = PaintingStyle.fill;
    
    final paintStroke = Paint()
      ..color = const Color(0xFF0F172A)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2.0;

    canvas.drawCircle(center, radius - 2, paintBlue);
    canvas.drawCircle(center, radius - 2, paintStroke);

    final faceCenter = Offset(center.dx, center.dy + 6);
    canvas.drawCircle(faceCenter, radius * 0.76, paintWhite);
    canvas.drawCircle(faceCenter, radius * 0.76, paintStroke);

    final eyeLeftCenter = Offset(center.dx - 7, center.dy - 14);
    final eyeRightCenter = Offset(center.dx + 7, center.dy - 14);
    final eyeSize = Size(14, 18);

    canvas.drawOval(Rect.fromCenter(center: eyeLeftCenter, width: eyeSize.width, height: eyeSize.height), paintWhite);
    canvas.drawOval(Rect.fromCenter(center: eyeLeftCenter, width: eyeSize.width, height: eyeSize.height), paintStroke);
    
    canvas.drawOval(Rect.fromCenter(center: eyeRightCenter, width: eyeSize.width, height: eyeSize.height), paintWhite);
    canvas.drawOval(Rect.fromCenter(center: eyeRightCenter, width: eyeSize.width, height: eyeSize.height), paintStroke);

    canvas.drawCircle(Offset(eyeLeftCenter.dx + 2, eyeLeftCenter.dy + 1), 2.5, paintBlack);
    canvas.drawCircle(Offset(eyeRightCenter.dx - 2, eyeRightCenter.dy + 1), 2.5, paintBlack);

    final noseCenter = Offset(center.dx, center.dy - 5);
    canvas.drawCircle(noseCenter, 5.5, paintRed);
    canvas.drawCircle(noseCenter, 5.5, paintStroke);
    canvas.drawCircle(Offset(noseCenter.dx - 1.8, noseCenter.dy - 1.8), 1.5, Paint()..color = Colors.white);

    canvas.drawLine(Offset(center.dx, noseCenter.dy + 5.5), Offset(center.dx, center.dy + 21), paintStroke);
    
    final smilePath = Path()
      ..moveTo(center.dx - 22, center.dy + 11)
      ..quadraticBezierTo(center.dx, center.dy + 28, center.dx + 22, center.dy + 11);
    canvas.drawPath(smilePath, paintStroke);

    canvas.drawLine(Offset(center.dx - 24, center.dy - 4), Offset(center.dx - 11, center.dy - 6), paintStroke);
    canvas.drawLine(Offset(center.dx - 26, center.dy + 2), Offset(center.dx - 13, center.dy + 2), paintStroke);
    canvas.drawLine(Offset(center.dx - 24, center.dy + 8), Offset(center.dx - 11, center.dy + 10), paintStroke);
    
    canvas.drawLine(Offset(center.dx + 11, center.dy - 6), Offset(center.dx + 24, center.dy - 4), paintStroke);
    canvas.drawLine(Offset(center.dx + 13, center.dy + 2), Offset(center.dx + 26, center.dy + 2), paintStroke);
    canvas.drawLine(Offset(center.dx + 11, center.dy + 10), Offset(center.dx + 24, center.dy + 8), paintStroke);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}

class RotatingFanPainter extends CustomPainter {
  final double angle;

  RotatingFanPainter({required this.angle});

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final radius = size.width / 2;

    final paintOuterBorder = Paint()
      ..color = Colors.grey.withOpacity(0.3)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 3.0;

    final paintBlade = Paint()
      ..color = const Color(0xFF14B8A6)
      ..style = PaintingStyle.fill;
      
    final paintBladeOutline = Paint()
      ..color = const Color(0xFF0D9488)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 1.5;

    final paintCenterPin = Paint()..color = Colors.grey[600]!..style = PaintingStyle.fill;
    final paintCenterPinCap = Paint()..color = Colors.white..style = PaintingStyle.stroke..strokeWidth = 1.0;

    canvas.drawCircle(center, radius - 4, paintOuterBorder);

    canvas.save();
    canvas.translate(center.dx, center.dy);
    canvas.rotate(angle);

    for (int i = 0; i < 4; i++) {
      canvas.save();
      canvas.rotate(i * math.pi / 2);
      
      final bladePath = Path()
        ..moveTo(0, 0)
        ..quadraticBezierTo(-12, -25, 0, -40)
        ..quadraticBezierTo(12, -25, 0, 0);
        
      canvas.drawPath(bladePath, paintBlade);
      canvas.drawPath(bladePath, paintBladeOutline);
      
      canvas.restore();
    }

    canvas.drawCircle(Offset.zero, 7.0, paintCenterPin);
    canvas.drawCircle(Offset.zero, 7.0, paintCenterPinCap);

    canvas.restore();
  }

  @override
  bool shouldRepaint(covariant RotatingFanPainter oldDelegate) {
    return oldDelegate.angle != angle;
  }
}

class TomFacePainter extends CustomPainter {
  final bool isSlapped;
  final bool isDizzy;

  TomFacePainter({required this.isSlapped, required this.isDizzy});

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final radius = size.width / 2;

    final paintGrey = Paint()..color = const Color(0xFF6B7280)..style = PaintingStyle.fill;
    final paintDarkGrey = Paint()..color = const Color(0xFF4B5563)..style = PaintingStyle.fill;
    final paintWhite = Paint()..color = Colors.white..style = PaintingStyle.fill;
    final paintMuzzle = Paint()..color = const Color(0xFFE5E7EB)..style = PaintingStyle.fill;
    final paintPink = Paint()..color = const Color(0xFFF472B6)..style = PaintingStyle.fill;
    final paintBlack = Paint()..color = const Color(0xFF0F172A)..style = PaintingStyle.fill;
    final paintGreen = Paint()..color = const Color(0xFF10B981)..style = PaintingStyle.fill;
    final paintRed = Paint()..color = const Color(0xFFEF4444)..style = PaintingStyle.fill;

    final paintStroke = Paint()
      ..color = const Color(0xFF1F2937)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2.0;

    // 1. Dizzy stars above head
    if (isDizzy) {
      final starPaint = Paint()..color = const Color(0xFFFACC15)..style = PaintingStyle.fill;
      canvas.drawCircle(Offset(center.dx - 22, center.dy - 46), 3, starPaint);
      canvas.drawCircle(Offset(center.dx + 22, center.dy - 46), 3, starPaint);
    }

    // 2. Ears
    final leftEarPath = Path()
      ..moveTo(center.dx - 32, center.dy - 22)
      ..lineTo(center.dx - 45, center.dy - 44)
      ..quadraticBezierTo(center.dx - 35, center.dy - 48, center.dx - 22, center.dy - 32);
    canvas.drawPath(leftEarPath, paintDarkGrey);
    canvas.drawPath(leftEarPath, paintStroke);
    
    final leftEarPink = Path()
      ..moveTo(center.dx - 30, center.dy - 24)
      ..lineTo(center.dx - 40, center.dy - 38)
      ..quadraticBezierTo(center.dx - 34, center.dy - 40, center.dx - 25, center.dy - 30);
    canvas.drawPath(leftEarPink, paintPink);

    final rightEarPath = Path()
      ..moveTo(center.dx + 32, center.dy - 22)
      ..lineTo(center.dx + 45, center.dy - 44)
      ..quadraticBezierTo(center.dx + 35, center.dy - 48, center.dx + 22, center.dy - 32);
    canvas.drawPath(rightEarPath, paintDarkGrey);
    canvas.drawPath(rightEarPath, paintStroke);

    final rightEarPink = Path()
      ..moveTo(center.dx + 30, center.dy - 24)
      ..lineTo(center.dx + 40, center.dy - 38)
      ..quadraticBezierTo(center.dx + 34, center.dy - 40, center.dx + 25, center.dy - 30);
    canvas.drawPath(rightEarPink, paintPink);

    // 3. Grey Head casing shape
    final headPath = Path()
      ..moveTo(center.dx - 35, center.dy - 20)
      ..quadraticBezierTo(center.dx, center.dy - 35, center.dx + 35, center.dy - 20)
      ..quadraticBezierTo(center.dx + 40, center.dy + 10, center.dx, center.dy + 40)
      ..quadraticBezierTo(center.dx - 40, center.dy + 10, center.dx - 35, center.dy - 20);
    canvas.drawPath(headPath, paintGrey);
    canvas.drawPath(headPath, paintStroke);

    // 4. Eyes
    final eyeLeftRect = Rect.fromCenter(center: Offset(center.dx - 12, center.dy - 10), width: 16, height: 22);
    final eyeRightRect = Rect.fromCenter(center: Offset(center.dx + 12, center.dy - 10), width: 16, height: 22);
    
    if (isDizzy) {
      // Spiral dizzy eyes
      final dizzyEyePaint = Paint()..color = const Color(0xFF1F2937)..style = PaintingStyle.stroke..strokeWidth = 2.0;
      canvas.drawOval(eyeLeftRect, paintWhite);
      canvas.drawOval(eyeLeftRect, paintStroke);
      canvas.drawArc(eyeLeftRect.deflate(4), 0, 4.5, false, dizzyEyePaint);
      
      canvas.drawOval(eyeRightRect, paintWhite);
      canvas.drawOval(eyeRightRect, paintStroke);
      canvas.drawArc(eyeRightRect.deflate(4), 3.14, 4.5, false, dizzyEyePaint);
    } else {
      // Normal green eyes
      canvas.drawOval(eyeLeftRect, paintWhite);
      canvas.drawOval(eyeLeftRect, paintStroke);
      canvas.drawCircle(Offset(center.dx - 12, center.dy - 10), 4.5, paintGreen);
      canvas.drawCircle(Offset(center.dx - 12, center.dy - 10), 2.0, paintBlack);

      canvas.drawOval(eyeRightRect, paintWhite);
      canvas.drawOval(eyeRightRect, paintStroke);
      canvas.drawCircle(Offset(center.dx + 12, center.dy - 10), 4.5, paintGreen);
      canvas.drawCircle(Offset(center.dx + 12, center.dy - 10), 2.0, paintBlack);
    }

    // 5. White Muzzle Cheeks
    canvas.drawCircle(Offset(center.dx - 7, center.dy + 8), 8.0, paintMuzzle);
    canvas.drawCircle(Offset(center.dx - 7, center.dy + 8), 8.0, paintStroke);
    canvas.drawCircle(Offset(center.dx + 7, center.dy + 8), 8.0, paintMuzzle);
    canvas.drawCircle(Offset(center.dx + 7, center.dy + 8), 8.0, paintStroke);

    // 6. Pink Nose
    final nosePath = Path()
      ..moveTo(center.dx - 4, center.dy)
      ..lineTo(center.dx + 4, center.dy)
      ..lineTo(center.dx, center.dy + 5)
      ..close();
    canvas.drawPath(nosePath, paintPink);
    canvas.drawPath(nosePath, paintStroke);

    // 7. Mouth
    if (isDizzy) {
      canvas.drawCircle(Offset(center.dx, center.dy + 15), 4.5, paintRed);
      canvas.drawCircle(Offset(center.dx, center.dy + 15), 4.5, paintStroke);
    } else {
      final mouthPath = Path()
        ..moveTo(center.dx - 12, center.dy + 12)
        ..quadraticBezierTo(center.dx, center.dy + 21, center.dx + 12, center.dy + 12);
      canvas.drawPath(mouthPath, paintStroke);
    }

    // 8. Whiskers lines
    canvas.drawLine(Offset(center.dx - 22, center.dy + 6), Offset(center.dx - 42, center.dy + 2), paintStroke);
    canvas.drawLine(Offset(center.dx - 24, center.dy + 12), Offset(center.dx - 44, center.dy + 12), paintStroke);
    canvas.drawLine(Offset(center.dx + 22, center.dy + 6), Offset(center.dx + 42, center.dy + 2), paintStroke);
    canvas.drawLine(Offset(center.dx + 24, center.dy + 12), Offset(center.dx + 44, center.dy + 12), paintStroke);

    // 9. Draw Slap impact star flash
    if (isSlapped) {
      final starPaint = Paint()..color = const Color(0xFFFACC15)..style = PaintingStyle.fill;
      final starPath = Path()
        ..moveTo(center.dx, center.dy - 15)
        ..lineTo(center.dx + 4, center.dy - 2)
        ..lineTo(center.dx + 17, center.dy - 8)
        ..lineTo(center.dx + 8, center.dy + 2)
        ..lineTo(center.dx + 18, center.dy + 12)
        ..lineTo(center.dx + 4, center.dy + 11)
        ..lineTo(center.dx, center.dy + 22)
        ..lineTo(center.dx - 4, center.dy + 11)
        ..lineTo(center.dx - 18, center.dy + 12)
        ..lineTo(center.dx - 8, center.dy + 2)
        ..lineTo(center.dx - 17, center.dy - 8)
        ..lineTo(center.dx - 4, center.dy - 2)
        ..close();
      canvas.drawPath(starPath, starPaint);
      canvas.drawPath(starPath, paintStroke);
    }
  }

  @override
  bool shouldRepaint(covariant TomFacePainter oldDelegate) {
    return oldDelegate.isSlapped != isSlapped || oldDelegate.isDizzy != isDizzy;
  }
}

class EmojiFacePainter extends CustomPainter {
  final int expressionIndex;

  EmojiFacePainter({required this.expressionIndex});

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final radius = size.width / 2;

    final paintFace = Paint()..color = const Color(0xFFFBBF24)..style = PaintingStyle.fill;
    final paintOutline = Paint()..color = const Color(0xFFD97706)..style = PaintingStyle.stroke..strokeWidth = 2.5;
    final paintBlack = Paint()..color = Colors.black..style = PaintingStyle.fill;
    final paintBlackStroke = Paint()..color = Colors.black..style = PaintingStyle.stroke..strokeWidth = 3.5..strokeCap = StrokeCap.round;

    // Draw yellow face base
    canvas.drawCircle(center, radius - 2, paintFace);
    canvas.drawCircle(center, radius - 2, paintOutline);

    // Expressions map: 0: Happy, 1: Surprised, 2: Angry, 3: Laughing, 4: Cool, 5: Dizzy
    switch (expressionIndex) {
      case 1: // Surprised
        canvas.drawCircle(Offset(center.dx - 14, center.dy - 10), 6.5, paintBlack);
        canvas.drawCircle(Offset(center.dx + 14, center.dy - 10), 6.5, paintBlack);
        canvas.drawCircle(Offset(center.dx, center.dy + 14), 7.5, paintBlack);
        break;
      case 2: // Angry
        // Eyebrows
        canvas.drawLine(Offset(center.dx - 22, center.dy - 15), Offset(center.dx - 8, center.dy - 9), paintBlackStroke);
        canvas.drawLine(Offset(center.dx + 22, center.dy - 15), Offset(center.dx + 8, center.dy - 9), paintBlackStroke);
        canvas.drawCircle(Offset(center.dx - 14, center.dy - 5), 4.5, paintBlack);
        canvas.drawCircle(Offset(center.dx + 14, center.dy - 5), 4.5, paintBlack);
        // Angled mouth
        final mouthPath = Path()
          ..moveTo(center.dx - 14, center.dy + 16)
          ..quadraticBezierTo(center.dx, center.dy + 6, center.dx + 14, center.dy + 16);
        canvas.drawPath(mouthPath, paintBlackStroke);
        break;
      case 3: // Laughing
        // Squint eyes
        final eyeL = Path()..moveTo(center.dx - 22, center.dy - 8)..quadraticBezierTo(center.dx - 14, center.dy - 14, center.dx - 6, center.dy - 8);
        final eyeR = Path()..moveTo(center.dx + 6, center.dy - 8)..quadraticBezierTo(center.dx + 14, center.dy - 14, center.dx + 22, center.dy - 8);
        canvas.drawPath(eyeL, paintBlackStroke);
        canvas.drawPath(eyeR, paintBlackStroke);
        // Open laugh mouth
        final mouthPath = Path()
          ..moveTo(center.dx - 18, center.dy + 8)
          ..quadraticBezierTo(center.dx, center.dy + 32, center.dx + 18, center.dy + 8)
          ..close();
        canvas.drawPath(mouthPath, paintBlack);
        break;
      case 4: // Cool (Sunglasses)
        final leftGlass = Rect.fromCenter(center: Offset(center.dx - 15, center.dy - 12), width: 20, height: 10);
        final rightGlass = Rect.fromCenter(center: Offset(center.dx + 15, center.dy - 12), width: 20, height: 10);
        canvas.drawRect(leftGlass, paintBlack);
        canvas.drawRect(rightGlass, paintBlack);
        canvas.drawLine(Offset(center.dx - 5, center.dy - 12), Offset(center.dx + 5, center.dy - 12), paintBlackStroke);
        // Smirk mouth
        final mouthPath = Path()
          ..moveTo(center.dx - 14, center.dy + 12)
          ..quadraticBezierTo(center.dx - 2, center.dy + 18, center.dx + 14, center.dy + 8);
        canvas.drawPath(mouthPath, paintBlackStroke);
        break;
      case 5: // Dizzy (X eyes)
        // X Left
        canvas.drawLine(Offset(center.dx - 19, center.dy - 15), Offset(center.dx - 9, center.dy - 5), paintBlackStroke);
        canvas.drawLine(Offset(center.dx - 9, center.dy - 15), Offset(center.dx - 19, center.dy - 5), paintBlackStroke);
        // X Right
        canvas.drawLine(Offset(center.dx + 9, center.dy - 15), Offset(center.dx + 19, center.dy - 5), paintBlackStroke);
        canvas.drawLine(Offset(center.dx + 19, center.dy - 15), Offset(center.dx + 9, center.dy - 5), paintBlackStroke);
        // Wave mouth
        final mouthPath = Path()
          ..moveTo(center.dx - 14, center.dy + 14)
          ..quadraticBezierTo(center.dx - 7, center.dy + 18, center.dx, center.dy + 12)
          ..quadraticBezierTo(center.dx + 7, center.dy + 6, center.dx + 14, center.dy + 14);
        canvas.drawPath(mouthPath, paintBlackStroke);
        break;
      case 0: // Happy (Default)
      default:
        canvas.drawCircle(Offset(center.dx - 14, center.dy - 10), 5.0, paintBlack);
        canvas.drawCircle(Offset(center.dx + 14, center.dy - 10), 5.0, paintBlack);
        final mouthPath = Path()
          ..moveTo(center.dx - 18, center.dy + 10)
          ..quadraticBezierTo(center.dx, center.dy + 28, center.dx + 18, center.dy + 10);
        canvas.drawPath(mouthPath, paintBlackStroke);
        break;
    }
  }

  @override
  bool shouldRepaint(covariant EmojiFacePainter oldDelegate) {
    return oldDelegate.expressionIndex != expressionIndex;
  }
}
