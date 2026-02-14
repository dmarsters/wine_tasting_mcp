"""
Wine Tasting Visual Vocabulary MCP Server

Translates oenological expertise into visual parameters for image generation.
Based on systematic wine evaluation methodology from Court of Master Sommeliers
and WSET (Wine & Spirit Education Trust) frameworks.

Categorical Structure:
- Varietal Character (base functor)
- Terroir/Region (environmental modifier)
- Winemaking Technique (process overlay)
- Temporal Evolution (aging dimension)
- Balance Relationships (coherence constraints)
"""

from fastmcp import FastMCP
from typing import Dict, List, Optional, Literal, Any
from dataclasses import dataclass
from enum import Enum
import json
import re
from pathlib import Path
import yaml

# Initialize FastMCP server
mcp = FastMCP("Wine Tasting Visual Vocabulary")

# ============================================================================
# TYPE DEFINITIONS - Categorical Objects
# ============================================================================

class WineType(Enum):
    RED = "red"
    WHITE = "white"
    ROSE = "rosé"
    SPARKLING = "sparkling"
    DESSERT = "dessert"
    FORTIFIED = "fortified"

class Varietal(Enum):
    # Red Varietals
    PINOT_NOIR = "pinot_noir"
    CABERNET_SAUVIGNON = "cabernet_sauvignon"
    MERLOT = "merlot"
    SYRAH = "syrah"
    GRENACHE = "grenache"
    NEBBIOLO = "nebbiolo"
    SANGIOVESE = "sangiovese"
    TEMPRANILLO = "tempranillo"
    MALBEC = "malbec"
    ZINFANDEL = "zinfandel"
    
    # White Varietals
    CHARDONNAY = "chardonnay"
    SAUVIGNON_BLANC = "sauvignon_blanc"
    RIESLING = "riesling"
    PINOT_GRIGIO = "pinot_grigio"
    CHENIN_BLANC = "chenin_blanc"
    GEWURZTRAMINER = "gewurztraminer"
    VIOGNIER = "viognier"
    ALBARINO = "albariño"

class ClimateType(Enum):
    COOL = "cool"
    MODERATE = "moderate"
    WARM = "warm"
    HOT = "hot"

class WinemakingStyle(Enum):
    OLD_WORLD = "old_world"
    NEW_WORLD = "new_world"

class OakTreatment(Enum):
    NONE = "none"
    NEUTRAL = "neutral"
    FRENCH_OAK = "french_oak"
    AMERICAN_OAK = "american_oak"
    MIXED_OAK = "mixed_oak"

class AgeCategory(Enum):
    YOUTHFUL = "youthful"
    DEVELOPING = "developing"
    MATURE = "mature"
    PAST_PRIME = "past_prime"

# ============================================================================
# VARIETAL CHARACTER - Base Functor
# ============================================================================

VARIETAL_CHARACTERISTICS = {
    # Red Varietals
    Varietal.PINOT_NOIR: {
        "color_base": "ruby translucent",
        "color_hue": "#8B2635",
        "opacity": 0.6,
        "texture": "delicate silky",
        "structure": "fine-grained elegant",
        "visual_weight": "light ethereal",
        "characteristic_notes": ["cherry", "mushroom", "forest_floor", "rose_petal"],
        "edge_quality": "soft diffused",
        "composition": "nuanced layered intimate"
    },
    Varietal.CABERNET_SAUVIGNON: {
        "color_base": "deep purple opaque",
        "color_hue": "#2C1810",
        "opacity": 0.95,
        "texture": "structured firm",
        "structure": "bold geometric angular",
        "visual_weight": "full commanding",
        "characteristic_notes": ["blackcurrant", "cedar", "graphite", "tobacco"],
        "edge_quality": "defined precise",
        "composition": "architectural powerful monumental"
    },
    Varietal.MERLOT: {
        "color_base": "ruby garnet",
        "color_hue": "#722F37",
        "opacity": 0.8,
        "texture": "plush velvety",
        "structure": "rounded soft",
        "visual_weight": "medium approachable",
        "characteristic_notes": ["plum", "chocolate", "vanilla", "leather"],
        "edge_quality": "gentle flowing",
        "composition": "harmonious welcoming generous"
    },
    Varietal.SYRAH: {
        "color_base": "inky purple black",
        "color_hue": "#1A0F14",
        "opacity": 0.9,
        "texture": "dense smoky",
        "structure": "wild untamed powerful",
        "visual_weight": "full intense",
        "characteristic_notes": ["blackberry", "smoke", "pepper", "bacon_fat"],
        "edge_quality": "dramatic bold",
        "composition": "primal visceral dynamic"
    },
    Varietal.NEBBIOLO: {
        "color_base": "garnet brick translucent",
        "color_hue": "#9B4F47",
        "opacity": 0.65,
        "texture": "grippy chalky tannic",
        "structure": "austere angular aristocratic",
        "visual_weight": "medium ethereal",
        "characteristic_notes": ["rose", "tar", "truffle", "dried_cherry"],
        "edge_quality": "sharp precise",
        "composition": "noble stern elegant"
    },
    Varietal.GRENACHE: {
        "color_base": "ruby translucent warm",
        "color_hue": "#A52A2A",
        "opacity": 0.7,
        "texture": "soft approachable",
        "structure": "rounded generous friendly",
        "visual_weight": "medium light",
        "characteristic_notes": ["strawberry", "raspberry", "white_pepper", "herbs"],
        "edge_quality": "soft flowing",
        "composition": "warm welcoming open"
    },
    Varietal.SANGIOVESE: {
        "color_base": "ruby bright",
        "color_hue": "#8B0000",
        "opacity": 0.75,
        "texture": "firm savory",
        "structure": "angular structured linear",
        "visual_weight": "medium bright",
        "characteristic_notes": ["cherry", "tomato", "herbs", "earth"],
        "edge_quality": "defined crisp",
        "composition": "savory focused precise"
    },
    Varietal.TEMPRANILLO: {
        "color_base": "ruby garnet",
        "color_hue": "#8B2635",
        "opacity": 0.8,
        "texture": "medium-bodied balanced",
        "structure": "moderate structured",
        "visual_weight": "medium substantial",
        "characteristic_notes": ["cherry", "leather", "tobacco", "vanilla"],
        "edge_quality": "smooth defined",
        "composition": "balanced traditional composed"
    },
    Varietal.MALBEC: {
        "color_base": "deep purple inky",
        "color_hue": "#2C0E3F",
        "opacity": 0.9,
        "texture": "plush dense",
        "structure": "full-bodied powerful",
        "visual_weight": "full dense",
        "characteristic_notes": ["blackberry", "plum", "chocolate", "violet"],
        "edge_quality": "soft deep",
        "composition": "lush opulent powerful"
    },
    Varietal.ZINFANDEL: {
        "color_base": "deep ruby purple",
        "color_hue": "#722F37",
        "opacity": 0.85,
        "texture": "bold jammy",
        "structure": "powerful intense",
        "visual_weight": "full heavy",
        "characteristic_notes": ["blackberry", "jam", "spice", "tobacco"],
        "edge_quality": "bold dramatic",
        "composition": "intense powerful exuberant"
    },
    
    # White Varietals
    Varietal.CHARDONNAY: {
        "color_base": "golden straw",
        "color_hue": "#F4E4C1",
        "opacity": 0.85,
        "texture": "creamy rich",
        "structure": "full-bodied opulent",
        "visual_weight": "medium to full",
        "characteristic_notes": ["apple", "butter", "vanilla", "hazelnut"],
        "edge_quality": "smooth rounded",
        "composition": "luxurious generous expansive"
    },
    Varietal.SAUVIGNON_BLANC: {
        "color_base": "pale straw green-tinged",
        "color_hue": "#F5F5DC",
        "opacity": 0.9,
        "texture": "crisp electric",
        "structure": "lean racy angular",
        "visual_weight": "light precise",
        "characteristic_notes": ["grapefruit", "grass", "gooseberry", "flint"],
        "edge_quality": "sharp cutting",
        "composition": "vibrant energetic focused"
    },
    Varietal.RIESLING: {
        "color_base": "pale yellow crystalline",
        "color_hue": "#FFFACD",
        "opacity": 0.95,
        "texture": "crystalline pure",
        "structure": "taut precise delicate",
        "visual_weight": "light to medium",
        "characteristic_notes": ["lime", "petrol", "honey", "slate"],
        "edge_quality": "razor-sharp brilliant",
        "composition": "luminous transparent exact"
    },
    Varietal.VIOGNIER: {
        "color_base": "deep golden",
        "color_hue": "#FFD700",
        "opacity": 0.8,
        "texture": "viscous oily",
        "structure": "full perfumed exotic",
        "visual_weight": "full voluptuous",
        "characteristic_notes": ["apricot", "honeysuckle", "peach", "ginger"],
        "edge_quality": "soft blurred aromatic",
        "composition": "sensuous heady intoxicating"
    },
    Varietal.PINOT_GRIGIO: {
        "color_base": "pale straw light",
        "color_hue": "#F5F5DC",
        "opacity": 0.9,
        "texture": "light crisp",
        "structure": "simple clean refreshing",
        "visual_weight": "light delicate",
        "characteristic_notes": ["lemon", "apple", "pear", "almond"],
        "edge_quality": "clean sharp",
        "composition": "simple direct refreshing"
    },
    Varietal.CHENIN_BLANC: {
        "color_base": "golden straw",
        "color_hue": "#F4E4C1",
        "opacity": 0.85,
        "texture": "waxy honeyed",
        "structure": "versatile complex",
        "visual_weight": "medium rich",
        "characteristic_notes": ["honey", "quince", "chamomile", "ginger"],
        "edge_quality": "smooth textured",
        "composition": "complex textural layered"
    },
    Varietal.GEWURZTRAMINER: {
        "color_base": "deep golden",
        "color_hue": "#FFD700",
        "opacity": 0.82,
        "texture": "oily perfumed",
        "structure": "exotic aromatic spicy",
        "visual_weight": "medium full",
        "characteristic_notes": ["lychee", "rose", "ginger", "spice"],
        "edge_quality": "aromatic diffused",
        "composition": "exotic perfumed intense"
    },
    Varietal.ALBARINO: {
        "color_base": "pale yellow green-tinged",
        "color_hue": "#FFFACD",
        "opacity": 0.9,
        "texture": "fresh saline",
        "structure": "crisp coastal bright",
        "visual_weight": "light medium",
        "characteristic_notes": ["citrus", "peach", "saline", "minerals"],
        "edge_quality": "bright clean",
        "composition": "fresh coastal vibrant"
    }
}

