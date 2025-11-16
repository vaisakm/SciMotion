# Black Hole Simulation Tutorial

## Quick Start: Automated Demo

The easiest way to create a black hole animation is to run the automated demo script:

```bash
python create_blackhole_demo.py
```

This will automatically create a complete black hole project with:
- ✓ Animated black hole moving in a circular path
- ✓ Pulsating radius effect (100 → 300 → 100 pixels)
- ✓ Variable gravitational mass for dynamic distortion
- ✓ Glow effect using exposure modifier
- ✓ Blur for smooth edges
- ✓ 10-second animation at 60fps (600 frames)
- ✓ Full HD resolution (1920x1080)

After running the script, open `BlackHole_Demo.smp` in SciMotion to view and render.

---

## Manual Creation Guide

### Step 1: Launch SciMotion
```bash
python main.py
```

### Step 2: Create New Project
- **Menu**: File → New Project (Ctrl+Shift+N)
- Enter project name: "Black Hole Simulation"

### Step 3: Create Sequence
- **Menu**: Sequence → New Sequence (Ctrl+N)
- **Settings**:
  - Title: "Black Hole"
  - Width: 1920
  - Height: 1080
  - Frame Rate: 60 fps
  - Duration: 600 frames (10 seconds)

### Step 4: Add Background Layer
- **Menu**: Layer → New Solid Layer (Ctrl+Y)
- **Settings**:
  - Title: "Background"
  - Color: Black (R:0, G:0, B:0, A:1)
  - Click OK

### Step 5: Add Black Hole Layer
- **Menu**: Layer → New Solid Layer (Ctrl+Y)
- **Settings**:
  - Title: "Black Hole"
  - Color: White (R:1, G:1, B:1, A:1)
  - Click OK

### Step 6: Add Black Hole Generator
1. In the right panel, find **Modifier Browser**
2. Navigate to **Generators** category
3. Find **Black Hole** modifier
4. Drag it to the "Black Hole" layer or select layer and click Add

### Step 7: Configure Black Hole Modifier Parameters

The Black Hole modifier has these parameters (visible in right panel under "Black hole"):

#### Tilt
- **Description**: Viewing angle of the black hole (0° = face-on, higher = tilted)
- **Default**: 0.0
- **Suggested**: Try values 0.0 to 1.0 for different viewing angles

#### Spin  
- **Description**: Rotation/angular momentum of the black hole
- **Range**: -1.0 to 1.0
- **Default**: 0.0
- **Effect**: Affects accretion disk rotation direction and appearance

#### Inner radius
- **Description**: Inner edge of the accretion disk (event horizon size)
- **Default**: 6.0
- **Suggested**: 3.0 to 10.0
- **Animation**: Can pulse for dynamic effect

#### Outer radius
- **Description**: Outer edge of the accretion disk brightness
- **Default**: 15.0
- **Suggested**: 10.0 to 25.0
- **Animation**: Can expand/contract for breathing effect

### Step 8: Animate Layer Position (Circular Motion)

The black hole **position** is controlled by **layer properties** (bottom right panel), not modifier parameters.

Select the "blackhole" layer in timeline, then in the layer properties panel:

#### Position (Circular Motion)
- **Frame 0**: X=0.500, Y=0.500 (center) → Click value, press `K` to keyframe
- **Frame 150**: X=0.656, Y=0.500 → Press `K`
- **Frame 300**: X=0.500, Y=0.778 → Press `K`  
- **Frame 450**: X=0.344, Y=0.500 → Press `K`
- **Frame 600**: X=0.500, Y=0.500 → Press `K`

> **Note**: Position uses normalized coordinates (0.0 to 1.0), where (0.5, 0.5) is screen center.

### Step 9: Animate Accretion Disk (Optional)

In the "Black hole" modifier panel (top right), animate the disk size:

#### Inner Radius Animation
- **Frame 0**: 6.0 → Press `K`
- **Frame 300**: 4.0 → Press `K`
- **Frame 600**: 6.0 → Press `K`

#### Outer Radius Animation  
- **Frame 0**: 15.0 → Press `K`
- **Frame 300**: 20.0 → Press `K`
- **Frame 600**: 15.0 → Press `K`

### Step 10: Adjust Glow Effect (Already Added)
The demo project already includes:
1. **Exposure** modifier for glow (exposure = 2.0)
2. **Box Blur** modifier for smooth edges (radius = 5.0)

You can adjust these in the Modifiers panel on the right.

### Step 11: Preview
- Press `Space` to play/pause
- Use scroll wheel in viewer to zoom
- Click and drag to pan
- `Home` key: go to start
- `End` key: go to end

### Step 11: Save Project
- **Menu**: File → Save Project As (Ctrl+Shift+S)
- Choose location and filename
- Click Save

