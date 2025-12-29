#!/usr/bin/env python3
"""
Generate Performance Comparison Charts for ANPR Detector Models
Creates PNG charts for documentation
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Set style
plt.style.use('seaborn-v0_8-darkgrid')

# Model data from 33% validation test
models = {
    # 320p models
    'micro_320p_fp32': {'detection': 97.13, 'fps': 128, 'size': 83, 'type': '320p FP32'},
    'micro_320p_fp16': {'detection': 97.13, 'fps': 56, 'size': 42, 'type': '320p FP16'},
    'small_320p_fp32': {'detection': 98.00, 'fps': 142, 'size': 114, 'type': '320p FP32'},
    'medium_320p_fp32': {'detection': 98.06, 'fps': 136, 'size': 153, 'type': '320p FP32'},
    'large_320p_fp32': {'detection': 98.40, 'fps': 131, 'size': 164, 'type': '320p FP32'},
    'pico_320p_fp32': {'detection': 96.02, 'fps': 129, 'size': 75, 'type': '320p FP32'},
    
    # 640p models
    'micro_640p_fp32': {'detection': 98.99, 'fps': 68, 'size': 83, 'type': '640p FP32'},
    'pico_640p_fp32': {'detection': 98.54, 'fps': 66, 'size': 75, 'type': '640p FP32'},
    'small_640p_fp32': {'detection': 99.15, 'fps': 70, 'size': 114, 'type': '640p FP32'},
    'medium_640p_fp32': {'detection': 99.21, 'fps': 66, 'size': 153, 'type': '640p FP32'},
    'large_640p_fp32': {'detection': 99.31, 'fps': 60, 'size': 164, 'type': '640p FP32'},
}

# Create output directory
output_dir = Path(__file__).parent / 'images'
output_dir.mkdir(exist_ok=True)

# Chart 1: Speed vs Detection Rate (Scatter Plot)
fig, ax = plt.subplots(figsize=(12, 8))

for model_name, data in models.items():
    color = '#2196F3' if '320p_fp16' in model_name else '#4CAF50' if '320p' in model_name else '#FF9800'
    size_scale = data['size'] * 3
    marker = 'o' if 'fp32' in model_name else '^'
    
    ax.scatter(data['fps'], data['detection'], s=size_scale, alpha=0.6, 
              c=color, marker=marker, edgecolors='black', linewidth=1.5)
    
    # Annotate key models
    if model_name in ['micro_320p_fp32', 'micro_320p_fp16', 'micro_640p_fp32', 'small_320p_fp32']:
        label = model_name.replace('_', '\n')
        ax.annotate(label, (data['fps'], data['detection']), 
                   textcoords="offset points", xytext=(0,10), ha='center',
                   fontsize=8, weight='bold')

ax.set_xlabel('Speed (FPS)', fontsize=14, weight='bold')
ax.set_ylabel('Detection Rate (%)', fontsize=14, weight='bold')
ax.set_title('RT-DETR Detector Models: Speed vs Detection Rate\n(RTX 4090, 33% validation)', 
            fontsize=16, weight='bold', pad=20)
ax.grid(True, alpha=0.3)
ax.set_ylim(95, 100)

# Legend
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='320p FP32 (Fast)', 
           markerfacecolor='#4CAF50', markersize=10),
    Line2D([0], [0], marker='^', color='w', label='320p FP16 (Mobile)', 
           markerfacecolor='#2196F3', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='640p FP32 (High Detection)', 
           markerfacecolor='#FF9800', markersize=10),
]
ax.legend(handles=legend_elements, loc='lower left', fontsize=11)

# Add text annotations
ax.text(0.98, 0.02, 'Bubble size = Model size (MB)', 
        transform=ax.transAxes, ha='right', va='bottom',
        fontsize=10, style='italic', alpha=0.7)

plt.tight_layout()
plt.savefig(output_dir / 'detector_performance_comparison.png', dpi=150, bbox_inches='tight')
print(f'✅ Created: {output_dir / "detector_performance_comparison.png"}')
plt.close()

# Chart 2: Model Comparison Bar Chart
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Top 7 models by different metrics
top_models = ['micro_320p_fp32', 'micro_320p_fp16', 'small_320p_fp32', 
              'micro_640p_fp32', 'pico_320p_fp32', 'small_640p_fp32', 'large_640p_fp32']

model_names = [m.replace('_', '\n') for m in top_models]
detection_rates = [models[m]['detection'] for m in top_models]
fps_values = [models[m]['fps'] for m in top_models]

colors = ['#4CAF50' if '320p_fp32' in m else '#2196F3' if '320p_fp16' in m else '#FF9800' 
          for m in top_models]

# Detection Rate
bars1 = ax1.barh(model_names, detection_rates, color=colors, alpha=0.7, edgecolor='black')
ax1.set_xlabel('Detection Rate (%)', fontsize=12, weight='bold')
ax1.set_title('Detection Rate Comparison', fontsize=14, weight='bold')
ax1.set_xlim(95, 100)
ax1.grid(axis='x', alpha=0.3)

# Add value labels
for i, (bar, val) in enumerate(zip(bars1, detection_rates)):
    ax1.text(val + 0.1, bar.get_y() + bar.get_height()/2, f'{val:.2f}%',
            va='center', fontsize=10, weight='bold')

# Speed (FPS)
bars2 = ax2.barh(model_names, fps_values, color=colors, alpha=0.7, edgecolor='black')
ax2.set_xlabel('Speed (FPS)', fontsize=12, weight='bold')
ax2.set_title('Speed Comparison', fontsize=14, weight='bold')
ax2.grid(axis='x', alpha=0.3)

# Add value labels
for i, (bar, val) in enumerate(zip(bars2, fps_values)):
    ax2.text(val + 2, bar.get_y() + bar.get_height()/2, f'{val} FPS',
            va='center', fontsize=10, weight='bold')

plt.suptitle('MareArts RT-DETR Detector Performance', fontsize=16, weight='bold', y=1.02)
plt.tight_layout()
plt.savefig(output_dir / 'detector_comparison_bars.png', dpi=150, bbox_inches='tight')
print(f'✅ Created: {output_dir / "detector_comparison_bars.png"}')
plt.close()

print('\n✅ All charts generated!')
print(f'📁 Location: {output_dir}/')
print('\nNext: Add to models.md:')
print('  ![Performance Comparison](images/detector_performance_comparison.png)')

