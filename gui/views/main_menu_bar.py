"""Main menu bar of the app."""

from typing import Callable, Optional, TYPE_CHECKING, cast

from PySide6.QtGui import QKeySequence, QAction
from PySide6.QtWidgets import QMenuBar

from gui.services.sequence_gui_service import SequenceGUIService
from gui.services.project_gui_service import ProjectGUIService

if TYPE_CHECKING:
    from gui.views.main_window import MainWindow


class MainMenuBar(QMenuBar):
    """Main menu bar of the app."""

    def __init__(self, parent: 'MainWindow'):
        super().__init__(parent)
        self.create_file_menu()
        self.create_edit_menu()
        self.create_sequence_menu()
        self.create_layer_menu()

    def create_file_menu(self):
        """Create the file menu."""
        _menu = self.addMenu("&File")
        _menu.addAction(self._action("New project", ProjectGUIService.create_new_project, "Ctrl+Shift+N"))
        _menu.addAction(self._action("Open project", ProjectGUIService.open_project, "Ctrl+O"))
        _menu.addSeparator()
        _menu.addAction(self._action("Save project", ProjectGUIService.save_project, "Ctrl+S"))
        _menu.addAction(self._action("Save project as", ProjectGUIService.save_project_as, "Ctrl+Shift+S"))
        _menu.addSeparator()
        _menu.addAction(self._action("Export video", ProjectGUIService.export_video, "Ctrl+E"))
        _menu.addSeparator()
        _menu.addAction(self._action("Project parameters", ProjectGUIService.show_project_parameters, "Ctrl+P"))
        _menu.addSeparator()
        _menu.addAction(self._action("Close", lambda: cast('MainWindow', self.parent()).close(), "Ctrl+Q"))
    
    def create_edit_menu(self):
        """Create the edit menu."""
        _menu = self.addMenu("&Edit")
        _menu.addAction(self._action("Cut", None, "Ctrl+X"))
        _menu.addAction(self._action("Copy", None, "Ctrl+C"))
        _menu.addAction(self._action("Paste", None, "Ctrl+V"))
    
    def create_sequence_menu(self):
        """Create the sequence menu."""
        _menu = self.addMenu("&Sequence")

        _menu.addAction(
            self._action("New sequence",
                         SequenceGUIService.create_new_sequence,
                         "Ctrl+N"))
        
        _menu.addSeparator()

        _parameters = self._action("Sequence parameters",
                                   SequenceGUIService.open_sequence_parameters,
                                   "Ctrl+K")
        _parameters.setEnabled(False)
        SequenceGUIService.focus_sequence_signal.connect(
            lambda sequence_id:
            self._toggle_action(_parameters, sequence_id is not None)
        )
        _menu.addAction(_parameters)
    
    def create_layer_menu(self):
        """Create the layer menu."""
        _menu = self.addMenu("&Layer")

        _new_solid = self._action("New solid layer",
                                  SequenceGUIService.create_new_solid_layer,
                                  "Ctrl+Y")
        _new_solid.setEnabled(False)
        SequenceGUIService.focus_sequence_signal.connect(
            lambda sequence_id:
            self._toggle_action(_new_solid, sequence_id is not None)
        )
        _menu.addAction(_new_solid)

        _menu.addSeparator()

        _parameters = self._action("Layer parameters", None, "Ctrl+Shift+Y")
        _parameters.setEnabled(False)
        _menu.addAction(_parameters)

    def _action(self,
                  title: str,
                  function: Optional[Callable] = None,
                  shortcut: Optional[str] = None
                  ) -> QAction:
        """Create a QAction for the menu bar."""
        _action = QAction(title, self)
        _action.setStatusTip(title)
        if function is not None:
            _action.triggered.connect(function)
        else:
            _action.setEnabled(False)
        if shortcut is not None:
            _action.setShortcut(QKeySequence(shortcut))
        return _action

    def _toggle_action(self, action: QAction, toggle: bool):
        """Enable / disable a menu action."""
        action.setEnabled(toggle)