# ============================================================================
# TERROIR & CLIMATE - Environmental Modifiers
# ============================================================================

CLIMATE_MODIFIERS = {
    ClimateType.COOL: {
        "color_shift": "lighter brighter",
        "saturation_adjust": -0.15,
        "brightness_adjust": 0.1,
        "texture_modifier": "crisp angular tense",
        "atmosphere": "cool restrained mineral",
        "visual_tension": "high precise",
        "edge_treatment": "sharp defined"
    },
    ClimateType.MODERATE: {
        "color_shift": "balanced",
        "saturation_adjust": 0.0,
        "brightness_adjust": 0.0,
        "texture_modifier": "harmonious integrated",
        "atmosphere": "temperate balanced elegant",
        "visual_tension": "medium composed",
        "edge_treatment": "clean refined"
    },
    ClimateType.WARM: {
        "color_shift": "deeper richer",
        "saturation_adjust": 0.1,
        "brightness_adjust": -0.05,
        "texture_modifier": "soft ripe generous",
        "atmosphere": "warm sun-drenched opulent",
        "visual_tension": "low relaxed",
        "edge_treatment": "soft blended"
    },
    ClimateType.HOT: {
        "color_shift": "intense dark",
        "saturation_adjust": 0.2,
        "brightness_adjust": -0.15,
        "texture_modifier": "jammy concentrated thick",
        "atmosphere": "hot intense powerful",
        "visual_tension": "very low heavy",
        "edge_treatment": "blurred diffused"
    }
}

WINEMAKING_STYLE_MODIFIERS = {
    WinemakingStyle.OLD_WORLD: {
        "aesthetic": "restrained mineral earthy",
        "composition": "subtle understated elegant",
        "color_treatment": "muted sophisticated tertiary",
        "detail_level": "fine precise intricate",
        "atmosphere": "cool stone cellar ancient"
    },
    WinemakingStyle.NEW_WORLD: {
        "aesthetic": "fruit-forward bold exuberant",
        "composition": "generous obvious accessible",
        "color_treatment": "vibrant primary saturated",
        "detail_level": "bold clear direct",
        "atmosphere": "sunny modern open"
    }
}

# ============================================================================
# OAK TREATMENT - Process Overlay
# ============================================================================

OAK_CHARACTERISTICS = {
    OakTreatment.NONE: {
        "texture_overlay": "pure clean unadulterated",
        "color_influence": "none",
        "finish_quality": "bright transparent",
        "material_reference": "glass crystal water"
    },
    OakTreatment.NEUTRAL: {
        "texture_overlay": "subtle softened rounded",
        "color_influence": "minimal slight warmth",
        "finish_quality": "smooth integrated",
        "material_reference": "aged_wood smooth_stone"
    },
    OakTreatment.FRENCH_OAK: {
        "texture_overlay": "silky refined spice",
        "color_influence": "golden vanilla subtle toast",
        "finish_quality": "elegant sophisticated polished",
        "material_reference": "fine_wood polished_bronze"
    },
    OakTreatment.AMERICAN_OAK: {
        "texture_overlay": "bold creamy coconut",
        "color_influence": "deep amber vanilla caramel",
        "finish_quality": "rich obvious sweet",
        "material_reference": "charred_wood bourbon_barrel"
    },
    OakTreatment.MIXED_OAK: {
        "texture_overlay": "complex layered spice-sweet",
        "color_influence": "warm amber golden vanilla",
        "finish_quality": "balanced nuanced",
        "material_reference": "varied_wood aged_patina"
    }
}

# ============================================================================
# TEMPORAL EVOLUTION - Aging Dimension
# ============================================================================

AGE_TRANSFORMATIONS = {
    AgeCategory.YOUTHFUL: {
        "color_evolution": "vibrant primary bright",
        "red_color_shift": "purple ruby",
        "white_color_shift": "pale straw green-tinged",
        "aromatic_category": "primary fruit-forward fresh",
        "texture_state": "taut structured firm",
        "integration": "separate distinct angular",
        "visual_clarity": "brilliant star-bright",
        "time_signature": "present immediate vivid"
    },
    AgeCategory.DEVELOPING: {
        "color_evolution": "deepening softening",
        "red_color_shift": "garnet ruby-brick",
        "white_color_shift": "golden straw",
        "aromatic_category": "secondary developing complex",
        "texture_state": "integrating softening",
        "integration": "blending harmonizing",
        "visual_clarity": "bright clear",
        "time_signature": "transitional evolving"
    },
    AgeCategory.MATURE: {
        "color_evolution": "tertiary evolved",
        "red_color_shift": "brick garnet tawny-edge",
        "white_color_shift": "deep-gold amber",
        "aromatic_category": "tertiary developed savory",
        "texture_state": "silky resolved integrated",
        "integration": "seamless unified complete",
        "visual_clarity": "clear luminous",
        "time_signature": "patient wise settled"
    },
    AgeCategory.PAST_PRIME: {
        "color_evolution": "fading oxidized",
        "red_color_shift": "brown tawny brick-brown",
        "white_color_shift": "deep-amber brown-tinged",
        "aromatic_category": "fading oxidized tired",
        "texture_state": "thin drying out",
        "integration": "falling apart disjointed",
        "visual_clarity": "dull fading",
        "time_signature": "past declining fragile"
    }
}

# ============================================================================
# AROMA/FLAVOR CLUSTERS - Palette Generators
# ============================================================================

AROMA_CLUSTERS = {
    "red_fruit": {
        "notes": ["cherry", "raspberry", "strawberry", "cranberry", "red_currant"],
        "color_palette": ["#DC143C", "#C71585", "#FF6B6B", "#E74C3C"],
        "brightness": "bright vivid fresh",
        "texture": "juicy tart crisp"
    },
    "black_fruit": {
        "notes": ["blackberry", "blackcurrant", "black_cherry", "plum", "blueberry"],
        "color_palette": ["#1A0F14", "#2C1810", "#4A0E4E", "#191970"],
        "brightness": "deep dark concentrated",
        "texture": "dense rich powerful"
    },
    "stone_fruit": {
        "notes": ["peach", "apricot", "nectarine", "plum"],
        "color_palette": ["#FFDAB9", "#FFB347", "#FF8C69", "#DDA0DD"],
        "brightness": "warm glowing ripe",
        "texture": "soft luscious velvety"
    },
    "citrus": {
        "notes": ["lemon", "lime", "grapefruit", "orange_zest"],
        "color_palette": ["#FFF44F", "#BFFF00", "#FF6F61", "#FFD700"],
        "brightness": "electric vibrant zesty",
        "texture": "sharp crisp cutting"
    },
    "tropical": {
        "notes": ["pineapple", "mango", "passion_fruit", "lychee", "guava"],
        "color_palette": ["#FFD700", "#FF8C00", "#FF69B4", "#F0E68C"],
        "brightness": "exotic bright heady",
        "texture": "lush voluptuous perfumed"
    },
    "earth_mineral": {
        "notes": ["wet_stone", "slate", "chalk", "graphite", "flint", "petrichor"],
        "color_palette": ["#708090", "#696969", "#A9A9A9", "#2F4F4F"],
        "brightness": "cool muted subtle",
        "texture": "dry stony mineral"
    },
    "forest_floor": {
        "notes": ["mushroom", "truffle", "forest_floor", "damp_leaves", "soil"],
        "color_palette": ["#3E2723", "#5D4037", "#4E342E", "#654321"],
        "brightness": "dark earthy organic",
        "texture": "loamy dense humid"
    },
    "oak_spice": {
        "notes": ["vanilla", "cinnamon", "clove", "nutmeg", "cedar", "toast"],
        "color_palette": ["#D2691E", "#CD853F", "#DEB887", "#8B4513"],
        "brightness": "warm amber golden",
        "texture": "smooth spicy aromatic"
    },
    "leather_tobacco": {
        "notes": ["leather", "tobacco", "cigar_box", "dried_herbs"],
        "color_palette": ["#8B4513", "#654321", "#704214", "#3E2723"],
        "brightness": "aged patinated rich",
        "texture": "supple smooth aged"
    },
    "floral": {
        "notes": ["rose", "violet", "honeysuckle", "jasmine", "orange_blossom"],
        "color_palette": ["#FFB6C1", "#DDA0DD", "#E6E6FA", "#FFF0F5"],
        "brightness": "delicate perfumed aromatic",
        "texture": "soft ethereal fragrant"
    }
}

# ============================================================================
# BALANCE DIMENSIONS - Coherence Constraints
# ============================================================================

@dataclass
class BalanceProfile:
    """Represents the equilibrium relationships in wine"""
    acidity: float  # 1-10 scale
    tannin: float  # 1-10 scale (reds only)
    sweetness: float  # 1-10 scale
    alcohol: float  # 1-10 scale
    body: float  # 1-10 scale
    
    def get_visual_tension(self) -> str:
        """Calculate overall visual tension from balance"""
        acid_tension = self.acidity / 10.0
        tannin_tension = self.tannin / 10.0
        
        # Tension is driven by structural elements (acid + tannin)
        tension_score = (acid_tension + tannin_tension) / 2
        
        if tension_score > 0.65:
            return "high angular taut"
        elif tension_score > 0.45:
            return "medium balanced"
        else:
            return "low soft relaxed"
    
    def get_visual_weight(self) -> str:
        """Calculate visual density from body and alcohol"""
        weight_score = (self.body + self.alcohol) / 20.0
        
        if weight_score > 0.7:
            return "full dense heavy opaque"
        elif weight_score > 0.4:
            return "medium substantial"
        else:
            return "light ethereal transparent"

# ============================================================================
# FINISH DIMENSION - Temporal Decay
# ============================================================================

