import matplotlib.pyplot as plt

# Timeframe data in hierarchical order
timeframes = ["M1", "W1", "D1", "H4", "H1", "m15", "m5", "m1"]
zint_values = [-1, 1, -1, -1, 0, -1, 1, -1]
zcol_map = {1: "green", 0: "gray", -1: "red"}
zcol_values = [zcol_map[z] for z in zint_values]

# Create the plot
fig, ax = plt.subplots(figsize=(6, 6))
for i, (tf, color) in enumerate(zip(timeframes, zcol_values)):
    ax.scatter(0, -i, s=800, color=color, edgecolors='black', zorder=2)
    ax.text(0, -i, tf, va='center', ha='center', fontsize=12, color='white' if color != "gray" else "black", zorder=3)

# Arrows to indicate trend flow from top (M1) to bottom (m1)
for i in range(len(timeframes) - 1):
    ax.annotate("", xy=(0, -i - 1 + 0.4), xytext=(0, -i - 0.4),
                arrowprops=dict(arrowstyle="->", color='black'))

# Adjust plot
ax.set_xlim(-1, 1)
ax.set_ylim(-len(timeframes), 1)
ax.axis('off')
plt.tight_layout()

# Save to file
output_path = "/mnt/data/trend_stack_diagram.png"
plt.savefig(output_path, bbox_inches='tight')
output_path

