from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime, timezone

@dataclass
class Task:
    task_id: str
    description: str
    url: Optional[str] = ''
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    status: str = 'pending'

@dataclass
class TaskLog:
    log_id: str
    task_run_id: str
    step: str
    status: str
    started: Optional[str] = ''
    finished: Optional[str] = ''
    output: Optional[str] = ''
    created: Optional[str] = ''

@dataclass
class TaskRun:
    run_id: str
    task_id: str
    status: str
    started_at: Optional[str] = ''
    finished_at: Optional[str] = ''
    logs: List[TaskLog] = field(default_factory=list)
