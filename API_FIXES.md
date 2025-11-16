# SciMotion API Corrections

This document lists all the API method name corrections made to align with the actual SciMotion codebase architecture.

## Core Architecture Patterns

### Project Class
- **Type**: Static/Singleton class (not instance-based)
- **Usage**: `Project.get_sequences()`, `Project.set_title()`, etc.
- **Note**: No instantiation needed, all methods are class methods

### Data Types
- **All numeric values must be wrapped**: `Integer(1920)`, `Number(0.5)`, `Vector2(960, 540)`, `Color(0, 0, 0, 1)`
- **Serialization**: All data types have `to_dict()` and `from_dict()` methods

### Parameter Access
- **Pattern**: Index-based, not name-based
- **Correct**: `modifier.get_parameter_list()[0]` or `modifier.get_parameter("0")`
- **Incorrect**: `modifier.get_parameter("center")` ❌

## Method Name Corrections

### ModifierRepository → ModifierService
```python
# ❌ Wrong
ModifierRepository.load_from_directory()

# ✓ Correct
ModifierService.load_modifiers_from_directory()
```

### Modifier Creation
```python
# ❌ Wrong
ModifierService.create_modifier(template)

# ✓ Correct
ModifierService.modifier_from_template(template_id)
```

### Adding Modifiers to Layers
```python
# ❌ Wrong
layer.add_modifier(modifier)

# ✓ Correct
ModifierService.add_modifier_to_layer(modifier, layer)
```

### Keyframe Operations
```python
# ❌ Wrong
LayerService.set_keyframe(param, time, value)

# ✓ Correct
from core.entities.keyframe import Keyframe
from core.services.animation_service import AnimationService
AnimationService.add_keyframe(param, Keyframe(frame, value))
```

### Sequence Methods
```python
# ❌ Wrong
sequence.get_layers()

# ✓ Correct
sequence.get_layer_list()
```

### Layer Methods
```python
# ❌ Wrong
layer.get_modifiers()
layer.get_id()
layer.get_color()

# ✓ Correct
layer.get_modifier_list()
# Layer ID is index in list (use enumerate)
layer.get_property("color")
```

### Modifier Methods
```python
# ❌ Wrong
modifier.get_template().get_id()
modifier.is_enabled()
modifier.get_parameters()

# ✓ Correct
modifier.get_template_id()
# No enabled state stored in modifier
modifier.get_parameter_list()
```

### Parameter Methods
```python
# ❌ Wrong
param.get_keyframes()

# ✓ Correct
param.get_keyframe_list()
```

### Keyframe Methods
```python
# ❌ Wrong
keyframe.get_time()

# ✓ Correct
keyframe.get_frame()
```

## Serialization Patterns

### Layer ID
Layers don't have an inherent ID. Use list index:
```python
for layer_index, layer in enumerate(sequence.get_layer_list()):
    layer_data["id"] = layer_index
```

### Parameter ID
Parameters are accessed by index (0, 1, 2...) not by name:
```python
for param_index, param in enumerate(modifier.get_parameter_list()):
    modifier_data["parameters"][str(param_index)] = param_data
```

### Keyframe Data
```python
{
    "frame": kf.get_frame(),  # Not "time"
    "value": value_data,
    "value_type": type(kf_value).__name__
}
```

## Service Responsibilities

- **ModifierService**: Modifier creation, template management, adding to layers
- **AnimationService**: Keyframe operations
- **LayerService**: Layer creation and management
- **ProjectService**: Save/load project files
- **ModifierRepository**: Template storage (read-only access)

## Common Pitfalls

1. **Using plain integers/floats**: Always wrap in `Integer()` or `Number()`
2. **Assuming instance methods exist**: Check if it's a static class first
3. **Using name-based lookups**: Parameters and layers use index-based access
4. **Direct modifier.add()**: Use service methods instead
5. **Inconsistent naming**: `get_X_list()` not `get_Xs()` or `get_X()`

## Files Updated

- `create_blackhole_demo.py`: Demo script using correct API
- `core/services/project_service.py`: Serialization using correct methods
- `core/entities/project.py`: Added missing static methods
- `core/entities/modifier.py`: Added `get_parameter()` helper
