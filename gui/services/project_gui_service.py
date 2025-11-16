# filepath: e:\SciMotion\gui\services\project_gui_service.py
"""GUI service for project operations."""

import os
from typing import Optional

from PySide6.QtWidgets import QFileDialog, QMessageBox
from PySide6.QtCore import Signal, QObject

from core.services.project_service import ProjectService
from core.entities.project import Project
from gui.services.sequence_gui_service import SequenceGUIService


class ProjectGUIServiceSignals(QObject):
    """Signals for ProjectGUIService."""
    project_changed = Signal()


class ProjectGUIService:
    """Service to handle project-related GUI operations."""
    
    current_project: Optional[Project] = None  # Will always reference the static Project class
    current_file_path: Optional[str] = None
    signals = ProjectGUIServiceSignals()
    
    @classmethod
    def create_new_project(cls):
        """Create a new project."""
        if not cls._check_save_current():
            return
        
        cls.current_project = ProjectService.create_project()
        cls.current_file_path = None
        SequenceGUIService.clear_sequences()
        cls.signals.project_changed.emit()
        print("New project created!")  # Debug
        QMessageBox.information(None, "New Project", "New project created successfully!")
    
    @classmethod
    def open_project(cls):
        """Open an existing project."""
        if not cls._check_save_current():
            return
        
        file_path, _ = QFileDialog.getOpenFileName(
            None, 
            "Open Project", 
            "", 
            "SciMotion Project (*.smp);;All Files (*)"
        )
        
        if file_path:
            try:
                cls.current_project = ProjectService.load_project(file_path)
                cls.current_file_path = file_path
                SequenceGUIService.load_sequences_from_project(cls.current_project)
                cls.signals.project_changed.emit()
                QMessageBox.information(None, "Success", f"Project loaded: {os.path.basename(file_path)}")
            except Exception as e:
                QMessageBox.critical(None, "Error", f"Failed to open project:\n{str(e)}")
    
    @classmethod
    def save_project(cls):
        """Save the current project."""
        if not cls.current_project:
            QMessageBox.warning(None, "No Project", "No project to save!")
            return
        
        if cls.current_file_path:
            try:
                ProjectService.save_project(cls.current_project, cls.current_file_path)
                QMessageBox.information(None, "Success", "Project saved successfully!")
            except Exception as e:
                QMessageBox.critical(None, "Error", f"Failed to save project:\n{str(e)}")
        else:
            cls.save_project_as()
    
    @classmethod
    def save_project_as(cls):
        """Save project with new name."""
        if not cls.current_project:
            QMessageBox.warning(None, "No Project", "No project to save!")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            None,
            "Save Project As",
            "",
            "SciMotion Project (*.smp);;All Files (*)"
        )
        
        if file_path:
            if not file_path.endswith('.smp'):
                file_path += '.smp'
            
            try:
                ProjectService.save_project(cls.current_project, file_path)
                cls.current_file_path = file_path
                QMessageBox.information(None, "Success", f"Project saved: {os.path.basename(file_path)}")
            except Exception as e:
                QMessageBox.critical(None, "Error", f"Failed to save project:\n{str(e)}")
    
    @classmethod
    def export_video(cls):
        """Export current sequence as video."""
        if not SequenceGUIService.focus_sequence_id:
            QMessageBox.warning(None, "No Sequence", "Please select a sequence to export!")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            None,
            "Export Video",
            "",
            "PNG Sequence (*.png);;All Files (*)"
        )
        
        if file_path:
            try:
                from core.services.render_service import RenderService
                from utils.image import save_image
                import numpy as np
                
                sequence = SequenceGUIService.get_focused_sequence()
                if not sequence:
                    QMessageBox.warning(None, "Error", "No sequence selected!")
                    return
                
                duration = sequence.get_duration()
                
                # Create progress dialog
                from PySide6.QtWidgets import QProgressDialog
                progress = QProgressDialog("Exporting frames...", "Cancel", 0, duration, None)
                progress.setWindowTitle("Export Video")
                progress.setWindowModality(2)  # Qt.WindowModal
                
                # Export as PNG sequence
                base_path = file_path.replace('.png', '')
                for frame in range(duration):
                    if progress.wasCanceled():
                        break
                    
                    progress.setValue(frame)
                    texture = RenderService.render_sequence_frame(sequence, frame)
                    
                    if texture is not None:
                        # Convert moderngl.Texture to numpy array
                        output = np.frombuffer(
                            texture.read(), 
                            dtype=np.float32
                        ).reshape((sequence.get_height(), sequence.get_width(), 4))
                        
                        frame_path = f"{base_path}_{frame:04d}.png"
                        save_image(output, frame_path)
                
                progress.setValue(duration)
                
                if not progress.wasCanceled():
                    QMessageBox.information(None, "Success", f"Video exported successfully!\n{duration} frames saved.")
            except Exception as e:
                QMessageBox.critical(None, "Error", f"Failed to export:\n{str(e)}")
    
    @classmethod
    def show_project_parameters(cls):
        """Show project parameters dialog."""
        if not cls.current_project:
            QMessageBox.warning(None, "No Project", "No project is currently open!")
            return
        
        # TODO: Implement project parameters dialog
        QMessageBox.information(None, "Project Parameters", "Project parameters dialog not yet implemented")
    
    @classmethod
    def _check_save_current(cls) -> bool:
        """Check if current project needs saving."""
        if cls.current_project and len(Project.get_sequence_dict()) > 0:
            reply = QMessageBox.question(
                None,
                "Save Project?",
                "Do you want to save the current project?",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
            )
            
            if reply == QMessageBox.Yes:
                cls.save_project()
                return True
            elif reply == QMessageBox.No:
                return True
            else:
                return False
        return True