FINISH_CHARACTERISTICS = {
    "short": {
        "length_descriptor": "brief fleeting",
        "edge_treatment": "abrupt clean",
        "fade_pattern": "rapid quick dissipating",
        "atmospheric_depth": "shallow immediate"
    },
    "medium": {
        "length_descriptor": "moderate sustained",
        "edge_treatment": "gradual smooth",
        "fade_pattern": "steady even balanced",
        "atmospheric_depth": "middle-ground present"
    },
    "long": {
        "length_descriptor": "persistent lingering",
        "edge_treatment": "extended soft",
        "fade_pattern": "slow gradual evolving",
        "atmospheric_depth": "deep receding distant"
    },
    "very_long": {
        "length_descriptor": "endless immortal",
        "edge_treatment": "infinite dissolving",
        "fade_pattern": "complex ever-changing eternal",
        "atmospheric_depth": "vast infinite horizon"
    }
}

# ============================================================================
# MCP TOOLS - Morphisms
# ============================================================================

# Helper function to determine if varietal is red or white
def is_red_varietal(varietal_name: str) -> bool:
    """Determine if a varietal is red or white based on name"""
    red_varietals = {
        "pinot_noir", "cabernet_sauvignon", "merlot", "syrah", "nebbiolo",
        "grenache", "sangiovese", "tempranillo", "malbec", "zinfandel"
    }
    return varietal_name.lower() in red_varietals


# ============================================================================
# TAXONOMY CACHING - Load once at module initialization
# ============================================================================
_TAXONOMY_CACHE = None

def _load_taxonomy() -> Dict[str, Any]:
    """Load taxonomy ONCE and cache it at module level."""
    global _TAXONOMY_CACHE
    if _TAXONOMY_CACHE is None:
        yaml_path = Path(__file__).parent / "wine_tasting_olog.yaml"
        with open(yaml_path, 'r') as f:
            _TAXONOMY_CACHE = yaml.safe_load(f)
    return _TAXONOMY_CACHE

# Pre-load taxonomy on module import
TAXONOMY = _load_taxonomy()


@mcp.tool()
def generate_wine_visual_vocabulary(
    varietal: str,
    climate: str = "moderate",
    winemaking_style: str = "old_world",
    oak_treatment: str = "french_oak",
    age: str = "developing",
    acidity: float = 5.0,
    tannin: float = 5.0,
    sweetness: float = 2.0,
    alcohol: float = 6.0,
    body: float = 6.0,
    finish_length: str = "medium",
    primary_aromas: Optional[List[str]] = None
) -> Dict:
    """
    Generate complete visual vocabulary from wine tasting parameters.
    
    This is the primary morphism that composes all categorical structures
    into a unified visual parameter set for image generation.
    
    Args:
        varietal: Grape variety (e.g., "pinot_noir", "chardonnay")
        climate: Growing climate ("cool", "moderate", "warm", "hot")
        winemaking_style: Production approach ("old_world", "new_world")
        oak_treatment: Oak aging type ("none", "neutral", "french_oak", "american_oak", "mixed_oak")
        age: Wine age category ("youthful", "developing", "mature", "past_prime")
        acidity: Acid level 1-10 (higher = brighter, more angular)
        tannin: Tannin level 1-10 (reds only, higher = more structured)
        sweetness: Sugar level 1-10 (higher = richer, softer)
        alcohol: Alcohol level 1-10 (higher = warmer, fuller)
        body: Body weight 1-10 (higher = denser, heavier)
        finish_length: Persistence ("short", "medium", "long", "very_long")
        primary_aromas: List of dominant aroma descriptors (optional)
    
    Returns:
        Complete visual vocabulary dictionary with all parameters
    """
    
    # Parse enum values
    try:
        varietal_enum = Varietal(varietal.lower())
        climate_enum = ClimateType(climate.lower())
        style_enum = WinemakingStyle(winemaking_style.lower())
        oak_enum = OakTreatment(oak_treatment.lower())
        age_enum = AgeCategory(age.lower())
    except ValueError as e:
        return {"error": f"Invalid parameter value: {e}"}
    
    # Get base varietal characteristics
    varietal_char = VARIETAL_CHARACTERISTICS.get(varietal_enum, {})
    
    # Apply climate modifiers
    climate_mod = CLIMATE_MODIFIERS[climate_enum]
    
    # Apply winemaking style
    style_mod = WINEMAKING_STYLE_MODIFIERS[style_enum]
    
    # Apply oak treatment
    oak_char = OAK_CHARACTERISTICS[oak_enum]
    
    # Apply age transformations
    age_transform = AGE_TRANSFORMATIONS[age_enum]
    
    # Calculate balance profile
    balance = BalanceProfile(
        acidity=acidity,
        tannin=tannin,
        sweetness=sweetness,
        alcohol=alcohol,
        body=body
    )
    
    # Get finish characteristics
    finish_char = FINISH_CHARACTERISTICS.get(finish_length, FINISH_CHARACTERISTICS["medium"])
    
    # Process aroma clusters
    aroma_palette = []
    aroma_descriptors = []
    if primary_aromas:
        # Preprocess aroma list once (optimization: avoid repeated .lower() in nested loop)
        aromas_normalized = [aroma.lower() for aroma in primary_aromas]
        
        for aroma in aromas_normalized:
            # Find which cluster this aroma belongs to
            for cluster_name, cluster_data in AROMA_CLUSTERS.items():
                if aroma in cluster_data["notes"]:
                    aroma_palette.extend(cluster_data["color_palette"])
                    aroma_descriptors.append(cluster_data["brightness"])
                    aroma_descriptors.append(cluster_data["texture"])
    
    # Compose final visual vocabulary
    visual_vocabulary = {
        "base_color": {
            "hue": varietal_char.get("color_hue", "#FFFFFF"),
            "description": varietal_char.get("color_base", ""),
            "age_modified": age_transform.get("red_color_shift" if is_red_varietal(varietal) else "white_color_shift", ""),
            "climate_shift": climate_mod["color_shift"]
        },
        
        "opacity_clarity": {
            "base_opacity": varietal_char.get("opacity", 0.8),
            "clarity": age_transform["visual_clarity"],
            "visual_weight": balance.get_visual_weight()
        },
        
        "texture_surface": {
            "base_texture": varietal_char.get("texture", ""),
            "structure": varietal_char.get("structure", ""),
            "climate_modifier": climate_mod["texture_modifier"],
            "oak_overlay": oak_char["texture_overlay"],
            "age_state": age_transform["texture_state"]
        },
        
        "compositional_structure": {
            "base_composition": varietal_char.get("composition", ""),
            "style_aesthetic": style_mod["aesthetic"],
            "visual_tension": balance.get_visual_tension(),
            "integration": age_transform["integration"],
            "edge_quality": varietal_char.get("edge_quality", ""),
            "edge_treatment": climate_mod["edge_treatment"]
        },
        
        "atmospheric_qualities": {
            "climate_atmosphere": climate_mod["atmosphere"],
            "style_atmosphere": style_mod["atmosphere"],
            "finish_depth": finish_char["atmospheric_depth"],
            "fade_pattern": finish_char["fade_pattern"],
            "time_signature": age_transform["time_signature"]
        },
        
        "material_references": {
            "oak_materials": oak_char["material_reference"],
            "finish_quality": oak_char["finish_quality"],
            "age_patina": "aged weathered" if age_enum in [AgeCategory.MATURE, AgeCategory.PAST_PRIME] else "fresh new"
        },
        
        "color_palette": {
            "primary": varietal_char.get("color_hue", "#FFFFFF"),
            "aroma_palette": aroma_palette[:4] if aroma_palette else [],
            "saturation_adjust": climate_mod["saturation_adjust"],
            "brightness_adjust": climate_mod["brightness_adjust"],
            "color_treatment": style_mod["color_treatment"]
        },
        
        "aromatic_descriptors": {
            "characteristic_notes": varietal_char.get("characteristic_notes", []),
            "aroma_category": age_transform["aromatic_category"],
            "aroma_textures": list(set(aroma_descriptors))
        },
        
        "balance_relationships": {
            "acidity": acidity,
            "tannin": tannin,
            "sweetness": sweetness,
            "alcohol": alcohol,
            "body": body,
            "visual_tension": balance.get_visual_tension(),
            "visual_weight": balance.get_visual_weight()
        },
        
        "finish_dimension": {
            "length": finish_length,
            "descriptor": finish_char["length_descriptor"],
            "edge_treatment": finish_char["edge_treatment"],
            "fade_pattern": finish_char["fade_pattern"]
        },
        
        "metadata": {
            "varietal": varietal,
            "climate": climate,
            "winemaking_style": winemaking_style,
            "oak_treatment": oak_treatment,
            "age_category": age
        }
    }
    
    return visual_vocabulary


@mcp.tool()
def compare_wine_profiles(
    wine1_params: Dict,
    wine2_params: Dict
) -> Dict:
    """
    Compare two wine profiles to identify visual contrasts and similarities.
    
    Useful for creating comparative visualizations or understanding how
    different wines would look different visually.
    
    Args:
        wine1_params: Parameters for first wine (same as generate_wine_visual_vocabulary)
        wine2_params: Parameters for second wine
    
    Returns:
        Comparison analysis with contrasts and similarities
    """
    
    # Call the underlying functions, not the wrapped tools
    vocab1 = generate_wine_visual_vocabulary.fn(**wine1_params)
    vocab2 = generate_wine_visual_vocabulary.fn(**wine2_params)
    
    comparison = {
        "color_contrast": {
            "wine1": vocab1["base_color"],
            "wine2": vocab2["base_color"],
            "difference": "significant" if vocab1["base_color"]["hue"] != vocab2["base_color"]["hue"] else "subtle"
        },
        
        "texture_contrast": {
            "wine1": vocab1["texture_surface"]["base_texture"],
            "wine2": vocab2["texture_surface"]["base_texture"],
            "structural_difference": f"{vocab1['texture_surface']['structure']} vs {vocab2['texture_surface']['structure']}"
        },
        
        "weight_contrast": {
            "wine1": vocab1["opacity_clarity"]["visual_weight"],
            "wine2": vocab2["opacity_clarity"]["visual_weight"]
        },
        
        "atmospheric_contrast": {
            "wine1": vocab1["atmospheric_qualities"],
            "wine2": vocab2["atmospheric_qualities"]
        },
        
        "balance_comparison": {
            "wine1_tension": vocab1["balance_relationships"]["visual_tension"],
            "wine2_tension": vocab2["balance_relationships"]["visual_tension"],
            "wine1_weight": vocab1["balance_relationships"]["visual_weight"],
            "wine2_weight": vocab2["balance_relationships"]["visual_weight"]
        }
    }
    
    return comparison


