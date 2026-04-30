import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── Your table data ──────────────────────────────────────────────
classes    = ['Normal', 'Attack']
precision  = [0.93, 0.90]
recall     = [0.87, 0.95]
f1_score   = [0.90, 0.92]

# ── Layout ───────────────────────────────────────────────────────
x      = np.arange(len(classes))   # [0, 1]
width  = 0.25                       # width of each bar

fig, ax = plt.subplots(figsize=(7, 5))

bars1 = ax.bar(x - width,     precision, width, label='Precision', color='#3266AD', zorder=3)
bars2 = ax.bar(x,             recall,    width, label='Recall',    color='#E07B3A', zorder=3)
bars3 = ax.bar(x + width,     f1_score,  width, label='F1-Score',  color='#3B9A6C', zorder=3)

# ── Annotate bars with values ─────────────────────────────────────
for bars in [bars1, bars2, bars3]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f'{height:.2f}',
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 4), textcoords='offset points',
            ha='center', va='bottom', fontsize=9
        )

# ── Formatting ────────────────────────────────────────────────────
ax.set_xlabel('Class', fontsize=12)
ax.set_ylabel('Score', fontsize=12)
ax.set_title(
    'Random Forest Classification Results on UNSW-NB15 Test Set',
    fontsize=12, fontweight='bold', pad=12
)
ax.set_xticks(x)
ax.set_xticklabels(classes, fontsize=11)
ax.set_ylim(0.80, 1.02)
ax.set_yticks(np.arange(0.80, 1.02, 0.02))
ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%.2f'))
ax.legend(fontsize=10)
ax.grid(axis='y', linestyle='--', alpha=0.4, zorder=0)
ax.spines[['top', 'right']].set_visible(False)

fig.tight_layout()

# ── Save ──────────────────────────────────────────────────────────
fig.savefig('rf_unswnb15_results.pdf', dpi=300, bbox_inches='tight')   # for LaTeX
fig.savefig('rf_unswnb15_results.png', dpi=300, bbox_inches='tight')   # for Word/preview
plt.show()