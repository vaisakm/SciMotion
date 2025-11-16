"""A set of services for inputs."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QWidget, QBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QDialog, QMessageBox)

from core.entities.parameter_template import ParameterTemplate, ParameterFlag
from core.entities.parameter import Parameter
from data_types.color import Color
from data_types.vector2 import Vector2
from data_types.boolean import Boolean
from data_types.number import Number
from data_types.integer import Integer
from data_types.data_type import DataType
from gui.views.inputs.color_input import ColorInput
from gui.views.inputs.vector2_input import Vector2Input
from gui.views.inputs.boolean_input import BooleanInput
from gui.views.inputs.number_input import NumberInput
from gui.views.inputs.integer_input import IntegerInput
from gui.views.inputs.dropdown_input import DropdownInput
from utils.notification import Notification
from gui.services.modifier_gui_service import ModifierGUIService


class InputGUIService:
    """A set of services for inputs."""
    
    # Track currently focused parameter for keyframe adding
    _focused_parameter: Parameter = None
    _focused_sequence_id: int = None
    _current_frame: int = 0  # Track current frame for keyframe adding
    
    @classmethod
    def input_from_parameter(cls,
                             parent: QWidget,
                             template: ParameterTemplate,
                             parameter: Parameter,
                             sequence_id: int,
                             layer_id: int) -> QWidget:
        """Create a GUI input from a Parameter."""
        _type = template.get_data_type()
        _input = None

        if _type is Color:
            # Color inputs :
            _input = ColorInput(parent, parameter.get_current_value())

        elif _type is Vector2:
            # Vector2 inputs :
            _input = Vector2Input(parent,
                                  parameter.get_current_value(),
                                  min=template.get_min_value(),
                                  max=template.get_max_value())
            
        elif _type is Boolean:
            # Boolean inputs :
            _input = BooleanInput(parent, parameter.get_current_value())

        elif _type is Number:
            # Number inputs :
            _input = NumberInput(parent,
                                 parameter.get_current_value(),
                                 min=template.get_min_value(),
                                 max=template.get_max_value())
            
        elif _type is Integer:
            # Number inputs :
            if template.has_flag(ParameterFlag.DROPDOWN):
                _input = DropdownInput(
                    parent, parameter.get_current_value(),
                    template.get_additional_data("options"))
            else:
                _input = IntegerInput(parent,
                                      parameter.get_current_value(),
                                      min=template.get_min_value(),
                                      max=template.get_max_value())
        
        if _input is None:
            return None
        
        _input.value_changed.connect(
            cls._create_update_function(parameter, sequence_id, layer_id))
        return _input
    
    @classmethod
    def _create_update_function(cls,
                                parameter: Parameter,
                                sequence_id: int,
                                layer_id: int):
        """Create the update function for a parameter."""
        return lambda value: cls._update_parameter_value(
            parameter, value, sequence_id, layer_id)
    
    @staticmethod
    def _update_parameter_value(parameter: Parameter,
                                value: DataType,
                                sequence_id: int,
                                layer_id: int):
        """Update a parameter value."""
        parameter.set_current_value(value)
        ModifierGUIService.update_parameter_signal.emit(sequence_id, layer_id)
    
    @classmethod
    def set_focused_parameter(cls, parameter: Parameter, sequence_id: int):
        """Set the currently focused parameter for keyframe operations."""
        cls._focused_parameter = parameter
        cls._focused_sequence_id = sequence_id
    
    @classmethod
    def set_current_frame(cls, frame: int):
        """Set the current frame for keyframe operations."""
        cls._current_frame = frame
    
    @classmethod
    def add_keyframe_to_focused_parameter(cls):
        """Add a keyframe to the currently focused parameter at current frame."""
        if cls._focused_parameter is None:
            QMessageBox.information(
                None, 
                "No Parameter Selected", 
                "Please click on a parameter input field first, then press 'K' to add a keyframe."
            )
            return
        
        try:
            from core.services.animation_service import AnimationService
            from core.entities.keyframe import Keyframe
            from gui.services.sequence_gui_service import SequenceGUIService
            
            # Get current frame
            current_frame = cls._current_frame
            
            # Get current parameter value
            current_value = cls._focused_parameter.get_current_value()
            
            # Create and add keyframe
            keyframe = Keyframe(current_frame, current_value)
            AnimationService.add_keyframe(cls._focused_parameter, keyframe)
            
            QMessageBox.information(
                None,
                "Keyframe Added",
                f"Keyframe added at frame {current_frame}"
            )
            
            # Update the display
            if cls._focused_sequence_id is not None:
                ModifierGUIService.update_parameter_signal.emit(cls._focused_sequence_id, 0)
                
        except Exception as e:
            QMessageBox.critical(
                None,
                "Error Adding Keyframe",
                f"Failed to add keyframe: {str(e)}"
            )