@mcp.tool()
def get_varietal_list() -> Dict:
    """
    Get list of all supported wine varietals with their basic characteristics.
    
    Returns:
        Dictionary of varietals with descriptive info
    """
    
    varietal_info = {}
    
    for varietal in Varietal:
        char = VARIETAL_CHARACTERISTICS.get(varietal, {})
        varietal_info[varietal.value] = {
            "color": char.get("color_base", ""),
            "texture": char.get("texture", ""),
            "structure": char.get("structure", ""),
            "notes": char.get("characteristic_notes", [])
        }
    
    return varietal_info


@mcp.tool()
def get_aroma_clusters() -> Dict:
    """
    Get all aroma/flavor clusters with their visual characteristics.
    
    Returns:
        Dictionary of aroma clusters with color palettes and descriptors
    """
    return AROMA_CLUSTERS


@mcp.tool()
def create_regional_preset(
    region: str
) -> Dict:
    """
    Generate visual vocabulary for classic wine regions with typical characteristics.
    
    Supports major wine regions with their characteristic styles.
    
    Args:
        region: Wine region name (e.g., "burgundy", "napa", "rioja", "mosel")
    
    Returns:
        Pre-configured parameters for that region's typical wines
    """
    
    region_presets = {
        "burgundy_red": {
            "varietal": "pinot_noir",
            "climate": "cool",
            "winemaking_style": "old_world",
            "oak_treatment": "french_oak",
            "age": "developing",
            "acidity": 7.5,
            "tannin": 6.0,
            "sweetness": 2.0,
            "alcohol": 6.5,
            "body": 5.5,
            "finish_length": "long",
            "primary_aromas": ["cherry", "mushroom", "rose"]
        },
        
        "burgundy_white": {
            "varietal": "chardonnay",
            "climate": "cool",
            "winemaking_style": "old_world",
            "oak_treatment": "french_oak",
            "age": "developing",
            "acidity": 7.0,
            "tannin": 0.0,
            "sweetness": 2.0,
            "alcohol": 6.5,
            "body": 7.0,
            "finish_length": "long",
            "primary_aromas": ["apple", "hazelnut", "toast"]
        },
        
        "napa_cabernet": {
            "varietal": "cabernet_sauvignon",
            "climate": "warm",
            "winemaking_style": "new_world",
            "oak_treatment": "american_oak",
            "age": "youthful",
            "acidity": 5.5,
            "tannin": 8.5,
            "sweetness": 2.5,
            "alcohol": 8.5,
            "body": 9.0,
            "finish_length": "very_long",
            "primary_aromas": ["blackcurrant", "vanilla", "cedar"]
        },
        
        "rioja_tempranillo": {
            "varietal": "tempranillo",
            "climate": "moderate",
            "winemaking_style": "old_world",
            "oak_treatment": "american_oak",
            "age": "mature",
            "acidity": 6.0,
            "tannin": 6.5,
            "sweetness": 2.0,
            "alcohol": 6.5,
            "body": 6.5,
            "finish_length": "medium",
            "primary_aromas": ["cherry", "leather", "vanilla", "dried_herbs"]
        },
        
        "mosel_riesling": {
            "varietal": "riesling",
            "climate": "cool",
            "winemaking_style": "old_world",
            "oak_treatment": "none",
            "age": "youthful",
            "acidity": 9.0,
            "tannin": 0.0,
            "sweetness": 4.0,
            "alcohol": 4.5,
            "body": 4.0,
            "finish_length": "long",
            "primary_aromas": ["lime", "slate", "petrol"]
        },
        
        "barolo": {
            "varietal": "nebbiolo",
            "climate": "moderate",
            "winemaking_style": "old_world",
            "oak_treatment": "neutral",
            "age": "mature",
            "acidity": 8.5,
            "tannin": 9.0,
            "sweetness": 1.5,
            "alcohol": 7.5,
            "body": 7.0,
            "finish_length": "very_long",
            "primary_aromas": ["rose", "tar", "truffle", "dried_cherry"]
        },
        
        "rhone_syrah": {
            "varietal": "syrah",
            "climate": "moderate",
            "winemaking_style": "old_world",
            "oak_treatment": "french_oak",
            "age": "developing",
            "acidity": 6.0,
            "tannin": 7.5,
            "sweetness": 2.0,
            "alcohol": 7.0,
            "body": 8.0,
            "finish_length": "long",
            "primary_aromas": ["blackberry", "pepper", "smoke"]
        },
        
        "marlborough_sauvignon": {
            "varietal": "sauvignon_blanc",
            "climate": "cool",
            "winemaking_style": "new_world",
            "oak_treatment": "none",
            "age": "youthful",
            "acidity": 8.5,
            "tannin": 0.0,
            "sweetness": 1.5,
            "alcohol": 6.0,
            "body": 5.0,
            "finish_length": "medium",
            "primary_aromas": ["grapefruit", "grass", "gooseberry"]
        }
    }
    
    region_lower = region.lower().replace(" ", "_")
    
    if region_lower in region_presets:
        params = region_presets[region_lower]
        # Call the underlying function, not the wrapped tool
        vocab = generate_wine_visual_vocabulary.fn(**params)
        vocab["regional_preset"] = region
        return vocab
    else:
        return {
            "error": f"Region '{region}' not found",
            "available_regions": list(region_presets.keys())
        }


# ============================================================================
# STRATEGIC ANALYSIS (Tomographic Domain Projection)
# ============================================================================

STRATEGIC_PATTERNS = {
    "balance_integration": {
        "well_balanced": {
            "patterns": [
                r"well[- ]balanced", r"harmonious", r"coherent", r"integrated",
                r"unified", r"complement(?:ary|ing)", r"synerg(?:y|istic)",
                r"align(?:ed|ment)"
            ],
            "threshold": 4,
            "confidence": 0.8
        },
        "acidic_harsh": {
            "patterns": [
                r"harsh", r"acidic", r"sharp", r"bitter", r"conflict(?:ing|s)",
                r"tension", r"discord", r"contradict"
            ],
            "threshold": 3,
            "confidence": 0.75
        },
        "flabby_unfocused": {
            "patterns": [
                r"flabb", r"unfocused", r"diffuse", r"lack.*direction",
                r"unclear", r"vague", r"scattered", r"incoherent"
            ],
            "threshold": 3,
            "confidence": 0.75
        },
        "tannic_rigid": {
            "patterns": [
                r"rigid", r"inflexible", r"tannic", r"harsh.*structure",
                r"over.*constrain", r"restrictive", r"bureaucratic"
            ],
            "threshold": 4,
            "confidence": 0.7
        }
    },
    "temporal_maturity": {
        "youthful_premature": {
            "patterns": [
                r"premature", r"rushed", r"immature", r"under.*developed",
                r"too.*early", r"not.*ready", r"incomplete"
            ],
            "threshold": 3,
            "confidence": 0.8
        },
        "developing_integration": {
            "patterns": [
                r"developing", r"evolving", r"maturing", r"progress(?:ing|ion)",
                r"phase", r"transition", r"emerging"
            ],
            "threshold": 3,
            "confidence": 0.75
        },
        "mature_refined": {
            "patterns": [
                r"mature", r"refined", r"seasoned", r"established",
                r"proven", r"sophisticated", r"well.*developed"
            ],
            "threshold": 3,
            "confidence": 0.8
        },
        "past_prime_outdated": {
            "patterns": [
                r"outdated", r"stale", r"past.*prime", r"declining",
                r"obsolete", r"legacy.*burden", r"over.*mature"
            ],
            "threshold": 2,
            "confidence": 0.85
        }
    },
    "strategic_substance": {
        "light_insufficient": {
            "patterns": [
                r"insufficient", r"thin", r"weak", r"inadequate",
                r"under.*resource", r"lack.*substance", r"superficial"
            ],
            "threshold": 3,
            "confidence": 0.75
        },
        "full_bodied": {
            "patterns": [
                r"substantial", r"robust", r"strong", r"full(?:y|-)resource",
                r"comprehensive", r"thorough", r"well.*supported"
            ],
            "threshold": 4,
            "confidence": 0.8
        },
        "overweight_bloated": {
            "patterns": [
                r"bloat(?:ed)?", r"excessive", r"over.*resource",
                r"too.*complex", r"unwieldy", r"over.*built"
            ],
            "threshold": 3,
            "confidence": 0.75
        }
    },
    "persistence_planning": {
        "short_tactical": {
            "patterns": [
                r"short[- ]term", r"tactical", r"immediate", r"quick.*win",
                r"near[- ]term", r"reactive", r"ad[- ]hoc"
            ],
            "threshold": 4,
            "confidence": 0.8
        },
        "medium_balanced": {
            "patterns": [
                r"medium[- ]term", r"balanced.*horizon", r"phased",
                r"staged", r"incremental", r"quarterly"
            ],
            "threshold": 3,
            "confidence": 0.75
        },
        "long_strategic": {
            "patterns": [
                r"long[- ]term", r"strategic", r"sustained", r"enduring",
                r"multi[- ]year", r"persistent", r"lasting.*impact"
            ],
            "threshold": 3,
            "confidence": 0.8
        },
        "very_long_visionary": {
            "patterns": [
                r"visionary", r"transformational", r"decade", r"generational",
                r"legacy", r"fundamental.*shift", r"paradigm"
            ],
            "threshold": 2,
            "confidence": 0.85
        }
    }
}


def detect_balance_integration(text: str) -> list:
    """Detect strategic coherence patterns (constraints family)."""
    dimension = "balance_integration"
    findings = []
    
    for pattern_name, pattern_spec in STRATEGIC_PATTERNS[dimension].items():
        matches = []
        for regex in pattern_spec["patterns"]:
            found = re.finditer(regex, text, re.IGNORECASE)
            matches.extend([m.group() for m in found])
        
        if len(matches) >= pattern_spec["threshold"]:
            findings.append({
                "dimension": dimension,
                "pattern": pattern_name,
                "confidence": pattern_spec["confidence"],
                "evidence": matches[:5],  # First 5 matches
                "categorical_family": "constraints"
            })
    
    return findings