### Step 12: Export Video
- **Menu**: File → Export Video (Ctrl+E)
- Choose output location
- Select format (PNG sequence recommended)
- Click Save
- Wait for export to complete

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Shift+N` | New Project |
| `Ctrl+N` | New Sequence |
| `Ctrl+Y` | New Solid Layer |
| `Ctrl+S` | Save Project |
| `Ctrl+Shift+S` | Save Project As |
| `Ctrl+E` | Export Video |
| `Space` | Play/Pause Preview |
| `K` | Add Keyframe |
| `Home` | Go to First Frame |
| `End` | Go to Last Frame |
| `Ctrl+Drag` | Slow Parameter Adjustment |

---

## Black Hole Parameters Explained

### Black Hole Modifier Parameters

#### `tilt` (Number)
- **Description**: Viewing angle of the black hole
- **Range**: 0.0 (face-on) to higher values (tilted view)
- **Default**: 0.0
- **Effect**: Changes perspective of accretion disk
- **Animation Tip**: Slowly tilting creates a 3D rotation effect

#### `spin` (Number)
- **Description**: Angular momentum/rotation of the black hole
- **Range**: -1.0 to 1.0
- **Default**: 0.0
- **Effect**: Affects accretion disk asymmetry and Doppler effects
- **Animation Tip**: Positive = clockwise, Negative = counterclockwise

#### `disc_min` / `Inner radius` (Number)
- **Description**: Inner edge of the accretion disk (event horizon)
- **Range**: 3.0 - 10.0 (recommended)
- **Default**: 6.0
- **Effect**: Size of the dark center (black hole itself)
- **Animation Tip**: Pulsating creates breathing/heartbeat effect

#### `disc_max` / `Outer radius` (Number)
- **Description**: Outer edge of the visible accretion disk
- **Range**: 10.0 - 25.0 (recommended)
- **Default**: 15.0
- **Effect**: Extent of the glowing ring around the black hole
- **Animation Tip**: Expand/contract with inner radius for coherent effect

### Layer Properties (Bottom Right Panel)

#### `Position` (Vector2)
- **Description**: Position of black hole layer on screen
- **Range**: 0.0 to 1.0 (normalized coordinates)
- **Default**: (0.5, 0.5) = center
- **Effect**: Where the black hole appears
- **Animation Tip**: Circular paths or figure-8 motion

#### `Scale` (Vector2)
- **Description**: Size multiplier for the entire black hole
- **Range**: 0.0 to 10.0
- **Default**: (1.0, 1.0)
- **Effect**: Makes black hole bigger/smaller
- **Animation Tip**: Zoom in/out effects

#### `Rotation` (Number)
- **Description**: Rotation angle of the layer
- **Range**: 0.0 to 360.0 degrees
- **Default**: 0.0
- **Effect**: Rotates the entire black hole visual
- **Animation Tip**: Continuous rotation for spinning effect

#### `Opacity` (Number)
- **Description**: Transparency of the layer
- **Range**: 0.0 (invisible) to 1.0 (opaque)
- **Default**: 1.0
- **Effect**: Fade in/out
- **Animation Tip**: Fade in at start, fade out at end

---

## Tips & Tricks

### Performance Optimization
- **Lower Preview Resolution**: Set sequence to 1280x720 for faster preview
- **Reduce Frame Rate**: Use 30fps during testing, 60fps for final render
- **Reduce Max Steps**: In black_hole.py, lower `maxSteps` value (currently 500)

### Visual Enhancements
1. **Increase Spin**: Set spin to 0.8-0.9 for dramatic Doppler shifting
2. **Tilt the View**: Set tilt to 0.5-1.0 to see the disk from an angle
3. **Animate Spin**: Create accelerating/decelerating black hole
4. **Background Stars**: Replace black background with a starfield image
5. **Multiple Black Holes**: Create several layers with different positions
6. **Color the Disk**: The solid layer color affects the accretion disk color!

### Advanced Techniques
- **Accretion Disk**: Add noise + radial gradient layers
- **Event Horizon Glow**: Stack multiple exposure modifiers
- **Hawking Radiation**: Use simple noise with low opacity
- **Gravitational Lensing**: Adjust mass parameter for realistic physics

---

## Troubleshooting

### Black Hole Not Visible
- ✓ Check that layer is above background
- ✓ Verify modifier is enabled (checkbox in modifier list)
- ✓ Ensure radius > 0
- ✓ Check center is within screen bounds

### Performance Issues
- ✓ Reduce sequence resolution
- ✓ Lower frame rate during preview
- ✓ Disable unused modifiers
- ✓ Close other applications

### Export Fails
- ✓ Ensure Pillow is installed: `pip install Pillow`
- ✓ Check disk space for output files
- ✓ Verify write permissions to output folder
- ✓ Try PNG sequence instead of video

### Animation Not Smooth
- ✓ Add more keyframes for complex motion
- ✓ Increase frame rate (60fps recommended)
- ✓ Check interpolation between keyframes

---

## Example Projects

### Minimal Black Hole (Simple)
- 1 Background layer (black)
- 1 Black hole layer with basic parameters
- No animation

### Orbital Black Hole (Medium)
- Background + Black hole
- Circular center animation
- Static radius and mass

### Dynamic Black Hole (Advanced)
- Background + Black hole + Effects
- Animated center, radius, and mass
- Exposure + Blur modifiers
- Custom colors and gradients

### Binary Black Holes (Expert)
- 2 Black hole layers
- Opposite orbital paths
- Variable masses
- Complex interaction effects

---

## Physics Background

The black hole modifier simulates **gravitational lensing** - the bending of light around massive objects. The implementation uses simplified physics for artistic effect:

1. **Event Horizon**: The `radius` parameter approximates the Schwarzschild radius
2. **Gravitational Field**: `mass` controls field strength
3. **Light Bending**: Rays are deflected based on distance from center
4. **Singularity**: Center point represents the mathematical singularity

For realistic astrophysical simulations, additional parameters and ray-tracing would be needed.

---

## Next Steps

1. **Experiment**: Try different parameter values and animations
2. **Combine Effects**: Layer multiple modifiers for complex visuals
3. **Share**: Export your creation and share with the community
4. **Learn More**: Explore other modifiers (noise, gradients, color correction)
5. **Create Original**: Design your own unique black hole animation

Happy animating! 🌌
