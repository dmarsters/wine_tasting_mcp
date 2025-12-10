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
from typing import Dict, List, Optional, Literal
from dataclasses import dataclass
from enum import Enum

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
        for aroma in primary_aromas:
            # Find which cluster this aroma belongs to
            for cluster_name, cluster_data in AROMA_CLUSTERS.items():
                if aroma.lower() in cluster_data["notes"]:
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


# Run the server
if __name__ == "__main__":
    mcp.run()