def detect_temporal_maturity(text: str) -> list:
    """Detect maturity/timing patterns (morphisms family)."""
    dimension = "temporal_maturity"
    findings = []
    
    for pattern_name, pattern_spec in STRATEGIC_PATTERNS[dimension].items():
        matches = []
        for regex in pattern_spec["patterns"]:
            found = re.finditer(regex, text, re.IGNORECASE)
            matches.extend([m.group() for m in found])
        
        if len(matches) >= pattern_spec["threshold"]:
            findings.append({
                "dimension": dimension,
                "pattern": pattern_name,
                "confidence": pattern_spec["confidence"],
                "evidence": matches[:5],
                "categorical_family": "morphisms"
            })
    
    return findings


def detect_strategic_substance(text: str) -> list:
    """Detect resource commitment patterns (objects family)."""
    dimension = "strategic_substance"
    findings = []
    
    for pattern_name, pattern_spec in STRATEGIC_PATTERNS[dimension].items():
        matches = []
        for regex in pattern_spec["patterns"]:
            found = re.finditer(regex, text, re.IGNORECASE)
            matches.extend([m.group() for m in found])
        
        if len(matches) >= pattern_spec["threshold"]:
            findings.append({
                "dimension": dimension,
                "pattern": pattern_name,
                "confidence": pattern_spec["confidence"],
                "evidence": matches[:5],
                "categorical_family": "objects"
            })
    
    return findings


def detect_persistence_planning(text: str) -> list:
    """Detect long-term thinking patterns (morphisms family)."""
    dimension = "persistence_planning"
    findings = []
    
    for pattern_name, pattern_spec in STRATEGIC_PATTERNS[dimension].items():
        matches = []
        for regex in pattern_spec["patterns"]:
            found = re.finditer(regex, text, re.IGNORECASE)
            matches.extend([m.group() for m in found])
        
        if len(matches) >= pattern_spec["threshold"]:
            findings.append({
                "dimension": dimension,
                "pattern": pattern_name,
                "confidence": pattern_spec["confidence"],
                "evidence": matches[:5],
                "categorical_family": "morphisms"
            })
    
    return findings


def analyze_strategy_document(strategy_text: str) -> Dict[str, Any]:
    """
    Analyze strategy document through wine tasting lens.
    
    Pure deterministic pattern matching - zero LLM cost.
    Projects strategy through wine vocabulary to detect structural patterns.
    """
    all_findings = []
    
    # Run all four detectors
    all_findings.extend(detect_balance_integration(strategy_text))
    all_findings.extend(detect_temporal_maturity(strategy_text))
    all_findings.extend(detect_strategic_substance(strategy_text))
    all_findings.extend(detect_persistence_planning(strategy_text))
    
    # Filter by confidence threshold
    confidence_threshold = 0.6
    filtered_findings = [f for f in all_findings if f["confidence"] >= confidence_threshold]
    
    return {
        "domain": "wine_tasting",
        "findings": filtered_findings,
        "total_findings": len(filtered_findings),
        "methodology": "deterministic_pattern_matching",
        "llm_cost_tokens": 0
    }


@mcp.tool()
def evolution_sequence(
    varietal: str,
    climate: str = "moderate",
    winemaking_style: str = "old_world",
    oak_treatment: str = "french_oak",
    acidity: float = 6.0,
    tannin: float = 6.0,
    sweetness: float = 2.0,
    alcohol: float = 6.5,
    body: float = 6.5,
    finish_length: str = "long"
) -> Dict:
    """
    Generate a temporal sequence showing how a wine evolves visually over time.
    
    Creates visual vocabularies for the same wine at different age stages,
    showing the categorical transformation over time.
    
    Args:
        (Same base parameters as generate_wine_visual_vocabulary, minus age)
    
    Returns:
        Dictionary with visual vocabularies at each age stage
    """
    
    base_params = {
        "varietal": varietal,
        "climate": climate,
        "winemaking_style": winemaking_style,
        "oak_treatment": oak_treatment,
        "acidity": acidity,
        "tannin": tannin,
        "sweetness": sweetness,
        "alcohol": alcohol,
        "body": body,
        "finish_length": finish_length
    }
    
    sequence = {}
    
    for age in ["youthful", "developing", "mature", "past_prime"]:
        params = base_params.copy()
        params["age"] = age
        # Call the underlying function, not the wrapped tool
        sequence[age] = generate_wine_visual_vocabulary.fn(**params)
    
    return {
        "evolution_sequence": sequence,
        "key_transformations": {
            "color": "purple/pale → garnet/gold → brick/amber → brown",
            "texture": "taut → integrating → silky → thin",
            "aromatics": "primary → secondary → tertiary → fading",
            "clarity": "brilliant → bright → clear → dull"
        }
    }


# ============================================================================
# PHASE 2.6 - NORMALIZED PARAMETER SPACE & RHYTHMIC PRESETS
# ============================================================================
# Wine tasting aesthetic morphospace: 5 normalized dimensions [0.0, 1.0]
#
# structural_tension:  Acidity + tannin grip → angular/taut vs soft/round
# color_depth:         Opacity, saturation, darkness of visual impression
# aromatic_complexity: Primary/simple → tertiary/layered development
# textural_weight:     Light/ethereal → full/dense body and viscosity
# temporal_maturity:   Youthful/bright → aged/evolved patina
# ============================================================================

import math
import numpy as np

WINE_PARAMETER_NAMES = [
    "structural_tension",
    "color_depth",
    "aromatic_complexity",
    "textural_weight",
    "temporal_maturity"
]

# Canonical wine states in normalized 5D morphospace
WINE_TASTING_COORDS = {
    "young_burgundy": {
        "structural_tension": 0.70,
        "color_depth": 0.45,
        "aromatic_complexity": 0.40,
        "textural_weight": 0.40,
        "temporal_maturity": 0.15
    },
    "aged_barolo": {
        "structural_tension": 0.85,
        "color_depth": 0.55,
        "aromatic_complexity": 0.95,
        "textural_weight": 0.65,
        "temporal_maturity": 0.90
    },
    "napa_cabernet": {
        "structural_tension": 0.60,
        "color_depth": 0.95,
        "aromatic_complexity": 0.50,
        "textural_weight": 0.95,
        "temporal_maturity": 0.20
    },
    "mosel_riesling": {
        "structural_tension": 0.90,
        "color_depth": 0.15,
        "aromatic_complexity": 0.55,
        "textural_weight": 0.15,
        "temporal_maturity": 0.10
    },
    "rhone_syrah": {
        "structural_tension": 0.55,
        "color_depth": 0.90,
        "aromatic_complexity": 0.65,
        "textural_weight": 0.85,
        "temporal_maturity": 0.35
    },
    "champagne_brut": {
        "structural_tension": 0.80,
        "color_depth": 0.20,
        "aromatic_complexity": 0.60,
        "textural_weight": 0.25,
        "temporal_maturity": 0.30
    },
    "sauternes": {
        "structural_tension": 0.35,
        "color_depth": 0.75,
        "aromatic_complexity": 0.90,
        "textural_weight": 0.80,
        "temporal_maturity": 0.70
    }
}

# Phase 2.6 rhythmic preset definitions
WINE_RHYTHMIC_PRESETS = {
    "aging_evolution": {
        "state_a": "young_burgundy",
        "state_b": "aged_barolo",
        "pattern": "sinusoidal",
        "num_cycles": 3,
        "steps_per_cycle": 24,
        "description": "Temporal evolution from youthful vibrancy to aged complexity"
    },
    "weight_spectrum": {
        "state_a": "mosel_riesling",
        "state_b": "napa_cabernet",
        "pattern": "triangular",
        "num_cycles": 4,
        "steps_per_cycle": 20,
        "description": "Full sweep from crystalline delicacy to monumental density"
    },
    "terroir_pulse": {
        "state_a": "young_burgundy",
        "state_b": "rhone_syrah",
        "pattern": "sinusoidal",
        "num_cycles": 4,
        "steps_per_cycle": 18,
        "description": "Cool-climate finesse pulsing against warm-climate power"
    },
    "elegance_richness": {
        "state_a": "champagne_brut",
        "state_b": "sauternes",
        "pattern": "sinusoidal",
        "num_cycles": 5,
        "steps_per_cycle": 15,
        "description": "Taut effervescent precision cycling with honeyed opulence"
    },
    "structure_toggle": {
        "state_a": "mosel_riesling",
        "state_b": "aged_barolo",
        "pattern": "square",
        "num_cycles": 5,
        "steps_per_cycle": 12,
        "description": "Sharp alternation between crystalline youth and austere maturity"
    }
}

# ============================================================================
# PHASE 2.7 - VISUAL VOCABULARY & PROMPT GENERATION
# ============================================================================
# Visual types map canonical states to image-generation-ready keywords.
# Nearest-neighbor matching translates any 5D coordinate to visual vocabulary.
# ============================================================================

