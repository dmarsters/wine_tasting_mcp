# Wine Tasting Visual Vocabulary MCP Server

An epistemological infrastructure system that translates oenological expertise into visual parameters for AI image generation.

## Overview

This MCP server implements a three-layer olog (ontology log) architecture that maps wine tasting vocabulary to visual parameters through category theory. Expert wine tasters work in their native sensory vocabulary (acidity, tannin, terroir, finish length) while the system deterministically transforms these into compositional visual attributes.

## Categorical Structure

The server implements functors and natural transformations across five primary domains:

1. **Varietal Character** (base functor) - Grape variety characteristics
2. **Terroir/Climate** (environmental modifier) - Growing conditions
3. **Winemaking Technique** (process overlay) - Oak treatment, style
4. **Temporal Evolution** (aging dimension) - How wine changes over time
5. **Balance Relationships** (coherence constraints) - Equilibrium between elements

## Installation

```bash
# Local development
cd wine_tasting_mcp
pip install -e .

# For Claude Desktop
# Add to claude_desktop_config.json:
{
  "mcpServers": {
    "wine-tasting": {
      "command": "python",
      "args": ["/path/to/wine_tasting_mcp/server.py"]
    }
  }
}
```

## FastMCP Cloud Deployment

```bash
# Deploy to FastMCP Cloud
fastmcp deploy wine_tasting_mcp

# The server will be available at:
# https://[your-deployment].fastmcp.app/mcp
```

## Supported Varietals

### Red Wines
- **Pinot Noir** - Delicate, translucent, silky texture
- **Cabernet Sauvignon** - Bold, opaque, structured
- **Merlot** - Plush, velvety, approachable
- **Syrah/Shiraz** - Dense, smoky, powerful
- **Nebbiolo** - Austere, chalky, aristocratic
- **Grenache** - Warm, generous, soft
- **Sangiovese** - Bright, savory, firm
- **Tempranillo** - Medium-bodied, leather, vanilla
- **Malbec** - Dense, dark fruit, plush
- **Zinfandel** - Bold, jammy, high alcohol

### White Wines
- **Chardonnay** - Rich, creamy, full-bodied
- **Sauvignon Blanc** - Crisp, electric, angular
- **Riesling** - Crystalline, precise, brilliant
- **Pinot Grigio** - Light, clean, refreshing
- **Chenin Blanc** - Versatile, honeyed, waxy
- **Gewürztraminer** - Perfumed, exotic, spicy
- **Viognier** - Viscous, aromatic, voluptuous
- **Albariño** - Coastal, saline, zesty

## Tool Usage

### 1. Generate Wine Visual Vocabulary

Primary morphism that composes all categorical structures:

```python
# Classic Burgundy Pinot Noir
result = generate_wine_visual_vocabulary(
    varietal="pinot_noir",
    climate="cool",
    winemaking_style="old_world",
    oak_treatment="french_oak",
    age="developing",
    acidity=7.5,
    tannin=6.0,
    sweetness=2.0,
    alcohol=6.5,
    body=5.5,
    finish_length="long",
    primary_aromas=["cherry", "mushroom", "rose"]
)

# Bold Napa Cabernet
result = generate_wine_visual_vocabulary(
    varietal="cabernet_sauvignon",
    climate="warm",
    winemaking_style="new_world",
    oak_treatment="american_oak",
    age="youthful",
    acidity=5.5,
    tannin=8.5,
    sweetness=2.5,
    alcohol=8.5,
    body=9.0,
    finish_length="very_long",
    primary_aromas=["blackcurrant", "vanilla", "cedar"]
)

# Crisp Mosel Riesling
result = generate_wine_visual_vocabulary(
    varietal="riesling",
    climate="cool",
    winemaking_style="old_world",
    oak_treatment="none",
    age="youthful",
    acidity=9.0,
    tannin=0.0,
    sweetness=4.0,
    alcohol=4.5,
    body=4.0,
    finish_length="long",
    primary_aromas=["lime", "slate", "petrol"]
)
```

### 2. Regional Presets

Pre-configured parameters for classic wine regions:

```python
# Burgundy Red (Pinot Noir)
result = create_regional_preset("burgundy_red")

# Napa Valley Cabernet
result = create_regional_preset("napa_cabernet")

# Barolo (Nebbiolo)
result = create_regional_preset("barolo")

# Mosel Riesling
result = create_regional_preset("mosel_riesling")

# Available regions:
# - burgundy_red, burgundy_white
# - napa_cabernet
# - rioja_tempranillo
# - mosel_riesling
# - barolo
# - rhone_syrah
# - marlborough_sauvignon
```

### 3. Evolution Sequence

Show how wine transforms visually over time:

```python
result = evolution_sequence(
    varietal="pinot_noir",
    climate="cool",
    winemaking_style="old_world",
    oak_treatment="french_oak",
    acidity=7.5,
    tannin=6.0,
    body=5.5,
    finish_length="long"
)

# Returns visual vocabularies for:
# - youthful (vibrant, primary fruit)
# - developing (integrating, complex)
# - mature (tertiary, silky)
# - past_prime (fading, oxidized)
```

### 4. Compare Wine Profiles

Identify visual contrasts between wines:

```python
result = compare_wine_profiles(
    wine1_params={
        "varietal": "pinot_noir",
        "climate": "cool",
        "winemaking_style": "old_world",
        "age": "mature"
    },
    wine2_params={
        "varietal": "cabernet_sauvignon",
        "climate": "warm",
        "winemaking_style": "new_world",
        "age": "youthful"
    }
)
```

### 5. Get Reference Information

```python
# List all varietals with characteristics
varietals = get_varietal_list()

# Get aroma clusters with color palettes
aromas = get_aroma_clusters()
```

