"""Agenti del dipartimento contenuti."""
from .video_editor import VideoEditorAgent, SeniorVideoEditorAgent, JuniorVideoEditorAgent
from .photo_editor import PhotoEditorAgent, SeniorPhotoEditorAgent, JuniorPhotoEditorAgent
from .copywriter import CopywriterAgent, SeniorCopywriterAgent
from .graphic_designer import GraphicDesignerAgent
from .content_strategist import ContentStrategistAgent
from .content_director import ContentDirectorAgent

__all__ = [
    "ContentDirectorAgent",
    "VideoEditorAgent",
    "SeniorVideoEditorAgent",
    "JuniorVideoEditorAgent",
    "PhotoEditorAgent",
    "SeniorPhotoEditorAgent",
    "JuniorPhotoEditorAgent",
    "CopywriterAgent",
    "SeniorCopywriterAgent",
    "GraphicDesignerAgent",
    "ContentStrategistAgent",
]