WINE_VISUAL_TYPES = {
    "burgundian_silk": {
        "coords": {
            "structural_tension": 0.70,
            "color_depth": 0.45,
            "aromatic_complexity": 0.40,
            "textural_weight": 0.40,
            "temporal_maturity": 0.15
        },
        "keywords": [
            "translucent ruby glow",
            "silk draped over fine bone structure",
            "delicate cherry-rose luminescence",
            "cool mineral transparency",
            "intimate layered depth",
            "precise elegant restraint",
            "forest-floor earthiness"
        ],
        "optical_properties": {
            "finish": "satin",
            "transparency": "translucent",
            "refraction": "soft diffused glow",
            "dominant_palette": ["#8B2635", "#C71585", "#FFB6C1"]
        }
    },
    "barolo_patina": {
        "coords": {
            "structural_tension": 0.85,
            "color_depth": 0.55,
            "aromatic_complexity": 0.95,
            "textural_weight": 0.65,
            "temporal_maturity": 0.90
        },
        "keywords": [
            "aged garnet-brick translucence",
            "tar and rose petal duality",
            "noble austere architecture",
            "chalky tannic grip texture",
            "tertiary truffle complexity",
            "time-weathered aristocratic patina",
            "dried herb and leather warmth"
        ],
        "optical_properties": {
            "finish": "matte chalky",
            "transparency": "semi-translucent",
            "refraction": "warm brick-edge glow",
            "dominant_palette": ["#9B4F47", "#654321", "#8B4513"]
        }
    },
    "napa_monument": {
        "coords": {
            "structural_tension": 0.60,
            "color_depth": 0.95,
            "aromatic_complexity": 0.50,
            "textural_weight": 0.95,
            "temporal_maturity": 0.20
        },
        "keywords": [
            "deep opaque purple-black density",
            "monumental architectural weight",
            "charred oak and dark fruit saturation",
            "bold commanding visual mass",
            "velvety concentrated darkness",
            "sun-drenched power and extract",
            "polished new-oak sheen"
        ],
        "optical_properties": {
            "finish": "lacquered",
            "transparency": "opaque",
            "refraction": "deep absorptive",
            "dominant_palette": ["#2C1810", "#1A0F14", "#4A0E4E"]
        }
    },
    "riesling_crystal": {
        "coords": {
            "structural_tension": 0.90,
            "color_depth": 0.15,
            "aromatic_complexity": 0.55,
            "textural_weight": 0.15,
            "temporal_maturity": 0.10
        },
        "keywords": [
            "crystalline pale-straw luminosity",
            "razor-sharp mineral precision",
            "electric citrus-petrol clarity",
            "taut wire-like structural tension",
            "transparent slate-cold purity",
            "brilliant star-bright refraction",
            "weightless ethereal suspension"
        ],
        "optical_properties": {
            "finish": "crystalline",
            "transparency": "transparent",
            "refraction": "prismatic brilliant",
            "dominant_palette": ["#FFFACD", "#F5F5DC", "#BFFF00"]
        }
    },
    "rhone_wildfire": {
        "coords": {
            "structural_tension": 0.55,
            "color_depth": 0.90,
            "aromatic_complexity": 0.65,
            "textural_weight": 0.85,
            "temporal_maturity": 0.35
        },
        "keywords": [
            "inky purple-black smoke depth",
            "wild untamed visceral power",
            "cracked black pepper and smoked meat",
            "primal dynamic dark energy",
            "dense smoky atmospheric haze",
            "garrigue herb-scrub earthiness",
            "volcanic dark-fruit intensity"
        ],
        "optical_properties": {
            "finish": "smoky matte",
            "transparency": "near-opaque",
            "refraction": "smouldering dark glow",
            "dominant_palette": ["#1A0F14", "#2C1810", "#4A0E4E"]
        }
    },
    "champagne_effervescence": {
        "coords": {
            "structural_tension": 0.80,
            "color_depth": 0.20,
            "aromatic_complexity": 0.60,
            "textural_weight": 0.25,
            "temporal_maturity": 0.30
        },
        "keywords": [
            "pale gold effervescent sparkle",
            "fine persistent bead streams",
            "crisp autolytic biscuit elegance",
            "taut mousse-like textural lift",
            "luminous celebratory brightness",
            "chalk-driven mineral backbone",
            "precise toasty sophistication"
        ],
        "optical_properties": {
            "finish": "effervescent",
            "transparency": "translucent sparkling",
            "refraction": "dancing light refractions",
            "dominant_palette": ["#F4E4C1", "#FFD700", "#FFFACD"]
        }
    },
    "sauternes_gold": {
        "coords": {
            "structural_tension": 0.35,
            "color_depth": 0.75,
            "aromatic_complexity": 0.90,
            "textural_weight": 0.80,
            "temporal_maturity": 0.70
        },
        "keywords": [
            "deep amber-gold honeyed viscosity",
            "botrytis noble-rot opulence",
            "luscious apricot-saffron richness",
            "unctuous coating glycerol weight",
            "concentrated marmalade warmth",
            "perfumed exotic dried-fruit layers",
            "candied ginger and beeswax sheen"
        ],
        "optical_properties": {
            "finish": "viscous glossy",
            "transparency": "deep translucent",
            "refraction": "warm amber diffusion",
            "dominant_palette": ["#FFD700", "#FF8C00", "#DEB887"]
        }
    }
}


# ============================================================================
# PHASE 2.6 LAYER 2 - Deterministic Computation (0 tokens)
# ============================================================================

def _generate_wine_oscillation(num_steps: int, num_cycles: float, pattern: str):
    """Generate oscillation envelope [0, 1]."""
    t = [2.0 * math.pi * num_cycles * i / num_steps for i in range(num_steps)]
    
    if pattern == "sinusoidal":
        return [0.5 * (1.0 + math.sin(ti)) for ti in t]
    elif pattern == "triangular":
        result = []
        for ti in t:
            t_norm = (ti / (2.0 * math.pi)) % 1.0
            result.append(2.0 * t_norm if t_norm < 0.5 else 2.0 * (1.0 - t_norm))
        return result
    elif pattern == "square":
        return [0.0 if (ti / (2.0 * math.pi)) % 1.0 < 0.5 else 1.0 for ti in t]
    else:
        raise ValueError(f"Unknown pattern: {pattern}")


def _interpolate_wine_states(state_a_id: str, state_b_id: str, alpha: float) -> dict:
    """Interpolate between two wine states by blend factor alpha."""
    a = WINE_TASTING_COORDS[state_a_id]
    b = WINE_TASTING_COORDS[state_b_id]
    return {
        p: a[p] * (1.0 - alpha) + b[p] * alpha
        for p in WINE_PARAMETER_NAMES
    }


def _euclidean_distance_wine(state1: dict, state2: dict) -> float:
    """Euclidean distance between two wine parameter states."""
    return math.sqrt(sum(
        (state1[p] - state2[p]) ** 2
        for p in WINE_PARAMETER_NAMES
    ))


def _find_nearest_wine_visual_type(state: dict) -> tuple:
    """Find nearest visual type by Euclidean distance. Returns (type_id, distance)."""
    min_dist = float('inf')
    nearest = None
    for type_id, type_data in WINE_VISUAL_TYPES.items():
        dist = _euclidean_distance_wine(state, type_data["coords"])
        if dist < min_dist:
            min_dist = dist
            nearest = type_id
    return nearest, min_dist


def _generate_wine_preset_sequence(preset_name: str) -> list:
    """Generate full oscillation sequence for a preset."""
    preset = WINE_RHYTHMIC_PRESETS[preset_name]
    total_steps = preset["num_cycles"] * preset["steps_per_cycle"]
    alphas = _generate_wine_oscillation(total_steps, preset["num_cycles"], preset["pattern"])
    
    sequence = []
    for i, alpha in enumerate(alphas):
        state = _interpolate_wine_states(preset["state_a"], preset["state_b"], alpha)
        sequence.append({
            "step": i,
            "phase": i / total_steps,
            "blend_factor": round(alpha, 4),
            "state": {p: round(v, 4) for p, v in state.items()}
        })
    return sequence


# ============================================================================
# PHASE 2.6 MCP TOOLS
# ============================================================================

@mcp.tool()
def get_wine_tasting_types() -> str:
    """
    List all 7 canonical wine tasting visual types with descriptions.

    Layer 1: Pure taxonomy lookup (0 tokens)

    Returns:
        JSON mapping wine type IDs to their 5D parameter coordinates
        and human-readable descriptions.
    """
    result = {}
    for type_id, data in WINE_VISUAL_TYPES.items():
        result[type_id] = {
            "coords": data["coords"],
            "keyword_preview": data["keywords"][:3],
            "optical_finish": data["optical_properties"]["finish"]
        }
    return json.dumps(result, indent=2)


@mcp.tool()
def get_wine_tasting_specifications(wine_type_id: str) -> str:
    """
    Get complete visual specifications for a wine tasting type.

    Layer 1: Pure taxonomy lookup (0 tokens)

    Args:
        wine_type_id: One of the 7 canonical wine types
            (burgundian_silk, barolo_patina, napa_monument,
             riesling_crystal, rhone_wildfire, champagne_effervescence,
             sauternes_gold)

    Returns:
        Complete visual vocabulary, optical properties, and parameter coordinates.
    """
    if wine_type_id not in WINE_VISUAL_TYPES:
        available = list(WINE_VISUAL_TYPES.keys())
        return json.dumps({"error": f"Unknown type '{wine_type_id}'", "available": available})

    data = WINE_VISUAL_TYPES[wine_type_id]
    return json.dumps({
        "type_id": wine_type_id,
        "parameter_coordinates": data["coords"],
        "visual_keywords": data["keywords"],
        "optical_properties": data["optical_properties"],
        "parameter_names": WINE_PARAMETER_NAMES
    }, indent=2)


@mcp.tool()
def map_wine_tasting_parameters(
    wine_type_id: str,
    intensity: str = "moderate",
    emphasis: str = "finish"
) -> str:
    """
    Map wine type to visual parameters for image generation.

    Layer 2: Deterministic operation (0 tokens)

    Args:
        wine_type_id: Which wine type (burgundian_silk, barolo_patina, etc.)
        intensity: "subtle", "moderate", or "dramatic"
        emphasis: "finish", "texture", "color", "aroma", or "structure"

    Returns:
        Complete parameter set for visual synthesis including vocabulary
        weighted by intensity and emphasis.
    """
    if wine_type_id not in WINE_VISUAL_TYPES:
        available = list(WINE_VISUAL_TYPES.keys())
        return json.dumps({"error": f"Unknown type '{wine_type_id}'", "available": available})

    data = WINE_VISUAL_TYPES[wine_type_id]

    # Intensity multipliers
    intensity_map = {"subtle": 0.5, "moderate": 1.0, "dramatic": 1.5}
    mult = intensity_map.get(intensity, 1.0)

    # Emphasis selects which keywords get boosted
    emphasis_keyword_indices = {
        "finish": [0, 5],     # first and structural keywords
        "texture": [1, 3],    # texture-related keywords
        "color": [0, 2],      # color keywords
        "aroma": [2, 4, 5],   # aromatic / complexity keywords
        "structure": [1, 3, 5] # structural keywords
    }
    boosted = emphasis_keyword_indices.get(emphasis, [0])

    weighted_keywords = []
    for i, kw in enumerate(data["keywords"]):
        weight = mult * (1.5 if i in boosted else 1.0)
        weighted_keywords.append({"keyword": kw, "weight": round(weight, 2)})

    return json.dumps({
        "wine_type": wine_type_id,
        "intensity": intensity,
        "emphasis": emphasis,
        "parameter_coordinates": data["coords"],
        "weighted_keywords": weighted_keywords,
        "optical_properties": data["optical_properties"]
    }, indent=2)


