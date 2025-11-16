# -*- coding: utf-8 -*-
"""
Script to programmatically create a black hole animation demo.
Run this to automatically set up a black hole visualization project.
"""

import math
from configparser import ConfigParser

from utils.config import Config
from core.entities.project import Project
from core.entities.sequence import Sequence
from core.entities.solid_layer import SolidLayer
from core.entities.modifier_repository import ModifierRepository
from core.services.modifier_service import ModifierService
from core.services.layer_service import LayerService
from core.services.animation_service import AnimationService
from core.services.project_service import ProjectService
from core.entities.keyframe import Keyframe
from data_types.color import Color
from data_types.number import Number
from data_types.integer import Integer
from data_types.vector2 import Vector2


def create_blackhole_project():
    """Create a black hole animation project."""
    
    print("Loading configuration...")
    # Load config
    _config = ConfigParser()
    _config.read("config.cfg")
    Config.load(_config)
    
    print("Loading modifiers...")
    # Load modifiers
    ModifierService.load_modifiers_from_directory()
    
    print("Creating project...")
    # Create project (reset the static Project class)
    project = ProjectService.create_project("Black Hole Simulation")
    
    # Create sequence (1920x1080, 60fps, 10 seconds)
    print("Creating sequence (1920x1080, 60fps, 10 seconds)...")
    sequence = Sequence(
        title="Black Hole",
        width=1920,
        height=1080,
        frame_rate=60,
        duration=600  # 10 seconds * 60fps
    )
    
    # Add sequence to project
    sequence_id = ProjectService.add_sequence_to_project(sequence)
    
    print("Creating background layer...")
    # Create background layer (Black)
    background = SolidLayer(
        title="Background",
        start_frame=0,
        end_frame=600,
        width=Integer(1920),
        height=Integer(1080),
        color=Color(0, 0, 0, 1)  # Black
    )
    LayerService.add_layer_to_sequence(background, sequence)
    
    print("Creating black hole layer...")
    # Create black hole layer
    blackhole_layer = SolidLayer(
        title="Black Hole",
        start_frame=0,
        end_frame=600,
        width=Integer(1920),
        height=Integer(1080),
        color=Color(1, 1, 1, 1)  # White (will be modified by the black hole effect)
    )
    LayerService.add_layer_to_sequence(blackhole_layer, sequence)
    
    print("Adding black hole modifier...")
    # Add black hole generator modifier
    blackhole_template = ModifierRepository.get_template("black_hole")
    if blackhole_template:
        blackhole_modifier = ModifierService.modifier_from_template("black_hole")
        ModifierService.add_modifier_to_layer(blackhole_modifier, blackhole_layer)
        
        print("Setting up animation for center position (circular motion)...")
        # Set parameters - animate center position in a circle
        params = blackhole_modifier.get_parameter_list()
        # Assuming first parameter is 'center', second is 'radius', third is 'mass'
        # This is based on the typical black_hole modifier structure
        if len(params) >= 1:
            center_param = params[0]  # center parameter
            # Create circular motion around center
            for frame in range(0, 601, 15):  # Every 15 frames for smoother animation
                angle = (frame / 600) * 2 * math.pi
                x = 960 + 300 * math.cos(angle)  # Circle around center
                y = 540 + 300 * math.sin(angle)
                keyframe = Keyframe(frame, Vector2(x, y))
                AnimationService.add_keyframe(center_param, keyframe)
        
        print("Setting up pulsating radius animation...")
        # Set radius with pulsating animation
        if len(params) >= 2:
            radius_param = params[1]  # radius parameter
            AnimationService.add_keyframe(radius_param, Keyframe(0, Number(100)))
            AnimationService.add_keyframe(radius_param, Keyframe(150, Number(250)))
            AnimationService.add_keyframe(radius_param, Keyframe(300, Number(150)))
            AnimationService.add_keyframe(radius_param, Keyframe(450, Number(300)))
            AnimationService.add_keyframe(radius_param, Keyframe(600, Number(100)))
        
        # Set mass (gravitational strength)
        if len(params) >= 3:
            mass_param = params[2]  # mass parameter
            AnimationService.add_keyframe(mass_param, Keyframe(0, Number(1.0)))
            AnimationService.add_keyframe(mass_param, Keyframe(300, Number(1.5)))
            AnimationService.add_keyframe(mass_param, Keyframe(600, Number(1.0)))
    
    print("Adding exposure effect for glow...")
    # Add glow effect (exposure)
    exposure_template = ModifierRepository.get_template("exposure")
    if exposure_template:
        exposure_modifier = ModifierService.modifier_from_template("exposure")
        ModifierService.add_modifier_to_layer(exposure_modifier, blackhole_layer)
        
        params = exposure_modifier.get_parameter_list()
        if len(params) >= 1:
            exposure_param = params[0]  # exposure parameter
            AnimationService.add_keyframe(exposure_param, Keyframe(0, Number(2.0)))
            AnimationService.add_keyframe(exposure_param, Keyframe(300, Number(3.0)))
            AnimationService.add_keyframe(exposure_param, Keyframe(600, Number(2.0)))
    
    print("Adding blur for smooth edges...")
    # Add blur for smooth edges
    blur_template = ModifierRepository.get_template("box_blur")
    if blur_template:
        blur_modifier = ModifierService.modifier_from_template("box_blur")
        ModifierService.add_modifier_to_layer(blur_modifier, blackhole_layer)
        
        params = blur_modifier.get_parameter_list()
        if len(params) >= 1:
            radius_param = params[0]  # blur radius parameter
            AnimationService.add_keyframe(radius_param, Keyframe(0, Number(5.0)))
    
    print("\nSaving project...")
    # Save project
    import os
    save_path = os.path.join(os.path.dirname(__file__), "BlackHole_Demo.smp")
    ProjectService.save_project(project, save_path)
    
    separator = "=" * 60
    print("\n" + separator)
    print("✓ Black hole project created successfully!")
    print(separator)
    print("Project saved to: " + save_path)
    print("\nTo view and render:")
    print("1. Run: python main.py")
    print("2. File → Open Project")
    print("3. Select: BlackHole_Demo.smp")
    print("4. Press Space to preview")
    print("5. File → Export Video to render")
    print(separator + "\n")


if __name__ == "__main__":
    try:
        create_blackhole_project()
    except Exception as e:
        print("\nError creating black hole project: " + str(e))
        import traceback
        traceback.print_exc()
