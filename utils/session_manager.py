import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

class SessionManager:
    def __init__(self, max_sessions: int = 100, session_timeout: int = 30):
        
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.max_sessions = max_sessions
        self.session_timeout = session_timeout

    def create_session(self, user_id: Optional[str] = None) -> str:
        
        # Clean up old sessions
        self._cleanup_sessions()
        
        # Generate unique session ID
        session_id = user_id or str(uuid.uuid4())
        
        # Create new session
        self.sessions[session_id] = {
            "created_at": datetime.now(),
            "last_active": datetime.now(),
            "query_history": [],
            "function_history": []
        }
        
        return session_id

    def update_session(self, session_id: str, query: str, function: str):
    
        if session_id not in self.sessions:
            self.create_session(session_id)
        
        session = self.sessions[session_id]
        session["last_active"] = datetime.now()
        session["query_history"].append({
            "query": query,
            "timestamp": datetime.now()
        })
        session["function_history"].append({
            "function": function,
            "timestamp": datetime.now()
        })

    def get_session_context(self, session_id: str) -> Dict:
        
        return self.sessions.get(session_id, {})

    def _cleanup_sessions(self):
       
        current_time = datetime.now()
        expired_sessions = [
            sid for sid, session in self.sessions.items()
            if (current_time - session['last_active']) > timedelta(minutes=self.session_timeout)
        ]
        
        for sid in expired_sessions:
            del self.sessions[sid]