@mcp.tool()
def compute_wine_tasting_distance(wine_type_id_1: str, wine_type_id_2: str) -> str:
    """
    Compute distance between two wine tasting types.

    Layer 2: Pure distance computation (0 tokens)

    Args:
        wine_type_id_1: First wine type
        wine_type_id_2: Second wine type

    Returns:
        Distance value and per-parameter breakdown.
    """
    if wine_type_id_1 not in WINE_VISUAL_TYPES or wine_type_id_2 not in WINE_VISUAL_TYPES:
        return json.dumps({"error": "Unknown wine type(s)",
                           "available": list(WINE_VISUAL_TYPES.keys())})

    c1 = WINE_VISUAL_TYPES[wine_type_id_1]["coords"]
    c2 = WINE_VISUAL_TYPES[wine_type_id_2]["coords"]

    per_param = {p: round(abs(c1[p] - c2[p]), 4) for p in WINE_PARAMETER_NAMES}
    total = round(_euclidean_distance_wine(c1, c2), 4)

    return json.dumps({
        "wine_type_1": wine_type_id_1,
        "wine_type_2": wine_type_id_2,
        "euclidean_distance": total,
        "per_parameter": per_param
    }, indent=2)


@mcp.tool()
def compute_wine_tasting_trajectory(
    start_wine_type_id: str,
    end_wine_type_id: str,
    num_steps: int = 20
) -> str:
    """
    Compute smooth trajectory between two wine types in morphospace.

    Layer 2: Deterministic trajectory integration (0 tokens)

    Enables visualization of smooth aesthetic transitions — e.g.
    young Burgundy gradually becoming aged Barolo.

    Args:
        start_wine_type_id: Starting wine type
        end_wine_type_id: Target wine type
        num_steps: Number of interpolation steps (default: 20)

    Returns:
        Trajectory with intermediate states, distance profile,
        and transition characteristics.
    """
    if start_wine_type_id not in WINE_VISUAL_TYPES or end_wine_type_id not in WINE_VISUAL_TYPES:
        return json.dumps({"error": "Unknown wine type(s)",
                           "available": list(WINE_VISUAL_TYPES.keys())})

    start = WINE_VISUAL_TYPES[start_wine_type_id]["coords"]
    end = WINE_VISUAL_TYPES[end_wine_type_id]["coords"]
    total_dist = _euclidean_distance_wine(start, end)

    trajectory = []
    for i in range(num_steps + 1):
        t = i / num_steps
        state = {p: round(start[p] * (1.0 - t) + end[p] * t, 4) for p in WINE_PARAMETER_NAMES}
        nearest_type, type_dist = _find_nearest_wine_visual_type(state)
        trajectory.append({
            "step": i,
            "t": round(t, 3),
            "state": state,
            "nearest_visual_type": nearest_type,
            "distance_to_nearest": round(type_dist, 4)
        })

    # Characterize transition
    start_coords = start
    end_coords = end
    biggest_change_param = max(WINE_PARAMETER_NAMES,
                               key=lambda p: abs(end_coords[p] - start_coords[p]))

    return json.dumps({
        "start": start_wine_type_id,
        "end": end_wine_type_id,
        "num_steps": num_steps,
        "total_distance": round(total_dist, 4),
        "dominant_transition_axis": biggest_change_param,
        "trajectory": trajectory
    }, indent=2)


@mcp.tool()
def list_wine_tasting_rhythmic_presets() -> str:
    """
    List all available wine tasting rhythmic presets.

    Layer 2: Pure lookup (0 tokens)

    Returns:
        Preset names, periods, patterns, and descriptions.
    """
    result = {}
    for name, preset in WINE_RHYTHMIC_PRESETS.items():
        result[name] = {
            "period": preset["steps_per_cycle"],
            "total_steps": preset["num_cycles"] * preset["steps_per_cycle"],
            "pattern": preset["pattern"],
            "state_a": preset["state_a"],
            "state_b": preset["state_b"],
            "description": preset["description"]
        }
    return json.dumps(result, indent=2)


@mcp.tool()
def apply_wine_tasting_rhythmic_preset(preset_name: str) -> str:
    """
    Apply curated wine tasting rhythmic pattern preset.

    Layer 2: Deterministic sequence generation (0 tokens)

    Available presets:
        aging_evolution (24): young_burgundy ↔ aged_barolo
        weight_spectrum (20): mosel_riesling ↔ napa_cabernet
        terroir_pulse (18): young_burgundy ↔ rhone_syrah
        elegance_richness (15): champagne_brut ↔ sauternes
        structure_toggle (12): mosel_riesling ↔ aged_barolo

    Args:
        preset_name: One of the 5 rhythmic presets

    Returns:
        Complete oscillation sequence with parameter states at each step.
    """
    if preset_name not in WINE_RHYTHMIC_PRESETS:
        return json.dumps({"error": f"Unknown preset '{preset_name}'",
                           "available": list(WINE_RHYTHMIC_PRESETS.keys())})

    preset = WINE_RHYTHMIC_PRESETS[preset_name]
    sequence = _generate_wine_preset_sequence(preset_name)

    return json.dumps({
        "preset_name": preset_name,
        "period": preset["steps_per_cycle"],
        "total_steps": len(sequence),
        "pattern": preset["pattern"],
        "state_a": preset["state_a"],
        "state_b": preset["state_b"],
        "description": preset["description"],
        "sequence": sequence
    }, indent=2)


@mcp.tool()
def generate_wine_tasting_rhythmic_sequence(
    state_a_id: str,
    state_b_id: str,
    oscillation_pattern: str = "sinusoidal",
    num_cycles: int = 3,
    steps_per_cycle: int = 20,
    phase_offset: float = 0.0
) -> str:
    """
    Generate rhythmic oscillation between two wine types.

    Layer 2: Temporal composition (0 tokens)

    Args:
        state_a_id: Starting wine state
        state_b_id: Alternating wine state
        oscillation_pattern: "sinusoidal", "triangular", or "square"
        num_cycles: Number of complete A→B→A cycles
        steps_per_cycle: Samples per cycle
        phase_offset: Starting phase (0.0 = A, 0.5 = B)

    Returns:
        Sequence with states, pattern info, and phase points.
    """
    if state_a_id not in WINE_TASTING_COORDS or state_b_id not in WINE_TASTING_COORDS:
        return json.dumps({"error": "Unknown wine state(s)",
                           "available": list(WINE_TASTING_COORDS.keys())})

    total_steps = num_cycles * steps_per_cycle
    alphas = _generate_wine_oscillation(total_steps, num_cycles, oscillation_pattern)

    # Apply phase offset
    if phase_offset > 0:
        offset_steps = int(phase_offset * steps_per_cycle)
        alphas = alphas[offset_steps:] + alphas[:offset_steps]

    sequence = []
    for i, alpha in enumerate(alphas):
        state = _interpolate_wine_states(state_a_id, state_b_id, alpha)
        sequence.append({
            "step": i,
            "phase": round(i / total_steps, 4),
            "blend_factor": round(alpha, 4),
            "state": {p: round(v, 4) for p, v in state.items()}
        })

    return json.dumps({
        "state_a": state_a_id,
        "state_b": state_b_id,
        "oscillation_pattern": oscillation_pattern,
        "num_cycles": num_cycles,
        "steps_per_cycle": steps_per_cycle,
        "total_steps": total_steps,
        "phase_offset": phase_offset,
        "sequence": sequence
    }, indent=2)


# ============================================================================
# PHASE 2.7 - ATTRACTOR VISUALIZATION PROMPT GENERATION
# ============================================================================

@mcp.tool()
def extract_wine_tasting_visual_vocabulary(
    state: Optional[Dict[str, float]] = None,
    wine_type_id: Optional[str] = None,
    strength: float = 1.0
) -> str:
    """
    Extract visual vocabulary from wine parameter coordinates.

    Layer 2: Deterministic vocabulary mapping (0 tokens)

    Maps a 5D parameter state to the nearest visual type and returns
    image-generation-ready keywords.

    Args:
        state: Parameter coordinates dict (structural_tension, color_depth, etc.)
            Provide either state or wine_type_id.
        wine_type_id: Canonical wine type to use as state source.
        strength: Keyword weight multiplier [0.0, 1.0] (default: 1.0)

    Returns:
        Nearest visual type, keywords, optical properties, and vocabulary.
    """
    if wine_type_id and wine_type_id in WINE_VISUAL_TYPES:
        coords = WINE_VISUAL_TYPES[wine_type_id]["coords"]
    elif state:
        coords = state
    else:
        return json.dumps({"error": "Provide either state or wine_type_id"})

    nearest_type, distance = _find_nearest_wine_visual_type(coords)
    type_data = WINE_VISUAL_TYPES[nearest_type]

    weighted_keywords = [
        {"keyword": kw, "weight": round(strength * (1.0 - 0.05 * i), 2)}
        for i, kw in enumerate(type_data["keywords"])
    ]

    return json.dumps({
        "nearest_type": nearest_type,
        "distance": round(distance, 4),
        "keywords": type_data["keywords"],
        "weighted_keywords": weighted_keywords,
        "optical_properties": type_data["optical_properties"],
        "input_state": {p: round(coords.get(p, 0.0), 4) for p in WINE_PARAMETER_NAMES}
    }, indent=2)


