"""
Service concerning the project in general.

The ProjectService class defines services within the core
package, concerning the project. This includes adding new
sequences to the project, changing parameters...
"""

import json
from typing import Optional

from core.entities.project import Project
from core.entities.sequence import Sequence
from core.entities.solid_layer import SolidLayer
from core.entities.visual_layer import VisualLayer
from core.entities.modifier import Modifier
from core.entities.modifier_repository import ModifierRepository
from data_types.color import Color
from data_types.integer import Integer


class ProjectService:
    """Service concerning the project in general."""

    @staticmethod
    def add_sequence_to_project(sequence: Sequence) -> int:
        """Add a Sequence to a Project."""
        _sequence_id = Project.get_next_sequence_id()
        _sequence_dict = Project.get_sequence_dict()
        _sequence_dict[_sequence_id] = sequence
        return _sequence_id
    
    @staticmethod
    def get_sequence_by_id(sequence_id: int) -> Sequence:
        """Get a sequence from its id in the project."""
        _sequence_dict = Project.get_sequence_dict()
        if sequence_id not in _sequence_dict:
            return None
        _sequence = _sequence_dict[sequence_id]
        return _sequence
    
    @staticmethod
    def create_project(title: str = "Untitled Project") -> Project:
        """Create a new empty project."""
        Project.reset()
        Project.set_title(title)
        return Project
    
    @staticmethod
    def save_project(project: Project, file_path: str):
        """Save project to file."""
        project_data = {
            "title": Project.get_title(),
            "sequences": {}
        }
        
        # Serialize sequences from the static sequence dict
        _sequence_dict = Project.get_sequence_dict()
        for sequence_id, sequence in _sequence_dict.items():
            sequence_data = {
                "id": sequence_id,
                "title": sequence.get_title(),
                "width": sequence.get_width(),
                "height": sequence.get_height(),
                "frame_rate": sequence.get_frame_rate(),
                "duration": sequence.get_duration(),
                "layers": []
            }
            
            # Serialize layers
            for layer_id, layer in enumerate(sequence.get_layer_list()):
                layer_data = {
                    "id": layer_id,
                    "title": layer.get_title(),
                    "type": layer.__class__.__name__,
                    "modifiers": []
                }
                
                # Add layer-specific data
                if isinstance(layer, SolidLayer):
                    color = layer.get_property("color")
                    width = layer.get_property("width")
                    height = layer.get_property("height")
                    layer_data["color"] = color.to_dict() if color else None
                    layer_data["width"] = width.to_dict() if width and hasattr(width, 'to_dict') else None
                    layer_data["height"] = height.to_dict() if height and hasattr(height, 'to_dict') else None
                    layer_data["start_frame"] = layer.get_start_frame()
                    layer_data["end_frame"] = layer.get_end_frame()
                elif isinstance(layer, VisualLayer):
                    layer_data["file_path"] = layer.get_file_path() if hasattr(layer, 'get_file_path') else None
                    layer_data["start_frame"] = layer.get_start_frame()
                    layer_data["end_frame"] = layer.get_end_frame()
                
                # Serialize modifiers
                for modifier in layer.get_modifier_list():
                    modifier_data = {
                        "template_id": modifier.get_template_id(),
                        "enabled": True,  # Modifiers don't have is_enabled in this version
                        "parameters": {}
                    }
                    
                    # Serialize parameters with keyframes
                    for param_index, param in enumerate(modifier.get_parameter_list()):
                        param_data = {
                            "keyframes": []
                        }
                        for kf in param.get_keyframe_list():
                            kf_value = kf.get_value()
                            # Check if value has to_dict method
                            if hasattr(kf_value, 'to_dict'):
                                value_data = kf_value.to_dict()
                            else:
                                value_data = str(kf_value)
                            
                            param_data["keyframes"].append({
                                "frame": kf.get_frame(),
                                "value": value_data,
                                "value_type": type(kf_value).__name__
                            })
                        modifier_data["parameters"][str(param_index)] = param_data
                    
                    layer_data["modifiers"].append(modifier_data)
                
                sequence_data["layers"].append(layer_data)
            
            project_data["sequences"][str(sequence_id)] = sequence_data
        
        # Write to file
        with open(file_path, 'w') as f:
            json.dump(project_data, f, indent=2)
    
    @staticmethod
    def load_project(file_path: str) -> Project:
        """Load project from file."""
        with open(file_path, 'r') as f:
            project_data = json.load(f)
        
        # Reset and set title
        Project.reset()
        Project.set_title(project_data.get("title", "Untitled"))
        
        # Load modifier repository if not already loaded
        if not ModifierRepository.get_repository():
            ModifierService.load_modifiers_from_directory()
        
        # Deserialize sequences
        sequences_data = project_data.get("sequences", {})
        for seq_id_str, seq_data in sequences_data.items():
            sequence = Sequence(
                title=seq_data.get("title", "Untitled Sequence"),
                width=seq_data.get("width", 1920),
                height=seq_data.get("height", 1080),
                frame_rate=seq_data.get("frame_rate", 60),
                duration=seq_data.get("duration", 600)
            )
            
            # Deserialize layers
            for layer_data in seq_data.get("layers", []):
                layer = None
                layer_type = layer_data.get("type")
                
                if layer_type == "SolidLayer":
                    color_data = layer_data.get("color", {"r": 1, "g": 1, "b": 1, "a": 1})
                    color = Color.from_dict(color_data) if hasattr(Color, 'from_dict') else Color(
                        color_data.get("r", 1),
                        color_data.get("g", 1),
                        color_data.get("b", 1),
                        color_data.get("a", 1)
                    )
                    
                    # Get width and height
                    width_data = layer_data.get("width")
                    height_data = layer_data.get("height")
                    width = Integer.from_dict(width_data) if width_data and hasattr(Integer, 'from_dict') else Integer(1920)
                    height = Integer.from_dict(height_data) if height_data and hasattr(Integer, 'from_dict') else Integer(1080)
                    
                    layer = SolidLayer(
                        title=layer_data.get("title", "Solid Layer"),
                        start_frame=layer_data.get("start_frame", 0),
                        end_frame=layer_data.get("end_frame", 600),
                        width=width,
                        height=height,
                        color=color
                    )
                elif layer_type == "VisualLayer":
                    layer = VisualLayer(
                        title=layer_data.get("title", "Visual Layer"),
                        start_frame=layer_data.get("start_frame", 0),
                        end_frame=layer_data.get("end_frame", 600)
                    )
                
                if layer:
                    # Deserialize modifiers
                    for mod_data in layer_data.get("modifiers", []):
                        template_id = mod_data.get("template_id")
                        template = ModifierRepository.get_template(template_id)
                        
                        if template:
                            from core.services.modifier_service import ModifierService
                            modifier = ModifierService.modifier_from_template(template_id)
                            # Note: enabled state not stored in modifier object
                            
                            # Deserialize parameters and keyframes
                            params_data = mod_data.get("parameters", {})
                            for param_id, param_data in params_data.items():
                                param = modifier.get_parameter(param_id)
                                if param:
                                    # Clear existing keyframes
                                    param.get_keyframe_list().clear()
                                    
                                    # Add keyframes from data
                                    for kf_data in param_data.get("keyframes", []):
                                        frame = kf_data.get("frame", 0)
                                        value_data = kf_data.get("value")
                                        value_type = kf_data.get("value_type", "Number")
                                        
                                        # Reconstruct value from data
                                        value = ProjectService._reconstruct_value(value_data, value_type)
                                        
                                        if value is not None:
                                            from core.services.animation_service import AnimationService
                                            from core.entities.keyframe import Keyframe
                                            keyframe = Keyframe(frame, value)
                                            AnimationService.add_keyframe(param, keyframe)
                            
                            ModifierService.add_modifier_to_layer(modifier, layer)
                    
                    from core.services.layer_service import LayerService
                    LayerService.add_layer_to_sequence(layer, sequence)
            
            # Add sequence to project's static dict
            sequence_id = int(seq_id_str)
            Project.get_sequence_dict()[sequence_id] = sequence
            Project._next_sequence_id = max(Project._next_sequence_id, sequence_id + 1)
        
        return Project
    
    @staticmethod
    def _reconstruct_value(value_data, value_type: str):
        """Reconstruct a value object from serialized data."""
        from data_types.number import Number
        from data_types.integer import Integer
        from data_types.vector2 import Vector2
        from data_types.vector3 import Vector3
        from data_types.color import Color
        from data_types.boolean import Boolean
        
        if value_type == "Number":
            if isinstance(value_data, dict):
                return Number.from_dict(value_data) if hasattr(Number, 'from_dict') else Number(value_data.get("value", 0))
            return Number(float(value_data))
        elif value_type == "Integer":
            if isinstance(value_data, dict):
                return Integer.from_dict(value_data) if hasattr(Integer, 'from_dict') else Integer(value_data.get("value", 0))
            return Integer(int(value_data))
        elif value_type == "Vector2":
            if isinstance(value_data, dict):
                return Vector2.from_dict(value_data) if hasattr(Vector2, 'from_dict') else Vector2(
                    value_data.get("x", 0),
                    value_data.get("y", 0)
                )
        elif value_type == "Vector3":
            if isinstance(value_data, dict):
                return Vector3.from_dict(value_data) if hasattr(Vector3, 'from_dict') else Vector3(
                    value_data.get("x", 0),
                    value_data.get("y", 0),
                    value_data.get("z", 0)
                )
        elif value_type == "Color":
            if isinstance(value_data, dict):
                return Color.from_dict(value_data) if hasattr(Color, 'from_dict') else Color(
                    value_data.get("r", 0),
                    value_data.get("g", 0),
                    value_data.get("b", 0),
                    value_data.get("a", 1)
                )
        elif value_type == "Boolean":
            if isinstance(value_data, dict):
                return Boolean.from_dict(value_data) if hasattr(Boolean, 'from_dict') else Boolean(value_data.get("value", False))
            return Boolean(bool(value_data))
        
        return None