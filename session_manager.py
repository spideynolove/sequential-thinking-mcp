import uuid
import weakref
from typing import Dict, List, Optional
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from models import ThinkingSession

class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, ThinkingSession] = {}
        self.session_refs: Dict[str, weakref.ref] = {}
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    def create_session(self, problem: str, criteria: str, constraints: List[str], coding_session: bool = False) -> str:
        session_id = str(uuid.uuid4())[:8]
        now = datetime.now().isoformat()
        
        session = ThinkingSession(
            id=session_id,
            problem_statement=problem,
            success_criteria=criteria,
            constraints=constraints,
            main_thread=[],
            branches={},
            patterns=[],
            started=now,
            last_updated=now,
            coding_session=coding_session
        )
        
        self.sessions[session_id] = session
        return session_id
    
    def get_session(self, session_id: str) -> Optional[ThinkingSession]:
        return self.sessions.get(session_id)
    
    def cleanup_session(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]
        if session_id in self.session_refs:
            del self.session_refs[session_id]
    
    def check_memory_limits(self, session_id: str) -> bool:
        session = self.sessions.get(session_id)
        if not session:
            return False
        
        thought_count = len(session.main_thread)
        for branch in session.branches.values():
            thought_count += len(branch.thoughts)
        
        if thought_count > session.config.max_thoughts:
            return False
        
        return True