@mcp.tool()
def generate_wine_tasting_prompt(
    wine_type_id: str = "",
    custom_state: Optional[Dict[str, float]] = None,
    mode: str = "composite",
    style_modifier: str = ""
) -> str:
    """
    Generate image generation prompt from wine state or canonical type.

    Layer 2: Deterministic prompt synthesis (0 tokens)

    Translates wine tasting coordinates into visual prompts suitable
    for ComfyUI, Stable Diffusion, DALL-E, etc.

    Args:
        wine_type_id: Canonical wine type (or "" with custom_state)
        custom_state: Optional custom 5D coordinates
        mode: "composite" (single blended prompt) or "split_view" (per-category)
        style_modifier: Optional prefix ("photorealistic", "oil painting", etc.)

    Returns:
        Prompt string(s) with vocabulary details and wine metadata.
    """
    # Resolve coordinates
    if custom_state:
        coords = custom_state
    elif wine_type_id and wine_type_id in WINE_VISUAL_TYPES:
        coords = WINE_VISUAL_TYPES[wine_type_id]["coords"]
    else:
        return json.dumps({"error": "Provide wine_type_id or custom_state",
                           "available": list(WINE_VISUAL_TYPES.keys())})

    nearest_type, distance = _find_nearest_wine_visual_type(coords)
    type_data = WINE_VISUAL_TYPES[nearest_type]

    if mode == "composite":
        parts = []
        if style_modifier:
            parts.append(style_modifier)
        parts.extend(type_data["keywords"])
        # Append optical descriptors
        opt = type_data["optical_properties"]
        parts.append(f"{opt['finish']} finish")
        parts.append(f"{opt['refraction']}")
        prompt = ", ".join(parts)

        return json.dumps({
            "mode": "composite",
            "prompt": prompt,
            "nearest_type": nearest_type,
            "distance": round(distance, 4),
            "optical_properties": opt,
            "source_state": {p: round(coords.get(p, 0.0), 4) for p in WINE_PARAMETER_NAMES}
        }, indent=2)

    elif mode == "split_view":
        categories = {
            "color_light": [kw for kw in type_data["keywords"] if any(
                w in kw.lower() for w in ["color", "ruby", "gold", "amber", "pale",
                                           "deep", "opaque", "transluc", "crystal",
                                           "inky", "garnet", "brick", "purple", "straw"])],
            "texture_structure": [kw for kw in type_data["keywords"] if any(
                w in kw.lower() for w in ["texture", "silk", "chalk", "velvet", "dense",
                                           "grip", "taut", "weight", "mousse", "viscous",
                                           "crisp", "unctuous", "fine"])],
            "aroma_complexity": [kw for kw in type_data["keywords"] if any(
                w in kw.lower() for w in ["aroma", "fruit", "herb", "spice", "pepper",
                                           "smoke", "truffle", "honey", "toast", "leather",
                                           "cherry", "citrus", "rose", "tar", "ginger",
                                           "apricot", "biscuit"])],
            "atmosphere_mood": [kw for kw in type_data["keywords"] if any(
                w in kw.lower() for w in ["noble", "primal", "elegant", "power", "wild",
                                           "intimate", "celebrat", "austere", "lush",
                                           "luminous", "precise", "dynamic", "volcanic",
                                           "restrain", "sophisticat"])]
        }
        # Catch any keywords not classified
        classified = set()
        for cat_kws in categories.values():
            classified.update(cat_kws)
        uncategorized = [kw for kw in type_data["keywords"] if kw not in classified]
        if uncategorized:
            categories["general"] = uncategorized

        split_prompts = {}
        for cat_name, cat_kws in categories.items():
            if cat_kws:
                parts = []
                if style_modifier:
                    parts.append(style_modifier)
                parts.extend(cat_kws)
                split_prompts[cat_name] = ", ".join(parts)

        return json.dumps({
            "mode": "split_view",
            "prompts": split_prompts,
            "nearest_type": nearest_type,
            "distance": round(distance, 4),
            "source_state": {p: round(coords.get(p, 0.0), 4) for p in WINE_PARAMETER_NAMES}
        }, indent=2)

    return json.dumps({"error": f"Unknown mode '{mode}'. Use 'composite' or 'split_view'."})


@mcp.tool()
def generate_wine_tasting_sequence_prompts(
    preset_name: str,
    keyframe_count: int = 4,
    style_modifier: str = ""
) -> str:
    """
    Generate keyframe prompts from a rhythmic preset.

    Layer 2: Deterministic keyframe extraction (0 tokens)

    Extracts evenly-spaced keyframes from a rhythmic oscillation
    and generates an image prompt for each. Useful for storyboards,
    animation keyframes, and multi-panel visualizations.

    Args:
        preset_name: One of the 5 rhythmic presets
        keyframe_count: Number of keyframes to extract (default: 4)
        style_modifier: Optional style prefix for all prompts

    Returns:
        Keyframes with step index, state, prompt, and vocabulary.
    """
    if preset_name not in WINE_RHYTHMIC_PRESETS:
        return json.dumps({"error": f"Unknown preset '{preset_name}'",
                           "available": list(WINE_RHYTHMIC_PRESETS.keys())})

    sequence = _generate_wine_preset_sequence(preset_name)
    total = len(sequence)

    # Extract evenly-spaced keyframes
    if keyframe_count >= total:
        indices = list(range(total))
    else:
        indices = [int(i * total / keyframe_count) for i in range(keyframe_count)]

    keyframes = []
    for idx in indices:
        step_data = sequence[idx]
        state = step_data["state"]
        nearest_type, dist = _find_nearest_wine_visual_type(state)
        type_data = WINE_VISUAL_TYPES[nearest_type]

        parts = []
        if style_modifier:
            parts.append(style_modifier)
        parts.extend(type_data["keywords"])
        opt = type_data["optical_properties"]
        parts.append(f"{opt['finish']} finish")
        prompt = ", ".join(parts)

        keyframes.append({
            "step": step_data["step"],
            "phase": step_data["phase"],
            "blend_factor": step_data["blend_factor"],
            "state": state,
            "nearest_visual_type": nearest_type,
            "distance": round(dist, 4),
            "prompt": prompt
        })

    return json.dumps({
        "preset": preset_name,
        "period": WINE_RHYTHMIC_PRESETS[preset_name]["steps_per_cycle"],
        "keyframe_count": len(keyframes),
        "keyframes": keyframes
    }, indent=2)


@mcp.tool()
def get_wine_tasting_server_info() -> str:
    """
    Get information about the Wine Tasting Visual Vocabulary MCP server.

    Returns server metadata, capabilities, and phase status.
    """
    return json.dumps({
        "server": "Wine Tasting Visual Vocabulary",
        "version": "2.6.0",
        "description": "Oenological expertise translated into visual parameters for image generation",
        "methodology": "Court of Master Sommeliers + WSET frameworks",
        "capabilities": {
            "layer_1_taxonomy": {
                "wine_types": len(WINE_VISUAL_TYPES),
                "varietal_count": len(Varietal),
                "aroma_clusters": len(AROMA_CLUSTERS),
                "tools": [
                    "get_wine_tasting_types",
                    "get_wine_tasting_specifications",
                    "get_varietal_list",
                    "get_aroma_clusters"
                ]
            },
            "layer_2_computation": {
                "parameter_dimensions": len(WINE_PARAMETER_NAMES),
                "parameter_names": WINE_PARAMETER_NAMES,
                "canonical_states": len(WINE_TASTING_COORDS),
                "tools": [
                    "map_wine_tasting_parameters",
                    "compute_wine_tasting_distance",
                    "compute_wine_tasting_trajectory",
                    "generate_wine_tasting_rhythmic_sequence",
                    "extract_wine_tasting_visual_vocabulary",
                    "generate_wine_tasting_prompt",
                    "generate_wine_tasting_sequence_prompts"
                ]
            },
            "layer_3_synthesis": {
                "tools": [
                    "generate_wine_visual_vocabulary",
                    "evolution_sequence",
                    "compare_wine_profiles",
                    "create_regional_preset"
                ]
            },
            "strategy_analysis": {
                "tools": ["analyze_strategy_document_tool"],
                "methodology": "deterministic_pattern_matching",
                "llm_cost": 0
            }
        },
        "phase_2_6_enhancements": {
            "rhythmic_presets": True,
            "preset_count": len(WINE_RHYTHMIC_PRESETS),
            "presets": {
                name: {
                    "period": p["steps_per_cycle"],
                    "pattern": p["pattern"],
                    "states": f"{p['state_a']} ↔ {p['state_b']}"
                }
                for name, p in WINE_RHYTHMIC_PRESETS.items()
            },
            "periods": sorted(set(p["steps_per_cycle"] for p in WINE_RHYTHMIC_PRESETS.values()))
        },
        "phase_2_7_enhancements": {
            "attractor_visualization": True,
            "visual_type_count": len(WINE_VISUAL_TYPES),
            "visual_types": list(WINE_VISUAL_TYPES.keys()),
            "prompt_modes": ["composite", "split_view"],
            "keyframe_generation": True
        },
        "domain_integration": {
            "domain_id": "wine_tasting",
            "parameter_names": WINE_PARAMETER_NAMES,
            "preset_periods": sorted(set(p["steps_per_cycle"] for p in WINE_RHYTHMIC_PRESETS.values())),
            "canonical_state_ids": list(WINE_TASTING_COORDS.keys()),
            "compatible_with": "aesthetic-dynamics-core, composition-graph-mcp"
        }
    }, indent=2)


# ============================================================================
# STRATEGY ANALYSIS (Tomographic Domain Projection) - original tools below
# ============================================================================

@mcp.tool()
def analyze_strategy_document_tool(strategy_text: str) -> str:
    """
    Analyze a strategy document through wine tasting compositional principles.

    This is the tomographic domain projection tool - it projects strategic
    text through wine tasting vocabulary to detect structural patterns.

    Zero LLM cost - pure deterministic pattern matching.

    Args:
        strategy_text: Full text of the strategy document to analyze

    Returns:
        JSON string with domain projection results including:
        - domain: "wine_tasting"
        - findings: List of detected patterns with dimensions, confidence, evidence
        - total_findings: Count of findings
        - methodology: "deterministic_pattern_matching"
        - llm_cost_tokens: 0

    Example:
        result = analyze_strategy_document_tool(strategy_pdf_text)
        Returns findings like:
        {
          "domain": "wine_tasting",
          "findings": [
            {
              "dimension": "balance_integration",
              "pattern": "acidic_harsh",
              "confidence": 0.75,
              "evidence": ["conflict", "tension", "harsh"],
              "categorical_family": "constraints"
            }
          ],
          "total_findings": 4,
          "llm_cost_tokens": 0
        }
    """
    import json
    result = analyze_strategy_document(strategy_text)
    return json.dumps(result, indent=2)


# Run the server
if __name__ == "__main__":
    mcp.run()