## Parameter Definitions

### Balance Parameters (1-10 scale)

- **Acidity**: 1=flat, 5=balanced, 10=electric sharp
- **Tannin**: 1=soft (reds only), 5=moderate, 10=grippy astringent
- **Sweetness**: 1=bone dry, 5=off-dry, 10=dessert sweet
- **Alcohol**: 1=low (<11%), 5=moderate (12-13%), 10=high (>15%)
- **Body**: 1=light ethereal, 5=medium, 10=full dense

### Climate Types

- **cool** - Angular, bright, mineral, tense
- **moderate** - Balanced, elegant, composed
- **warm** - Soft, ripe, generous, relaxed
- **hot** - Intense, concentrated, heavy

### Oak Treatment

- **none** - Pure, bright, transparent
- **neutral** - Subtle, softened, rounded
- **french_oak** - Silky, refined, vanilla/spice
- **american_oak** - Bold, creamy, coconut/caramel
- **mixed_oak** - Complex, layered, balanced

### Age Categories

- **youthful** - Vibrant, primary fruit, taut structure
- **developing** - Integrating, complex, softening
- **mature** - Tertiary aromas, silky, resolved
- **past_prime** - Fading, oxidized, thin

### Finish Length

- **short** - Brief, fleeting, abrupt
- **medium** - Moderate, sustained, gradual
- **long** - Persistent, lingering, extended
- **very_long** - Endless, complex, evolving

## Visual Vocabulary Output Structure

```python
{
    "base_color": {
        "hue": "#8B2635",
        "description": "ruby translucent",
        "age_modified": "garnet ruby-brick",
        "climate_shift": "lighter brighter"
    },
    
    "opacity_clarity": {
        "base_opacity": 0.6,
        "clarity": "bright clear",
        "visual_weight": "light ethereal transparent"
    },
    
    "texture_surface": {
        "base_texture": "delicate silky",
        "structure": "fine-grained elegant",
        "climate_modifier": "crisp angular tense",
        "oak_overlay": "silky refined spice",
        "age_state": "integrating softening"
    },
    
    "compositional_structure": {
        "base_composition": "nuanced layered intimate",
        "style_aesthetic": "restrained mineral earthy",
        "visual_tension": "medium balanced",
        "integration": "blending harmonizing",
        "edge_quality": "soft diffused"
    },
    
    "atmospheric_qualities": {
        "climate_atmosphere": "cool restrained mineral",
        "style_atmosphere": "cool stone cellar ancient",
        "finish_depth": "deep receding distant",
        "fade_pattern": "slow gradual evolving"
    },
    
    "color_palette": [
        "#8B2635", "#DC143C", "#3E2723", "#CD853F"
    ],
    
    "balance_relationships": {
        "acidity": 7.5,
        "tannin": 6.0,
        "visual_tension": "medium balanced",
        "visual_weight": "light ethereal transparent"
    }
}
```

## Mathematical Foundation

### Functors

- **Varietal Functor**: Maps grape varieties to base visual characteristics
- **Climate Functor**: Transforms characteristics based on growing conditions
- **Oak Functor**: Overlays texture and color from barrel aging
- **Time Functor**: Evolves all parameters along aging dimension

### Natural Transformations

- **Balance Morphism**: Preserves equilibrium relationships across transformations
- **Regional Transformation**: Composes varietal + climate + style consistently
- **Evolution Morphism**: Maintains identity through time while modifying attributes

### Coherence Constraints

Balance dimensions enforce coherent visual relationships:
- High acidity → Angular edges, bright atmosphere
- High tannin → Structured texture, firm composition
- High body → Dense opacity, heavy visual weight
- Long finish → Extended fade, deep atmospheric depth

## Use Cases

### Image Generation

```
"Generate an image with the visual qualities of a mature Burgundy Pinot Noir:
delicate silky texture, ruby-brick translucent color, nuanced layered composition,
cool mineral atmosphere, fine-grained elegant structure"
```

### Comparative Visualization

```
"Show the visual contrast between youthful Napa Cabernet (opaque, bold, geometric)
and mature Burgundy Pinot (translucent, delicate, nuanced)"
```

### Temporal Sequence

```
"Create a series showing wine evolution: vibrant purple youthful → 
garnet developing → brick mature → brown fading"
```

## Expert Validation

The vocabulary is grounded in:
- **Court of Master Sommeliers** standardized tasting grid
- **WSET** (Wine & Spirit Education Trust) systematic approach
- **UC Davis Aroma Wheel** scientific categorization
- Classical wine regions and established quality standards

## Intentionality Reasoning

Why these mappings work:

1. **Color progression is real** - Wine literally changes color with age (purple→brick→brown)
2. **Texture vocabulary is synesthetic** - "Silky" vs "grippy" naturally suggests visual texture
3. **Structural metaphors are embodied** - "Angular" acid vs "soft" roundness
4. **Balance is visual equilibrium** - Tension/relaxation maps to composition
5. **Finish is temporal decay** - Length maps to atmospheric depth/fade

## Citation

When using this server's visual vocabulary, cite:
- Court of Master Sommeliers tasting methodology
- WSET systematic approach to wine evaluation
- UC Davis Wine Aroma Wheel (A.C. Noble et al.)

## License

MIT License - See LICENSE file for details

## Contributing

This server represents systematized expert knowledge. Contributions should:
1. Ground additions in established wine education frameworks
2. Maintain categorical coherence (morphisms must compose)
3. Include intentionality reasoning (why the mapping works)
4. Validate with wine education professionals

## Author

Part of the Lushy epistemological infrastructure project by Dal.
Translating domain expertise into visual parameters through category theory.
