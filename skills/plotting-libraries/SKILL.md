---
name: plotting-libraries
description: "Python plotting libraries for data visualization. Decision framework for matplotlib vs seaborn, common patterns, and best practices. Use when creating plots, charts, figures, or visualizations in Python."
---

<objective>
Guide effective use of Python's primary plotting libraries—matplotlib and seaborn—for creating data visualizations. This skill provides decision frameworks for choosing between libraries, common patterns for combining them, and links to detailed reference documentation.
</objective>

<quick_start>
**Choose your library:**

| Use Case | Library | Why |
|----------|---------|-----|
| Full control, custom layouts | matplotlib | Direct access to all elements |
| Statistical plots, DataFrames | seaborn | Built-in aggregation, cleaner API |
| Publication figures | Both | seaborn for quick stats → matplotlib for polish |
| Simple line/scatter/bar | matplotlib | Minimal dependencies |
| Distributions, correlations | seaborn | Automatic stats and styling |

**Quick matplotlib pattern:**
```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x, y, linewidth=2, label='Data')
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.legend()
plt.savefig('figure.png', dpi=300, bbox_inches='tight')
```

**Quick seaborn pattern:**
```python
import seaborn as sns
import matplotlib.pyplot as plt

sns.scatterplot(data=df, x='x_col', y='y_col', hue='category')
plt.savefig('figure.png', dpi=300, bbox_inches='tight')
```
</quick_start>

<decision_framework>
**Start with seaborn when:**
- Working with pandas DataFrames
- Need statistical estimation (means, confidence intervals, regression)
- Creating distribution plots (histplot, kdeplot, violinplot)
- Want faceted/small-multiple layouts quickly
- Exploring data (pairplot, jointplot)

**Start with matplotlib when:**
- Need pixel-level control over layout
- Creating non-standard plot types
- Building complex multi-panel figures with different plot types
- Animating visualizations
- Embedding in GUI applications

**Use both together when:**
- seaborn creates the base plot, matplotlib fine-tunes it
- Need statistical analysis AND custom annotations
- Creating publication-quality figures
</decision_framework>

<common_patterns>
**Combined workflow (most common for publications):**
```python
import seaborn as sns
import matplotlib.pyplot as plt

# seaborn for statistical plot
fig, ax = plt.subplots(figsize=(8, 6))
sns.boxplot(data=df, x='group', y='value', ax=ax)

# matplotlib for customization
ax.set_title('Distribution by Group', fontsize=14, fontweight='bold')
ax.set_xlabel('Experimental Group', fontsize=12)
ax.set_ylabel('Measurement (units)', fontsize=12)

# Add custom elements
ax.axhline(y=threshold, color='red', linestyle='--', label='Threshold')
ax.legend()

plt.tight_layout()
plt.savefig('figure.pdf', dpi=300, bbox_inches='tight')
```

**Multi-panel with mixed plots:**
```python
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Different plot types in each panel
sns.scatterplot(data=df, x='x', y='y', ax=axes[0, 0])
sns.histplot(data=df, x='value', ax=axes[0, 1])
axes[1, 0].plot(time, signal)  # Pure matplotlib
sns.heatmap(correlation_matrix, ax=axes[1, 1])

plt.tight_layout()
```

**Export for publications:**
```python
# Vector format (scalable, required by most journals)
plt.savefig('figure.pdf', bbox_inches='tight')
plt.savefig('figure.svg', bbox_inches='tight')

# Raster format (presentations, web)
plt.savefig('figure.png', dpi=300, bbox_inches='tight')
```
</common_patterns>

<styling_integration>
For scientific figures, coordinate with:

- **[scientific-visualization](../scientific-visualization/SKILL.md)**: Design principles, chart selection, publication requirements
- **[visual-design](../visual-design/SKILL.md)**: Brand colors, typography, consistent aesthetics

**Apply brand colors:**
```python
from your_brand_module import COLORS  # See visual-design skill

# matplotlib
ax.plot(x, y, color=COLORS['primary'])

# seaborn
sns.set_palette([COLORS['primary'], COLORS['secondary'], COLORS['accent']])
```
</styling_integration>

<reference_guides>
For detailed library documentation:

- **[references/matplotlib.md](references/matplotlib.md)**: Complete matplotlib reference—OO API, plot types, subplots, 3D, styling, saving
- **[references/seaborn.md](references/seaborn.md)**: Complete seaborn reference—statistical plots, figure-level vs axes-level, palettes, theming
</reference_guides>

<success_criteria>
- Appropriate library chosen for the task
- Figure renders correctly with all elements visible
- Exported at appropriate resolution (300 DPI for print, 150 for web)
- Labels, legends, and titles are readable
- Color palette is accessible (colorblind-friendly when possible)
</success_criteria>
