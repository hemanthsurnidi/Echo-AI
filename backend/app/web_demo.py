HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Echo AI – Communication Intelligence Platform</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        :root {
            --bg-primary: #0a0b10;
            --bg-secondary: rgba(20, 22, 37, 0.6);
            --border-color: rgba(255, 255, 255, 0.08);
            --text-primary: #f3f4f6;
            --text-secondary: #9ca3af;
            --primary: #8b5cf6;
            --primary-glow: rgba(139, 92, 246, 0.35);
            --secondary: #14b8a6;
            --secondary-glow: rgba(20, 184, 166, 0.35);
            --accent: #ec4899;
            --card-bg: rgba(15, 17, 33, 0.7);
            --card-blur: 16px;
            --font-family: 'Plus Jakarta Sans', sans-serif;
            --heading-family: 'Outfit', sans-serif;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
        }

        [data-theme="light"] {
            --bg-primary: #f8fafc;
            --bg-secondary: rgba(241, 245, 249, 0.7);
            --border-color: rgba(15, 23, 42, 0.08);
            --text-primary: #0f172a;
            --text-secondary: #475569;
            --primary: #7c3aed;
            --primary-glow: rgba(124, 58, 237, 0.15);
            --secondary: #0d9488;
            --secondary-glow: rgba(13, 148, 136, 0.15);
            --accent: #db2777;
            --card-bg: rgba(255, 255, 255, 0.75);
            --success: #059669;
            --warning: #d97706;
            --danger: #dc2626;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            transition: background-color 0.3s, border-color 0.3s, color 0.3s;
        }

        body {
            background-color: var(--bg-primary);
            color: var(--text-primary);
            font-family: var(--font-family);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(139, 92, 246, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(20, 184, 166, 0.08) 0%, transparent 40%);
            background-attachment: fixed;
        }

        /* Glassmorphism Card Style */
        .glass-card {
            background: var(--card-bg);
            backdrop-filter: blur(var(--card-blur));
            -webkit-backdrop-filter: blur(var(--card-blur));
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 24px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
        }

        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 5%;
            border-bottom: 1px solid var(--border-color);
            background: rgba(10, 11, 16, 0.3);
            backdrop-filter: blur(10px);
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .logo-container {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .logo-icon {
            width: 42px;
            height: 42px;
            border-radius: 12px;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 20px;
            box-shadow: 0 4px 15px var(--primary-glow);
        }

        .logo-text h1 {
            font-family: var(--heading-family);
            font-size: 22px;
            font-weight: 800;
            background: linear-gradient(to right, var(--text-primary), var(--primary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .logo-text p {
            font-size: 11px;
            color: var(--text-secondary);
            font-weight: 500;
            letter-spacing: 1px;
            text-transform: uppercase;
        }

        .theme-toggle {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            width: 44px;
            height: 44px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--text-primary);
            cursor: pointer;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }

        .theme-toggle:hover {
            transform: scale(1.05);
        }

        main {
            flex: 1;
            padding: 40px 5%;
            max-width: 1400px;
            width: 100%;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 1.2fr 1.8fr;
            gap: 32px;
        }

        @media (max-width: 1024px) {
            main {
                grid-template-columns: 1fr;
            }
        }

        .workspace-panel {
            display: flex;
            flex-direction: column;
            gap: 24px;
            height: fit-content;
        }

        .mode-selector {
            display: grid;
            grid-template-columns: 1fr 1fr;
            background: var(--bg-secondary);
            border-radius: 14px;
            padding: 4px;
            border: 1px solid var(--border-color);
        }

        .mode-btn {
            background: transparent;
            border: none;
            color: var(--text-secondary);
            font-family: var(--font-family);
            font-weight: 600;
            padding: 12px;
            border-radius: 10px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            font-size: 14px;
        }

        .mode-btn.active {
            background: var(--primary);
            color: white;
            box-shadow: 0 4px 15px var(--primary-glow);
        }

        .recording-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 40px 20px;
            position: relative;
            min-height: 320px;
        }

        .timer-display {
            font-family: var(--heading-family);
            font-size: 42px;
            font-weight: 700;
            margin-bottom: 24px;
            letter-spacing: 1px;
            background: linear-gradient(135deg, var(--text-primary), var(--text-secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .mic-wrapper {
            position: relative;
            width: 150px;
            height: 150px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 24px;
            border-radius: 50%;
            cursor: pointer;
        }

        .mic-button {
            width: 110px;
            height: 110px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border: none;
            color: white;
            font-size: 36px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            box-shadow: 0 10px 30px var(--primary-glow);
            z-index: 10;
            user-select: none;
            -webkit-user-select: none;
            overflow: visible;
            position: relative;
        }

        .recording-status-text {
            font-size: 14px;
            color: var(--text-secondary);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 12px;
            height: 20px;
        }

        /* 1. Pulse Animation */
        .animation-pulse {
            position: absolute;
            width: 100%;
            height: 100%;
            border-radius: 50%;
            background: var(--primary);
            opacity: 0;
            transform: scale(0.8);
            z-index: 1;
            pointer-events: none;
        }
        .recording .animation-pulse {
            animation: pulse-ring 1.8s cubic-bezier(0.215, 0.61, 0.355, 1) infinite;
        }
        @keyframes pulse-ring {
            0% { transform: scale(0.7); opacity: 0.5; }
            100% { transform: scale(1.4); opacity: 0; }
        }

        /* 2. Doraemon Scaling Animation */
        .doraemon-wrapper {
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .doraemon-face {
            width: 90px;
            height: 90px;
            transform-origin: center;
        }
        .recording .doraemon-face {
            animation: doraemon-bounce 0.8s ease-in-out infinite alternate;
        }
        @keyframes doraemon-bounce {
            0% { transform: scale(0.88); }
            100% { transform: scale(1.22); }
        }

        /* 3. Rotating Fan Animation */
        .fan-wrapper {
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .fan-blade {
            width: 82px;
            height: 82px;
            transform-origin: center;
        }
        .recording .fan-blade {
            animation: spin-fan-blades 0.35s linear infinite;
        }
        @keyframes spin-fan-blades {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        /* 4. Talking Tom SVG Face slaps and spins */
        .tom-wrapper {
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
        }
        .tom-face-svg {
            width: 95px;
            height: 95px;
            transform-origin: center;
            transition: transform 0.1s ease;
        }
        
        /* Tom Slap wiggle animation */
        .tom-face-svg.slapped {
            animation: tom-slap-shake 0.15s ease-out;
        }
        @keyframes tom-slap-shake {
            0% { transform: rotate(0deg) scale(1); }
            25% { transform: rotate(-16deg) scale(0.92) translate(-8px, 2px); }
            75% { transform: rotate(12deg) scale(1.05) translate(4px, -1px); }
            100% { transform: rotate(0deg) scale(1); }
        }

        /* Tom Dizzy head-roll spin */
        .tom-face-svg.dizzy {
            animation: tom-head-roll 1.1s cubic-bezier(0.4, 0, 0.2, 1);
        }
        @keyframes tom-head-roll {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        /* Talking Tom rapid shake inside/outside during recording */
        .recording .tom-face-svg {
            animation: tom-hold-shake 0.22s linear infinite;
        }
        @keyframes tom-hold-shake {
            0% { transform: scale(1.0) translate(0, 0) rotate(0deg); }
            20% { transform: scale(0.88) translate(-4px, 2px) rotate(-3deg); }
            40% { transform: scale(1.18) translate(3px, -3px) rotate(4deg); }
            60% { transform: scale(0.86) translate(-2px, 3px) rotate(-4deg); }
            80% { transform: scale(1.14) translate(4px, 1px) rotate(3deg); }
            100% { transform: scale(1.0) translate(0, 0) rotate(0deg); }
        }

        /* 5. Emoji Expressions cycling */
        .emoji-wrapper {
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .emoji-face-svg {
            width: 95px;
            height: 95px;
            transform-origin: center;
        }

        /* Style Selectors UI */
        .style-selector {
            width: 100%;
            margin-top: 15px;
        }
        .style-selector label {
            font-size: 12px;
            font-weight: 700;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
            display: block;
        }
        .style-grid {
            display: flex;
            gap: 8px;
            overflow-x: auto;
            padding-bottom: 8px;
        }
        .style-item {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            padding: 8px 12px;
            border-radius: 8px;
            font-size: 12px;
            color: var(--text-secondary);
            cursor: pointer;
            white-space: nowrap;
            font-weight: 600;
        }
        .style-item.active {
            background: var(--secondary-glow);
            color: var(--secondary);
            border-color: var(--secondary);
        }

        /* Control Buttons */
        .recorder-controls {
            display: flex;
            gap: 16px;
            margin-top: 10px;
        }
        .btn-control {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            font-family: var(--font-family);
            font-weight: 600;
            padding: 12px 24px;
            border-radius: 12px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .btn-control:hover {
            background: var(--border-color);
        }
        .btn-control:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        .btn-control.active-record {
            background: var(--danger);
            color: white;
            border-color: var(--danger);
        }

        /* Voice Effects Styling */
        .effects-panel {
            margin-top: 8px;
        }
        .effects-panel h3 {
            font-family: var(--heading-family);
            font-size: 16px;
            margin-bottom: 12px;
            font-weight: 700;
        }
        .effects-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
        }
        .effect-card {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 12px;
            text-align: center;
            cursor: pointer;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 6px;
        }
        .effect-card i {
            font-size: 18px;
            color: var(--text-secondary);
        }
        .effect-card span {
            font-size: 11px;
            font-weight: 600;
            color: var(--text-secondary);
        }
        .effect-card.active {
            border-color: var(--primary);
            background: var(--primary-glow);
        }
        .effect-card.active i {
            color: var(--primary);
        }
        .effect-card.active span {
            color: var(--text-primary);
        }

        /* Right Column: Analytics & Details */
        .analytics-panel {
            display: flex;
            flex-direction: column;
            gap: 24px;
        }

        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 16px;
        }
        @media (max-width: 640px) {
            .dashboard-grid {
                grid-template-columns: 1fr;
            }
        }

        .stat-card {
            display: flex;
            align-items: center;
            gap: 16px;
        }
        .stat-icon {
            width: 48px;
            height: 48px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
        }
        .stat-icon.purple { background: var(--primary-glow); color: var(--primary); }
        .stat-icon.teal { background: var(--secondary-glow); color: var(--secondary); }
        .stat-icon.pink { background: rgba(236, 72, 153, 0.15); color: var(--accent); }
        
        .stat-info h4 {
            font-size: 11px;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .stat-info p {
            font-family: var(--heading-family);
            font-size: 20px;
            font-weight: 700;
        }

        /* Main Session Display / Interactive Detail */
        .analysis-detail {
            min-height: 250px;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }

        .analysis-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 14px;
        }

        .analysis-title h3 {
            font-family: var(--heading-family);
            font-size: 20px;
            font-weight: 700;
        }
        .analysis-title p {
            font-size: 12px;
            color: var(--text-secondary);
            margin-top: 2px;
        }

        .score-pill {
            background: var(--secondary-glow);
            color: var(--secondary);
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .analysis-content {
            display: grid;
            grid-template-columns: 1.3fr 1fr;
            gap: 20px;
        }
        @media (max-width: 640px) {
            .analysis-content {
                grid-template-columns: 1fr;
            }
        }

        .transcript-box {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .transcript-box label {
            font-size: 11px;
            font-weight: 700;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .transcript-text {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 16px;
            font-size: 14px;
            line-height: 1.6;
            height: 160px;
            overflow-y: auto;
            color: var(--text-primary);
        }

        .metrics-breakdown {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        .metric-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 12px;
            background: var(--bg-secondary);
            border-radius: 10px;
            border: 1px solid var(--border-color);
        }
        .metric-label {
            font-size: 12px;
            color: var(--text-secondary);
            font-weight: 600;
        }
        .metric-value {
            font-size: 13px;
            font-weight: 700;
        }
        .metric-badge {
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 10px;
            font-weight: 800;
            text-transform: uppercase;
        }
        .badge-slow { background: rgba(239, 68, 68, 0.15); color: var(--danger); }
        .badge-normal { background: rgba(16, 185, 129, 0.15); color: var(--success); }
        .badge-fast { background: rgba(245, 158, 11, 0.15); color: var(--warning); }

        .tabs-header {
            display: flex;
            gap: 16px;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 16px;
        }
        .tab-link {
            font-family: var(--heading-family);
            font-size: 15px;
            font-weight: 600;
            color: var(--text-secondary);
            padding-bottom: 8px;
            cursor: pointer;
            border-bottom: 2px solid transparent;
        }
        .tab-link.active {
            color: var(--primary);
            border-bottom-color: var(--primary);
        }

        .tab-content {
            display: none;
        }
        .tab-content.active {
            display: block;
        }

        .history-list {
            max-height: 250px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .history-item {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            padding: 12px 16px;
            border-radius: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
        }
        .history-item:hover {
            border-color: var(--primary);
        }
        .history-meta h5 {
            font-size: 13px;
            font-weight: 700;
            margin-bottom: 2px;
        }
        .history-meta p {
            font-size: 11px;
            color: var(--text-secondary);
        }
        .history-score {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .hist-pill {
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 700;
        }
        .hist-pill.comm { background: rgba(20, 184, 166, 0.15); color: var(--secondary); }
        .btn-delete-hist {
            color: var(--text-secondary);
            background: transparent;
            border: none;
            cursor: pointer;
            padding: 4px;
        }
        .btn-delete-hist:hover {
            color: var(--danger);
        }

        .chart-container {
            width: 100%;
            height: 220px;
            position: relative;
        }
        .chart-svg {
            width: 100%;
            height: 100%;
        }

        .audio-player-card {
            display: flex;
            align-items: center;
            gap: 12px;
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            padding: 12px 16px;
            border-radius: 12px;
            margin-top: 10px;
        }
        .audio-player-card button {
            background: var(--primary);
            border: none;
            color: white;
            width: 38px;
            height: 38px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
        }
        .playback-progress {
            flex: 1;
            height: 4px;
            background: var(--border-color);
            border-radius: 2px;
            position: relative;
            cursor: pointer;
        }
        .progress-fill {
            height: 100%;
            width: 0%;
            background: var(--primary);
            border-radius: 2px;
        }
        .progress-time {
            font-size: 11px;
            color: var(--text-secondary);
            min-width: 32px;
        }

        footer {
            text-align: center;
            padding: 30px;
            font-size: 12px;
            color: var(--text-secondary);
            border-top: 1px solid var(--border-color);
            background: rgba(10, 11, 16, 0.1);
        }

        .toast {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: var(--primary);
            color: white;
            padding: 12px 24px;
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
            z-index: 1000;
            display: none;
            font-weight: 600;
            font-size: 14px;
            animation: slide-up-fade 0.3s ease;
        }
        @keyframes slide-up-fade {
            from { transform: translateY(20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
    </style>
</head>
<body>

    <header>
        <div class="logo-container">
            <div class="logo-icon">
                <i class="fa-solid fa-waveform-lines"></i>
            </div>
            <div class="logo-text">
                <h1>Echo AI</h1>
                <p>Speak. Listen. Improve.</p>
            </div>
        </div>
        
        <button class="theme-toggle" id="theme-toggle-btn">
            <i class="fa-solid fa-moon"></i>
        </button>
    </header>

    <main>
        <!-- Left Side: recorder and effect selection -->
        <div class="workspace-panel">
            <div class="glass-card">
                <div class="mode-selector">
                    <button class="mode-btn active" id="mode-echo">
                        <i class="fa-solid fa-repeat"></i> Echo Mode
                    </button>
                    <button class="mode-btn" id="mode-recorder">
                        <i class="fa-solid fa-microphone-lines"></i> Recorder
                    </button>
                </div>

                <div class="recording-container" id="record-container">
                    <div class="timer-display" id="duration-timer">00:00.0</div>
                    
                    <div class="recording-status-text" id="status-text">Ready to Record</div>

                    <div class="mic-wrapper" id="mic-wrapper-button">
                        <div class="animation-pulse" id="anim-pulse"></div>
                        
                        <button class="mic-button" id="mic-trigger">
                            <i class="fa-solid fa-microphone" id="traditional-mic-icon"></i>
                            
                            <!-- Doraemon custom SVG face -->
                            <div class="doraemon-wrapper" id="doraemon-face-wrapper" style="display: none;">
                                <svg class="doraemon-face" viewBox="0 0 100 100">
                                    <circle cx="50" cy="50" r="44" fill="#3b82f6" stroke="#0f172a" stroke-width="2.5"/>
                                    <circle cx="50" cy="56" r="34" fill="#ffffff" stroke="#0f172a" stroke-width="2"/>
                                    <ellipse cx="43" cy="36" rx="7" ry="9" fill="#ffffff" stroke="#0f172a" stroke-width="2"/>
                                    <ellipse cx="57" cy="36" rx="7" ry="9" fill="#ffffff" stroke="#0f172a" stroke-width="2"/>
                                    <circle cx="45" cy="37" r="2.5" fill="#000000"/>
                                    <circle cx="55" cy="37" r="2.5" fill="#000000"/>
                                    <circle cx="50" cy="45" r="5" fill="#ef4444" stroke="#0f172a" stroke-width="1.5"/>
                                    <circle cx="48" cy="43.5" r="1.5" fill="#ffffff"/>
                                    <path d="M 50 50 L 50 71" stroke="#0f172a" stroke-width="2"/>
                                    <path d="M 28 61 Q 50 78 72 61" fill="none" stroke="#0f172a" stroke-width="2.5"/>
                                    <line x1="26" y1="46" x2="13" y2="44" stroke="#0f172a" stroke-width="2"/>
                                    <line x1="24" y1="52" x2="11" y2="52" stroke="#0f172a" stroke-width="2"/>
                                    <line x1="26" y1="58" x2="13" y2="60" stroke="#0f172a" stroke-width="2"/>
                                    <line x1="74" y1="46" x2="87" y2="44" stroke="#0f172a" stroke-width="2"/>
                                    <line x1="76" y1="52" x2="89" y2="52" stroke="#0f172a" stroke-width="2"/>
                                    <line x1="74" y1="58" x2="87" y2="60" stroke="#0f172a" stroke-width="2"/>
                                </svg>
                            </div>

                            <!-- Rotating Fan custom SVG (Bright Light Yellow) -->
                            <div class="fan-wrapper" id="rotating-fan-wrapper" style="display: none;">
                                <svg class="fan-blade" viewBox="0 0 100 100">
                                    <circle cx="50" cy="50" r="42" fill="none" stroke="#fde047" stroke-width="3" stroke-dasharray="6,4" opacity="0.3"/>
                                    <g transform="translate(50, 50)">
                                        <g class="fan-blade-spin" id="fan-blade-group">
                                            <!-- Light Yellow Blades -->
                                            <path d="M 0 0 Q -12 -25 0 -40 Q 12 -25 0 0" fill="#fef08a" stroke="#ca8a04" stroke-width="1.5"/>
                                            <path d="M 0 0 Q 25 -12 40 0 Q 25 12 0 0" fill="#fef08a" stroke="#ca8a04" stroke-width="1.5"/>
                                            <path d="M 0 0 Q 12 25 0 40 Q -12 25 0 0" fill="#fef08a" stroke="#ca8a04" stroke-width="1.5"/>
                                            <path d="M 0 0 Q -25 12 -40 0 Q -25 -12 0 0" fill="#fef08a" stroke="#ca8a04" stroke-width="1.5"/>
                                            <circle cx="0" cy="0" r="7" fill="#4b5563" stroke="#fde047" stroke-width="1.5"/>
                                        </g>
                                    </g>
                                </svg>
                            </div>

                            <!-- Talking Tom Interactive Face -->
                            <div class="tom-wrapper" id="talking-tom-wrapper" style="display: none; width: 100%; height: 100%;">
                                <svg class="tom-face-svg" id="tom-face-svg" viewBox="0 0 100 100">
                                    <!-- Rotating dizziness stars -->
                                    <g id="tom-dizzy-stars" style="display: none;">
                                        <path d="M 20 8 Q 25 2 30 8" fill="none" stroke="#facc15" stroke-width="1.5" stroke-dasharray="2,2"/>
                                        <polygon points="20,8 22,5 24,8 21,9" fill="#facc15"/>
                                        <polygon points="76,8 78,5 80,8 77,9" fill="#facc15"/>
                                    </g>
                                    
                                    <!-- Main Head Structure -->
                                    <path d="M 15 30 Q 30 10 50 15 Q 70 10 85 30 Q 90 60 50 90 Q 10 60 15 30 Z" fill="#78716c" stroke="#1c1917" stroke-width="2.5"/>
                                    
                                    <!-- Left Ear -->
                                    <path d="M 18 28 L 5 10 Q 15 5 28 18 Z" fill="#57534e" stroke="#1c1917" stroke-width="2"/>
                                    <path d="M 15 20 L 8 13 Q 14 11 22 17 Z" fill="#fda4af" />
                                    
                                    <!-- Right Ear -->
                                    <path d="M 82 28 L 95 10 Q 85 5 72 18 Z" fill="#57534e" stroke="#1c1917" stroke-width="2"/>
                                    <path d="M 85 20 L 92 13 Q 86 11 78 17 Z" fill="#fda4af" />
                                    
                                    <!-- Eyes base -->
                                    <ellipse cx="38" cy="40" rx="8" ry="11" fill="#fff" stroke="#1c1917" stroke-width="2" id="tom-eye-l"/>
                                    <ellipse cx="62" cy="40" rx="8" ry="11" fill="#fff" stroke="#1c1917" stroke-width="2" id="tom-eye-r"/>
                                    
                                    <!-- Eyebrows (Detailed) -->
                                    <path d="M 27 26 Q 37 22 44 27" fill="none" stroke="#1c1917" stroke-width="3" stroke-linecap="round"/>
                                    <path d="M 73 26 Q 63 22 56 27" fill="none" stroke="#1c1917" stroke-width="3" stroke-linecap="round"/>
                                    
                                    <!-- Spirals dizzy eyes -->
                                    <path id="tom-eye-spiral-l" d="M 34 40 A 3 3 0 1 0 40 40 A 5 5 0 1 0 32 40" fill="none" stroke="#1c1917" stroke-width="2" style="display: none;"/>
                                    <path id="tom-eye-spiral-r" d="M 58 40 A 3 3 0 1 0 64 40 A 5 5 0 1 0 56 40" fill="none" stroke="#1c1917" stroke-width="2" style="display: none;"/>

                                    <!-- Green Pupils -->
                                    <circle cx="38" cy="40" r="4.5" fill="#10b981" id="tom-pupil-l"/>
                                    <circle cx="62" cy="40" r="4.5" fill="#10b981" id="tom-pupil-r"/>
                                    <circle cx="38" cy="40" r="2.0" fill="#000" id="tom-pupil-black-l"/>
                                    <circle cx="62" cy="40" r="2.0" fill="#000" id="tom-pupil-black-r"/>
                                    
                                    <!-- Muzzle cheeks white -->
                                    <circle cx="43" cy="58" r="8.5" fill="#f5f5f4" stroke="#1c1917" stroke-width="1.5"/>
                                    <circle cx="57" cy="58" r="8.5" fill="#f5f5f4" stroke="#1c1917" stroke-width="1.5"/>
                                    
                                    <!-- Muzzle spots -->
                                    <circle cx="41" cy="56" r="0.8" fill="#78716c"/>
                                    <circle cx="44" cy="59" r="0.8" fill="#78716c"/>
                                    <circle cx="59" cy="56" r="0.8" fill="#78716c"/>
                                    <circle cx="56" cy="59" r="0.8" fill="#78716c"/>

                                    <!-- Nose -->
                                    <polygon points="46,50 54,50 50,55" fill="#f43f5e" stroke="#1c1917" stroke-width="1.5"/>
                                    
                                    <!-- Mouth -->
                                    <path d="M 36 62 Q 50 72 64 62" fill="none" stroke="#1c1917" stroke-width="2.5" id="tom-mouth-smile"/>
                                    <circle cx="50" cy="65" r="4.5" fill="#e11d48" id="tom-mouth-dizzy" style="display: none;"/>
                                    
                                    <!-- Whiskers -->
                                    <line x1="28" y1="56" x2="8" y2="52" stroke="#1c1917" stroke-width="2.5"/>
                                    <line x1="26" y1="62" x2="6" y2="62" stroke="#1c1917" stroke-width="2.5"/>
                                    <line x1="72" y1="56" x2="92" y2="52" stroke="#1c1917" stroke-width="2.5"/>
                                    <line x1="74" y1="62" x2="94" y2="62" stroke="#1c1917" stroke-width="2.5"/>

                                    <!-- Slap impact star -->
                                    <g id="tom-impact-star" style="display: none;">
                                        <polygon points="50,15 54,28 67,22 58,32 68,42 54,41 50,52 46,41 32,42 42,32 33,22 46,28" fill="#facc15" stroke="#eab308" stroke-width="1.5"/>
                                    </g>
                                </svg>
                            </div>

                            <!-- Animated Emoji Expressions -->
                            <div class="emoji-wrapper" id="emoji-face-wrapper" style="display: none; width: 100%; height: 100%;">
                                <svg class="emoji-face-svg" viewBox="0 0 100 100">
                                    <circle cx="50" cy="50" r="44" fill="#fbbf24" stroke="#d97706" stroke-width="2.5"/>
                                    <!-- 3D Native Emoji rendering -->
                                    <text id="emoji-char" x="50" y="73" font-size="62" text-anchor="middle" font-family="Segoe UI Emoji, Noto Color Emoji, Apple Color Emoji, sans-serif">😃</text>
                                </svg>
                            </div>
                        </button>
                    </div>

                    <div class="recorder-controls" id="manual-controls">
                        <button class="btn-control" id="btn-record-start">
                            <i class="fa-solid fa-circle"></i> Record
                        </button>
                        <button class="btn-control" id="btn-record-pause" disabled>
                            <i class="fa-solid fa-pause"></i> Pause
                        </button>
                        <button class="btn-control" id="btn-record-stop" disabled>
                            <i class="fa-solid fa-square"></i> Stop
                        </button>
                    </div>

                    <!-- Selected Animation Dropdown style grid -->
                    <div class="style-selector">
                        <label>Microphone Animation Style</label>
                        <div class="style-grid" id="style-select-grid">
                            <div class="style-item active" data-anim="pulse">Traditional Mic</div>
                            <div class="style-item" data-anim="doraemon">Doraemon Face</div>
                            <div class="style-item" data-anim="fan">Rotating Fan</div>
                            <div class="style-item" data-anim="tom">Talking Tom</div>
                            <div class="style-item" data-anim="emoji">Emoji Face</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Voice Processing Card -->
            <div class="glass-card effects-panel">
                <h3>Voice Effects</h3>
                <div class="effects-grid" id="effects-grid-container">
                    <div class="effect-card active" data-effect="original">
                        <i class="fa-solid fa-user-check"></i>
                        <span>Original</span>
                    </div>
                    <div class="effect-card" data-effect="robot">
                        <i class="fa-solid fa-robot"></i>
                        <span>Robot Voice</span>
                    </div>
                    <div class="effect-card" data-effect="deep">
                        <i class="fa-solid fa-volume-low"></i>
                        <span>Deep Voice</span>
                    </div>
                    <div class="effect-card" data-effect="chipmunk">
                        <i class="fa-solid fa-squirrel"></i>
                        <span>Chipmunk</span>
                    </div>
                    <div class="effect-card" data-effect="cartoon">
                        <i class="fa-solid fa-cat"></i>
                        <span>Talking Tom</span>
                    </div>
                    <div class="effect-card" data-effect="radio">
                        <i class="fa-solid fa-walkie-talkie"></i>
                        <span>Radio Voice</span>
                    </div>
                </div>
                
                <!-- Audio Player controls -->
                <div class="audio-player-card" id="playback-card" style="display: none;">
                    <button id="player-play-btn"><i class="fa-solid fa-play"></i></button>
                    <div class="playback-progress" id="player-progress-bar">
                        <div class="progress-fill" id="player-progress-fill"></div>
                    </div>
                    <div class="progress-time" id="player-progress-time">0:00</div>
                    <audio id="audio-element"></audio>
                </div>
            </div>
        </div>

        <!-- Right Side: Dashboard Analytics -->
        <div class="analytics-panel">
            <div class="dashboard-grid">
                <div class="glass-card stat-card">
                    <div class="stat-icon purple">
                        <i class="fa-solid fa-microphone-lines"></i>
                    </div>
                    <div class="stat-info">
                        <h4>Total Sessions</h4>
                        <p id="stat-total-sessions">0</p>
                    </div>
                </div>
                <div class="glass-card stat-card">
                    <div class="stat-icon teal">
                        <i class="fa-solid fa-gauge-high"></i>
                    </div>
                    <div class="stat-info">
                        <h4>Average Speed</h4>
                        <p id="stat-avg-wpm">0 WPM</p>
                    </div>
                </div>
                <div class="glass-card stat-card">
                    <div class="stat-icon pink">
                        <i class="fa-solid fa-square-poll-vertical"></i>
                    </div>
                    <div class="stat-info">
                        <h4>Avg Confidence</h4>
                        <p id="stat-avg-confidence">0/100</p>
                    </div>
                </div>
                <div class="glass-card stat-card">
                    <div class="stat-icon purple" style="color: var(--accent); background: rgba(236, 72, 153, 0.1);">
                        <i class="fa-solid fa-chart-line"></i>
                    </div>
                    <div class="stat-info">
                        <h4>Avg Communication</h4>
                        <p id="stat-avg-communication">0/100</p>
                    </div>
                </div>
            </div>

            <!-- Detail Section -->
            <div class="glass-card analysis-detail">
                <div class="analysis-header">
                    <div class="analysis-title">
                        <h3 id="detail-title">Communication Intelligence</h3>
                        <p id="detail-date">Record speech on the left to start processing</p>
                    </div>
                    <div class="score-pill" id="detail-comm-score-pill" style="display: none;">
                        <i class="fa-solid fa-award"></i> Score: <span id="detail-comm-score">0</span>/100
                    </div>
                </div>

                <div class="analysis-content" id="detail-empty-state">
                    <div style="grid-column: 1 / span 2; text-align: center; padding: 40px 0; color: var(--text-secondary);">
                        <i class="fa-solid fa-microchip-ai" style="font-size: 48px; margin-bottom: 16px; color: var(--primary);"></i>
                        <p>No active session loaded. Record or select a session from history below.</p>
                    </div>
                </div>

                <div class="analysis-content" id="detail-data-state" style="display: none;">
                    <div class="transcript-box">
                        <label>Speech Transcript</label>
                        <div class="transcript-text" id="detail-transcript"></div>
                    </div>
                    <div class="metrics-breakdown">
                        <div class="metric-row">
                            <span class="metric-label">Words Per Minute</span>
                            <div style="display: flex; align-items: center; gap: 8px;">
                                <span class="metric-value" id="detail-wpm">0</span>
                                <span class="metric-badge" id="detail-wpm-badge">Normal</span>
                            </div>
                        </div>
                        <div class="metric-row">
                            <span class="metric-label">Confidence Score</span>
                            <span class="metric-value" id="detail-confidence-score">0/100</span>
                        </div>
                        <div class="metric-row">
                            <span class="metric-label">Filler Word Count</span>
                            <span class="metric-value" id="detail-filler-count">0</span>
                        </div>
                        <div class="metric-row">
                            <span class="metric-label">Pause Frequency</span>
                            <span class="metric-value" id="detail-pause-count">0</span>
                        </div>
                        <div class="metric-row">
                            <span class="metric-label">Speech Continuity</span>
                            <span class="metric-value" id="detail-active-ratio">0%</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- History and Chart Toggle tabs -->
            <div class="glass-card">
                <div class="tabs-header">
                    <span class="tab-link active" data-tab="tab-history">Session History</span>
                    <span class="tab-link" data-tab="tab-progress">Intelligence Progress</span>
                </div>

                <div class="tab-content active" id="tab-history">
                    <div class="history-list" id="history-list-container">
                        <!-- History items populating via JS -->
                        <div style="text-align: center; padding: 20px; color: var(--text-secondary);">
                            No sessions found.
                        </div>
                    </div>
                </div>

                <div class="tab-content" id="tab-progress">
                    <div class="chart-container">
                        <svg class="chart-svg" id="progress-chart-svg" viewBox="0 0 500 200" preserveAspectRatio="none">
                            <!-- SVG elements generated dynamically -->
                        </svg>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <footer>
        <p>Echo AI &copy; 2026. Made with Precision for Speech Analytics. Secure & Privacy-First.</p>
    </footer>

    <div class="toast" id="notification-toast">Speech analyzed!</div>

    <script>
        // Global variables for recording states and configuration
        let currentMode = "echo"; // 'recorder' or 'echo'
        let selectedAnimation = "pulse"; // pulse, doraemon, fan, tom, emoji
        let selectedEffect = "original";
        
        let isRecording = false;
        let wantsToRecord = false;
        let isPaused = false;
        let pauseCount = 0;
        let pauseStartTime = 0;
        let pausedDuration = 0;
        
        let recordingStartTime = 0;
        let timerInterval = null;
        let audioContext = null;
        let scriptProcessor = null;
        let mediaStream = null;
        let inputPoint = null;
        let leftchannel = [];
        let recordingLength = 0;
        let sampleRate = 44100;
        let currentSession = null;
        let theme = "dark";
        
        // Emoji cycle timer
        let emojiCycleInterval = null;
        let emojiIndex = 0;
        
        // 50 unique native Unicode emojis for high-fidelity expressions
        const EMOJI_LIST_50 = [
            "😃","😆","😅","😂","🤣","😊","😇","🙂","🙃","😉",
            "😌","😍","🥰","😘","😗","😙","😚","😋","😛","😝",
            "😜","🤪","🤨","🧐","🤓","😎","🤩","🥳","😏","😒",
            "😞","😔","😟","😕","🙁","☹️","😣","😖","😫","😩",
            "🥺","😢","😭","😤","😠","😡","🤬","🤯","😳","🥵"
        ];
        
        // Playback state variables
        const audioElement = document.getElementById("audio-element");
        let playbackProgressInterval = null;

        // Toast notifications helper
        function showToast(message) {
            const toast = document.getElementById("notification-toast");
            toast.textContent = message;
            toast.style.display = "block";
            setTimeout(() => {
                toast.style.display = "none";
            }, 3000);
        }

        // Initialize theme handling
        const themeBtn = document.getElementById("theme-toggle-btn");
        themeBtn.addEventListener("click", () => {
            theme = theme === "dark" ? "light" : "dark";
            document.body.setAttribute("data-theme", theme);
            themeBtn.innerHTML = theme === "dark" ? '<i class="fa-solid fa-moon"></i>' : '<i class="fa-solid fa-sun"></i>';
        });

        // Toggle Recording Modes
        const modeRecorder = document.getElementById("mode-recorder");
        const modeEcho = document.getElementById("mode-echo");
        const manualControls = document.getElementById("manual-controls");
        const statusText = document.getElementById("status-text");

        currentMode = "echo";
        modeEcho.classList.add("active");
        modeRecorder.classList.remove("active");
        manualControls.style.display = "none";
        statusText.textContent = "Press & Hold Mic Button";

        modeRecorder.addEventListener("click", () => {
            if (isRecording || wantsToRecord) stopRecording();
            currentMode = "recorder";
            modeRecorder.classList.add("active");
            modeEcho.classList.remove("active");
            manualControls.style.display = "flex";
            statusText.textContent = "Ready to Record";
        });

        modeEcho.addEventListener("click", () => {
            if (isRecording || wantsToRecord) stopRecording();
            currentMode = "echo";
            modeEcho.classList.add("active");
            modeRecorder.classList.remove("active");
            manualControls.style.display = "none";
            statusText.textContent = "Press & Hold Mic Button";
        });

        // Handle animation style item clicks
        const styleItems = document.querySelectorAll(".style-item");
        styleItems.forEach(item => {
            item.addEventListener("click", (e) => {
                styleItems.forEach(i => i.classList.remove("active"));
                e.target.classList.add("active");
                selectedAnimation = e.target.dataset.anim;
                updateMicAnimationsUI();
            });
        });

        function updateMicAnimationsUI() {
            const container = document.getElementById("record-container");
            const animPulse = document.getElementById("anim-pulse");
            
            const micIcon = document.getElementById("traditional-mic-icon");
            const doraemonFace = document.getElementById("doraemon-face-wrapper");
            const fanBlade = document.getElementById("rotating-fan-wrapper");
            const tomFace = document.getElementById("talking-tom-wrapper");
            const emojiFace = document.getElementById("emoji-face-wrapper");

            animPulse.style.display = "none";
            
            micIcon.style.display = "block";
            doraemonFace.style.display = "none";
            fanBlade.style.display = "none";
            tomFace.style.display = "none";
            emojiFace.style.display = "none";
            
            if (emojiCycleInterval) {
                clearInterval(emojiCycleInterval);
                emojiCycleInterval = null;
            }

            if (selectedAnimation === "doraemon") {
                micIcon.style.display = "none";
                doraemonFace.style.display = "flex";
            } else if (selectedAnimation === "fan") {
                micIcon.style.display = "none";
                fanBlade.style.display = "flex";
            } else if (selectedAnimation === "tom") {
                micIcon.style.display = "none";
                tomFace.style.display = "flex";
            } else if (selectedAnimation === "emoji") {
                micIcon.style.display = "none";
                emojiFace.style.display = "flex";
                // Reset emoji to default
                document.getElementById("emoji-char").textContent = EMOJI_LIST_50[0];
            }

            if (isRecording) {
                container.classList.add("recording");
                if (selectedAnimation === "pulse") {
                    animPulse.style.display = "block";
                } else if (selectedAnimation === "emoji") {
                    // Slower transition between emojis: cycle every 750ms as requested
                    emojiIndex = 0;
                    emojiCycleInterval = setInterval(() => {
                        emojiIndex = (emojiIndex + 1) % EMOJI_LIST_50.length;
                        document.getElementById("emoji-char").textContent = EMOJI_LIST_50[emojiIndex];
                    }, 750);
                }
            } else {
                container.classList.remove("recording");
            }
        }

        // Timer Display
        function startTimer() {
            if (!recordingStartTime) {
                recordingStartTime = Date.now();
            }
            timerInterval = setInterval(() => {
                const diff = Date.now() - recordingStartTime - pausedDuration;
                const min = Math.floor(diff / 60000).toString().padStart(2, '0');
                const sec = Math.floor((diff % 60000) / 1000).toString().padStart(2, '0');
                const ms = Math.floor((diff % 1000) / 100);
                document.getElementById("duration-timer").textContent = `${min}:${sec}.${ms}`;
            }, 100);
        }

        function stopTimer() {
            if (timerInterval) clearInterval(timerInterval);
        }

        function updateRecorderControls() {
            const btnPause = document.getElementById("btn-record-pause");
            const btnStart = document.getElementById("btn-record-start");
            const btnStop = document.getElementById("btn-record-stop");

            btnStart.disabled = isRecording;
            btnStop.disabled = !isRecording;
            btnPause.disabled = !isRecording;
            btnPause.style.display = isRecording ? "inline-flex" : "none";
            btnPause.innerHTML = `<i class="fa-solid fa-${isPaused ? 'play' : 'pause'}"></i> ${isPaused ? 'Resume' : 'Pause'}`;
        }

        function pauseRecording() {
            if (!isRecording || isPaused) return;
            isPaused = true;
            pauseCount += 1;
            pauseStartTime = Date.now();
            stopTimer();
            statusText.textContent = "Recording paused";
            document.getElementById("mic-trigger").style.transform = "scale(1)";
            updateRecorderControls();
        }

        function resumeRecording() {
            if (!isRecording || !isPaused) return;
            isPaused = false;
            pausedDuration += Date.now() - pauseStartTime;
            pauseStartTime = 0;
            startTimer();
            statusText.textContent = "Recording...";
            document.getElementById("mic-trigger").style.transform = "scale(0.95)";
            updateRecorderControls();
        }

        // Web Audio recording engine (direct WAV compilation in browser)
        async function startRecording() {
            if (isRecording || wantsToRecord) return;
            wantsToRecord = true;
            isPaused = false;
            pauseCount = 0;
            pauseStartTime = 0;
            pausedDuration = 0;
            
            leftchannel = [];
            recordingLength = 0;
            
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ 
                    audio: {
                        noiseSuppression: true,
                        echoCancellation: true,
                        autoGainControl: true
                    } 
                });
                
                if (!wantsToRecord) {
                    stream.getTracks().forEach(track => track.stop());
                    return;
                }
                
                mediaStream = stream;
                audioContext = new (window.AudioContext || window.webkitAudioContext)();
                sampleRate = audioContext.sampleRate;
                
                inputPoint = audioContext.createMediaStreamSource(mediaStream);
                scriptProcessor = audioContext.createScriptProcessor(2048, 1, 1);
                
                scriptProcessor.onaudioprocess = function(e) {
                    const left = e.inputBuffer.getChannelData(0);
                    leftchannel.push(new Float32Array(left));
                    recordingLength += 2048;
                };
                
                inputPoint.connect(scriptProcessor);
                scriptProcessor.connect(audioContext.destination);
                
                isRecording = true;
                wantsToRecord = false;
                recordingStartTime = Date.now();
                pausedDuration = 0;
                pauseStartTime = 0;
                
                updateMicAnimationsUI();
                startTimer();
                updateRecorderControls();
                
                statusText.textContent = "Listening...";
                document.getElementById("mic-trigger").style.transform = "scale(0.95)";
                
            } catch (err) {
                wantsToRecord = false;
                console.error("Mic access denied or error:", err);
                showToast("Microphone access is required.");
                statusText.textContent = "Ready to Record";
            }
        }

        async function stopRecording() {
            wantsToRecord = false;
            
            if (!isRecording) return;
            
            if (isPaused && pauseStartTime) {
                pausedDuration += Date.now() - pauseStartTime;
                pauseStartTime = 0;
                isPaused = false;
            }
            
            stopTimer();
            isRecording = false;
            updateMicAnimationsUI();
            updateRecorderControls();
            
            statusText.textContent = "Analyzing speech...";
            document.getElementById("mic-trigger").style.transform = "scale(1)";
            
            if (scriptProcessor) {
                scriptProcessor.disconnect();
                scriptProcessor.onaudioprocess = null;
            }
            if (inputPoint) inputPoint.disconnect();
            if (mediaStream) {
                mediaStream.getTracks().forEach(track => track.stop());
            }
            if (audioContext) audioContext.close();

            const elapsedSec = (Date.now() - recordingStartTime - pausedDuration) / 1000.0;
            
            if (elapsedSec < 0.5) {
                showToast("Hold down the button to record speech.");
                statusText.textContent = "Ready to Record";
                return;
            }
            
            const wavBlob = compileWav();
            await uploadRecording(wavBlob, elapsedSec);
        }

        function compileWav() {
            const flatChannel = flattenArray(leftchannel, recordingLength);
            const bufferVal = new ArrayBuffer(44 + recordingLength * 2);
            const view = new DataView(bufferVal);
            
            writeString(view, 0, 'RIFF');
            view.setUint32(4, 36 + recordingLength * 2, true);
            writeString(view, 8, 'WAVE');
            writeString(view, 12, 'fmt ');
            view.setUint32(16, 16, true);
            view.setUint16(20, 1, true);
            view.setUint16(22, 1, true);
            view.setUint32(24, sampleRate, true);
            view.setUint32(28, sampleRate * 2, true);
            view.setUint16(32, 2, true);
            view.setUint16(34, 16, true);
            writeString(view, 36, 'data');
            view.setUint32(40, recordingLength * 2, true);
            
            let index = 44;
            const length = flatChannel.length;
            for (let i = 0; i < length; i++) {
                let sample = Math.max(-1, Math.min(1, flatChannel[i]));
                view.setInt16(index, sample < 0 ? sample * 0x8000 : sample * 0x7FFF, true);
                index += 2;
            }
            
            return new Blob([bufferVal], { type: 'audio/wav' });
        }

        function flattenArray(channelBuffer, recordingLength) {
            const result = new Float32Array(recordingLength);
            let offset = 0;
            for (let i = 0; i < channelBuffer.length; i++) {
                const buffer = channelBuffer[i];
                result.set(buffer, offset);
                offset += buffer.length;
            }
            return result;
        }

        function writeString(view, offset, string) {
            for (let i = 0; i < string.length; i++) {
                view.setUint8(offset + i, string.charCodeAt(i));
            }
        }

        // Upload and handle analyzed JSON response
        async function uploadRecording(blob, durationSec) {
            const formData = new FormData();
            formData.append("file", blob, "recording.wav");
            formData.append("duration", durationSec);

            try {
                const response = await fetch("/api/analyze", {
                    method: "POST",
                    body: formData
                });

                if (!response.ok) throw new Error("Backend analysis failed");
                
                const session = await response.json();
                session.pause_count = pauseCount;
                const totalDuration = durationSec + pausedDuration / 1000;
                session.active_ratio = totalDuration > 0 ? `${Math.round((durationSec / totalDuration) * 100)}%` : "100%";
                currentSession = session;
                
                showToast("Speech analyzed successfully!");
                statusText.textContent = "Analysis Complete";
                
                loadSessionDetail(session);
                
                if (currentMode === "echo") {
                    await playVoiceEffect("original");
                } else {
                    setupAudioPlayer(`/static/audio/${session.audio_filename}`);
                }
                
                await fetchDashboardData();
                
            } catch (err) {
                console.error(err);
                showToast("Failed to analyze speech. Ensure backend server is active.");
                statusText.textContent = "Ready to Record";
            }
        }

        function loadSessionDetail(session) {
            document.getElementById("detail-empty-state").style.display = "none";
            const dataState = document.getElementById("detail-data-state");
            dataState.style.display = "grid";
            
            const localDate = new Date(session.timestamp).toLocaleString();
            document.getElementById("detail-date").textContent = localDate;
            document.getElementById("detail-title").textContent = `Communication Intelligence Session`;
            
            const scorePill = document.getElementById("detail-comm-score-pill");
            scorePill.style.display = "flex";
            document.getElementById("detail-comm-score").textContent = session.communication_score;
            
            document.getElementById("detail-transcript").textContent = session.transcript;
            document.getElementById("detail-wpm").textContent = `${session.wpm} WPM`;
            document.getElementById("detail-confidence-score").textContent = `${session.confidence_score}/100`;
            
            const wpmBadge = document.getElementById("detail-wpm-badge");
            wpmBadge.textContent = session.speed_category;
            wpmBadge.className = "metric-badge";
            if (session.speed_category.toLowerCase() === "slow") {
                wpmBadge.classList.add("badge-slow");
            } else if (session.speed_category.toLowerCase() === "fast") {
                wpmBadge.classList.add("badge-fast");
            } else {
                wpmBadge.classList.add("badge-normal");
            }

            const words = session.transcript.split(/\\s+/).filter(Boolean);
            const fillerCount = words.filter(w => ["uh","um","ah","like","so","er"].includes(w.toLowerCase())).length;
            document.getElementById("detail-filler-count").textContent = fillerCount;
            document.getElementById("detail-pause-count").textContent = session.pause_count ?? 0;
            document.getElementById("detail-active-ratio").textContent = session.active_ratio ?? "100%";

            selectedEffect = "original";
            highlightSelectedEffectCard("original");
        }

        async function playVoiceEffect(effectType) {
            if (!currentSession) return;
            
            selectedEffect = effectType;
            highlightSelectedEffectCard(effectType);
            
            if (effectType === "original") {
                setupAudioPlayer(`/static/audio/${currentSession.audio_filename}`);
                audioElement.play().catch(e => console.log("Playback failed", e));
                return;
            }

            try {
                const response = await fetch("/api/voice-effect", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        session_id: currentSession.session_id,
                        effect: effectType
                    })
                });

                if (!response.ok) throw new Error("Failed to process voice effect");
                
                const data = await response.json();
                setupAudioPlayer(data.processed_audio);
                audioElement.play().catch(e => console.log("Audio play blocked", e));
                
            } catch (err) {
                console.error(err);
                showToast("Failed to apply voice effect");
            }
        }

        function highlightSelectedEffectCard(effectType) {
            const cards = document.querySelectorAll(".effect-card");
            cards.forEach(c => {
                if (c.dataset.effect === effectType) {
                    c.classList.add("active");
                } else {
                    c.classList.remove("active");
                }
            });
        }

        const effectCards = document.querySelectorAll(".effect-card");
        effectCards.forEach(c => {
            c.addEventListener("click", () => {
                if (!currentSession) {
                    showToast("Please record a speech session first.");
                    return;
                }
                playVoiceEffect(c.dataset.effect);
            });
        });

        function setupAudioPlayer(src) {
            const cacheKey = `_=${Date.now()}`;
            audioElement.src = src + (src.includes('?') ? '&' : '?') + cacheKey;
            audioElement.playbackRate = 1.0;
            if (typeof audioElement.preservesPitch !== 'undefined') {
                audioElement.preservesPitch = true;
            }
            audioElement.currentTime = 0;
            audioElement.load();
            
            const playbackCard = document.getElementById("playback-card");
            playbackCard.style.display = "flex";
            
            const playBtn = document.getElementById("player-play-btn");
            playBtn.innerHTML = '<i class="fa-solid fa-play"></i>';
            
            document.getElementById("player-progress-fill").style.width = "0%";
            document.getElementById("player-progress-time").textContent = "0:00";
        }

        const playBtn = document.getElementById("player-play-btn");
        playBtn.addEventListener("click", () => {
            if (audioElement.paused) {
                audioElement.play().catch(e => console.log(e));
                playBtn.innerHTML = '<i class="fa-solid fa-pause"></i>';
                startPlaybackTracking();
            } else {
                audioElement.pause();
                playBtn.innerHTML = '<i class="fa-solid fa-play"></i>';
                stopPlaybackTracking();
            }
        });

        function startPlaybackTracking() {
            if (playbackProgressInterval) clearInterval(playbackProgressInterval);
            playbackProgressInterval = setInterval(() => {
                if (audioElement.duration) {
                    const percent = (audioElement.currentTime / audioElement.duration) * 100;
                    document.getElementById("player-progress-fill").style.width = `${percent}%`;
                    
                    const min = Math.floor(audioElement.currentTime / 60);
                    const sec = Math.floor(audioElement.currentTime % 60).toString().padStart(2, '0');
                    document.getElementById("player-progress-time").textContent = `${min}:${sec}`;
                }
            }, 100);
        }

        function stopPlaybackTracking() {
            if (playbackProgressInterval) clearInterval(playbackProgressInterval);
        }

        audioElement.addEventListener("ended", () => {
            playBtn.innerHTML = '<i class="fa-solid fa-play"></i>';
            document.getElementById("player-progress-fill").style.width = "0%";
            document.getElementById("player-progress-time").textContent = "0:00";
            stopPlaybackTracking();
        });

        document.getElementById("player-progress-bar").addEventListener("click", (e) => {
            if (!audioElement.duration) return;
            const rect = e.target.getBoundingClientRect();
            const clickX = e.clientX - rect.left;
            const percent = clickX / rect.width;
            audioElement.currentTime = percent * audioElement.duration;
            document.getElementById("player-progress-fill").style.width = `${percent * 100}%`;
        });

        // Trigger slaps and dizzy spins on Talking Tom SVG
        const tomSvg = document.getElementById("tom-face-svg");
        
        tomSvg.addEventListener("click", (e) => {
            e.stopPropagation();
            
            const rect = tomSvg.getBoundingClientRect();
            const tapY = e.clientY - rect.top;
            const relativeHeight = tapY / rect.height;
            
            playSlapAudioFX();

            if (relativeHeight < 0.35) {
                triggerTomDizzySpin();
            } else {
                triggerTomCheekSlap();
            }
        });

        function triggerTomCheekSlap() {
            if (tomSvg.classList.contains("dizzy")) return;
            
            tomSvg.classList.remove("slapped");
            void tomSvg.offsetWidth;
            tomSvg.classList.add("slapped");
            
            const star = document.getElementById("tom-impact-star");
            star.style.display = "block";
            
            setTimeout(() => {
                star.style.display = "none";
                tomSvg.classList.remove("slapped");
            }, 180);
        }

        function triggerTomDizzySpin() {
            tomSvg.classList.remove("slapped");
            tomSvg.classList.remove("dizzy");
            void tomSvg.offsetWidth;
            tomSvg.classList.add("dizzy");
            
            document.getElementById("tom-eye-l").style.display = "none";
            document.getElementById("tom-eye-r").style.display = "none";
            document.getElementById("tom-pupil-l").style.display = "none";
            document.getElementById("tom-pupil-r").style.display = "none";
            document.getElementById("tom-pupil-black-l").style.display = "none";
            document.getElementById("tom-pupil-black-r").style.display = "none";
            document.getElementById("tom-eye-spiral-l").style.display = "block";
            document.getElementById("tom-eye-spiral-r").style.display = "block";
            document.getElementById("tom-mouth-smile").style.display = "none";
            document.getElementById("tom-mouth-dizzy").style.display = "block";
            
            const stars = document.getElementById("tom-dizzy-stars");
            stars.style.display = "block";
            
            setTimeout(() => {
                document.getElementById("tom-eye-l").style.display = "block";
                document.getElementById("tom-eye-r").style.display = "block";
                document.getElementById("tom-pupil-l").style.display = "block";
                document.getElementById("tom-pupil-r").style.display = "block";
                document.getElementById("tom-pupil-black-l").style.display = "block";
                document.getElementById("tom-pupil-black-r").style.display = "block";
                document.getElementById("tom-eye-spiral-l").style.display = "none";
                document.getElementById("tom-eye-spiral-r").style.display = "none";
                document.getElementById("tom-mouth-smile").style.display = "block";
                document.getElementById("tom-mouth-dizzy").style.display = "none";
                stars.style.display = "none";
                tomSvg.classList.remove("dizzy");
            }, 1100);
        }

        function playSlapAudioFX() {
            try {
                const ctx = new (window.AudioContext || window.webkitAudioContext)();
                const bufferSize = ctx.sampleRate * 0.08;
                const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
                const data = buffer.getChannelData(0);
                for (let i = 0; i < bufferSize; i++) {
                    data[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / bufferSize, 3);
                }
                
                const noiseNode = ctx.createBufferSource();
                noiseNode.buffer = buffer;
                
                const filter = ctx.createBiquadFilter();
                filter.type = "lowpass";
                filter.frequency.setValueAtTime(1200, ctx.currentTime);
                filter.Q.setValueAtTime(3, ctx.currentTime);
                
                const gain = ctx.createGain();
                gain.gain.setValueAtTime(0.45, ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.07);
                
                noiseNode.connect(filter);
                filter.connect(gain);
                gain.connect(ctx.destination);
                
                noiseNode.start();
            } catch (err) {
                console.log("AudioContext blocked slap synthesizer");
            }
        }

        const micTrigger = document.getElementById("mic-trigger");
        const btnRecordStart = document.getElementById("btn-record-start");
        const btnRecordPause = document.getElementById("btn-record-pause");
        const btnRecordStop = document.getElementById("btn-record-stop");

        btnRecordStart.addEventListener("click", () => {
            startRecording();
            btnRecordStart.disabled = true;
            btnRecordStop.disabled = false;
            btnRecordStart.classList.add("active-record");
        });

        btnRecordPause.addEventListener("click", () => {
            if (!isRecording) return;
            if (isPaused) {
                resumeRecording();
            } else {
                pauseRecording();
            }
        });

        btnRecordStop.addEventListener("click", () => {
            stopRecording();
            btnRecordStart.disabled = false;
            btnRecordStop.disabled = true;
            btnRecordStart.classList.remove("active-record");
        });

        micTrigger.addEventListener("mousedown", (e) => {
            e.stopPropagation();
            if (currentMode === "echo") startRecording();
        });

        window.addEventListener("mouseup", (e) => {
            if (currentMode === "echo" && (isRecording || wantsToRecord)) {
                stopRecording();
            }
        });

        micTrigger.addEventListener("touchstart", (e) => {
            e.preventDefault();
            e.stopPropagation();
            if (currentMode === "echo") startRecording();
        });

        window.addEventListener("touchend", (e) => {
            if (currentMode === "echo" && (isRecording || wantsToRecord)) {
                stopRecording();
            }
        });

        const tabLinks = document.querySelectorAll(".tab-link");
        tabLinks.forEach(link => {
            link.addEventListener("click", (e) => {
                tabLinks.forEach(l => l.classList.remove("active"));
                document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));
                
                e.target.classList.add("active");
                document.getElementById(e.target.dataset.tab).classList.add("active");
            });
        });

        async function fetchDashboardData() {
            try {
                const res = await fetch("/api/dashboard");
                const data = await res.json();
                
                document.getElementById("stat-total-sessions").textContent = data.total_recordings;
                document.getElementById("stat-avg-wpm").textContent = `${Math.round(data.average_wpm)} WPM`;
                document.getElementById("stat-avg-confidence").textContent = `${Math.round(data.average_confidence)}/100`;
                document.getElementById("stat-avg-communication").textContent = `${Math.round(data.average_communication)}/100`;
                
                populateHistoryList(data.recent_sessions);
                buildSVGCharts(data.communication_trend);
                
            } catch (err) {
                console.error("Dashboard fetch error:", err);
            }
        }

        function populateHistoryList(sessions) {
            const container = document.getElementById("history-list-container");
            container.innerHTML = "";
            
            if (sessions.length === 0) {
                container.innerHTML = `<div style="text-align: center; padding: 20px; color: var(--text-secondary);">No sessions found.</div>`;
                return;
            }

            sessions.forEach(s => {
                const date = new Date(s.timestamp).toLocaleDateString(undefined, {month: 'short', day: 'numeric', hour: '2-digit', minute:'2-digit'});
                const duration = s.duration.toFixed(1);
                
                const item = document.createElement("div");
                item.className = "history-item";
                item.innerHTML = `
                    <div class="history-meta" onclick="loadHistoryItem('${s.session_id}')">
                        <h5>Speech Session</h5>
                        <p>${date} &bull; ${duration}s &bull; ${s.word_count} words</p>
                    </div>
                    <div class="history-score">
                        <span class="hist-pill comm">Score: ${s.communication_score}</span>
                        <button class="btn-delete-hist" onclick="event.stopPropagation(); deleteHistoryItem('${s.session_id}')">
                            <i class="fa-solid fa-trash-can"></i>
                        </button>
                    </div>
                `;
                container.appendChild(item);
            });
        }

        async function loadHistoryItem(sessionId) {
            try {
                const res = await fetch(`/api/sessions`);
                const sessions = await res.json();
                const session = sessions.find(s => s.session_id === sessionId);
                if (session) {
                    currentSession = session;
                    loadSessionDetail(session);
                    setupAudioPlayer(`/static/audio/${session.audio_filename}`);
                    showToast("Session loaded from history");
                }
            } catch (err) {
                console.error(err);
            }
        }

        async function deleteHistoryItem(sessionId) {
            if(!confirm("Are you sure you want to delete this session?")) return;
            try {
                const res = await fetch(`/api/sessions/${sessionId}`, { method: "DELETE" });
                if (res.ok) {
                    showToast("Session deleted");
                    if (currentSession && currentSession.session_id === sessionId) {
                        currentSession = null;
                        document.getElementById("detail-data-state").style.display = "none";
                        document.getElementById("detail-empty-state").style.display = "block";
                        document.getElementById("playback-card").style.display = "none";
                        audioElement.src = "";
                    }
                    await fetchDashboardData();
                }
            } catch (err) {
                console.error(err);
            }
        }

        function buildSVGCharts(trendData) {
            const svg = document.getElementById("progress-chart-svg");
            svg.innerHTML = "";
            
            if (trendData.length < 2) {
                const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
                text.setAttribute("x", "50%");
                text.setAttribute("y", "50%");
                text.setAttribute("text-anchor", "middle");
                text.setAttribute("fill", "var(--text-secondary)");
                text.setAttribute("font-size", "14");
                text.textContent = "Need at least 2 sessions to compute score progression trend.";
                svg.appendChild(text);
                return;
            }

            const width = 500;
            const height = 200;
            const padding = 30;
            
            const stepX = (width - padding * 2) / (trendData.length - 1);
            
            for (let i = 1; i <= 4; i++) {
                const lineY = padding + (height - padding * 2) * (1 - i/4);
                
                const gridLine = document.createElementNS("http://www.w3.org/2000/svg", "line");
                gridLine.setAttribute("x1", padding);
                gridLine.setAttribute("y1", lineY);
                gridLine.setAttribute("x2", width - padding);
                gridLine.setAttribute("y2", lineY);
                gridLine.setAttribute("stroke", "var(--border-color)");
                gridLine.setAttribute("stroke-dasharray", "4,4");
                svg.appendChild(gridLine);
                
                const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
                label.setAttribute("x", padding - 5);
                label.setAttribute("y", lineY + 4);
                label.setAttribute("text-anchor", "end");
                label.setAttribute("font-size", "9");
                label.setAttribute("fill", "var(--text-secondary)");
                label.textContent = (i * 25).toString();
                svg.appendChild(label);
            }

            function getY(val) {
                const graphHeight = height - padding * 2;
                return padding + graphHeight * (1 - val / 100);
            }

            let commPoints = [];
            let confPoints = [];
            
            trendData.forEach((point, idx) => {
                const x = padding + idx * stepX;
                commPoints.push(`${x},${getY(point.communication_score)}`);
                confPoints.push(`${x},${getY(point.confidence_score)}`);
                
                if (trendData.length <= 10 || idx % 2 === 0) {
                    const xLabel = document.createElementNS("http://www.w3.org/2000/svg", "text");
                    xLabel.setAttribute("x", x);
                    xLabel.setAttribute("y", height - 10);
                    xLabel.setAttribute("text-anchor", "middle");
                    xLabel.setAttribute("font-size", "9");
                    xLabel.setAttribute("fill", "var(--text-secondary)");
                    xLabel.textContent = point.label;
                    svg.appendChild(xLabel);
                }
            });

            const confPath = document.createElementNS("http://www.w3.org/2000/svg", "path");
            confPath.setAttribute("d", `M ${confPoints.join(" L ")}`);
            confPath.setAttribute("fill", "none");
            confPath.setAttribute("stroke", "var(--accent)");
            confPath.setAttribute("stroke-width", "2.5");
            confPath.setAttribute("stroke-linecap", "round");
            confPath.setAttribute("stroke-linejoin", "round");
            svg.appendChild(confPath);

            const commPath = document.createElementNS("http://www.w3.org/2000/svg", "path");
            commPath.setAttribute("d", `M ${commPoints.join(" L ")}`);
            commPath.setAttribute("fill", "none");
            commPath.setAttribute("stroke", "var(--primary)");
            commPath.setAttribute("stroke-width", "3.5");
            commPath.setAttribute("stroke-linecap", "round");
            commPath.setAttribute("stroke-linejoin", "round");
            svg.appendChild(commPath);
            
            trendData.forEach((point, idx) => {
                const x = padding + idx * stepX;
                
                const cCircle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
                cCircle.setAttribute("cx", x);
                cCircle.setAttribute("cy", getY(point.communication_score));
                cCircle.setAttribute("r", "5");
                cCircle.setAttribute("fill", "var(--bg-primary)");
                cCircle.setAttribute("stroke", "var(--primary)");
                cCircle.setAttribute("stroke-width", "2.5");
                svg.appendChild(cCircle);
            });
        }

        window.addEventListener("load", () => {
            fetchDashboardData();
            updateMicAnimationsUI();
        });
    </script>
</body>
</html>
"""
