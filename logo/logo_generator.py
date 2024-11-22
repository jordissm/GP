import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Create figure and 3D axis
fig = plt.figure(figsize=(5, 5), dpi=300)
ax = fig.add_subplot(111, projection='3d')
ax.view_init(elev=0, azim=-90)  # Set a horizontal view angle
background_color = (16./256, 18./256, 22./256)
fig.set_facecolor(background_color)
ax.set_facecolor(background_color)

# Generate sphere data
def generate_sphere(u_points=300, v_points=300):
    u = np.linspace(0, 2 * np.pi, u_points)
    v = np.linspace(0, np.pi, v_points)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))
    return x, y, z

x, y, z = generate_sphere()

# Plot spheres with different opacities
opacities = [0.175, 0.325, 0.55, 0.775, 1.0]
magnification = 1
separation = 3
sphere_color = 'r'

for i, opacity in enumerate(opacities):
    ax.plot_surface(magnification * opacity * x + i * separation,
                    magnification * opacity * y,
                    magnification * opacity * z,
                    color=sphere_color,
                    alpha=opacity,
                    rstride=5,
                    cstride=5,
                    linewidth=0,
                    edgecolor='none')

# Add arrow at the bottom with label 'Time'
ax.quiver(0, 0, -1.75, 12, 0, 0, color='white', arrow_length_ratio=0.05)
ax.text(6, 0, -2.8, r'${\displaystyle \text{Time}}$', fontsize=16, color='white', ha='center')

# Set axis limits
ax.set_xlim([-1, 13])
ax.set_ylim([-1.2, 1.2])
ax.set_zlim([-1.2, 1.2])

# Set aspect ratio
ax.set_box_aspect([5.5, 1, 1])

# Hide axes for better visual clarity
ax.axis('off')

# Save plot as an image file
plt.tight_layout()
plt.savefig('logo.png', transparent=False, bbox_inches = matplotlib.transforms.Bbox.from_extents(0.2,1.4,5.0,3), pad_inches=0)

# Display message for successful save
print("Plot saved as 'logo.png'")


