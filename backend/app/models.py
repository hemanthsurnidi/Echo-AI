from pydantic import BaseModel
from typing import List, Dict, Any

class SessionResponse(BaseModel):
    session_id: str
    timestamp: str
    transcript: str
    word_count: int
    wpm: float
    speed_category: str
    confidence_score: int
    communication_score: int
    duration: float
    audio_filename: str

class VoiceEffectRequest(BaseModel):
    session_id: str
    effect: str  # 'robot', 'deep', 'chipmunk', 'cartoon', 'radio', 'original'

class VoiceEffectResponse(BaseModel):
    session_id: str
    effect: str
    original_audio: str
    processed_audio: str

class ChartDataPoint(BaseModel):
    label: str  # e.g., Date or index
    wpm: float
    confidence_score: float
    communication_score: float

class DashboardMetricsResponse(BaseModel):
    total_recordings: int
    average_wpm: float
    average_confidence: float
    average_communication: float
    wpm_trend: List[ChartDataPoint]
    confidence_trend: List[ChartDataPoint]
    communication_trend: List[ChartDataPoint]
    recent_sessions: List[SessionResponse]
