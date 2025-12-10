"""
Test suite for Wine Tasting Visual Vocabulary MCP Server

Tests categorical properties, morphism preservation, and coherence constraints.
"""

import pytest
import asyncio
import server
from server import (
    Varietal,
    ClimateType,
    WinemakingStyle,
    OakTreatment,
    AgeCategory,
    BalanceProfile,
    VARIETAL_CHARACTERISTICS,
    CLIMATE_MODIFIERS,
    AROMA_CLUSTERS
)

# Helper to call wrapped MCP functions synchronously for testing
def call_tool(tool_name, *args, **kwargs):
    """Helper to call FastMCP-wrapped tools synchronously in tests"""
    tool = getattr(server, tool_name)
    return tool.fn(*args, **kwargs)

# Create convenience wrappers for tests
def generate_wine_visual_vocabulary(*args, **kwargs):
    return call_tool('generate_wine_visual_vocabulary', *args, **kwargs)

def compare_wine_profiles(*args, **kwargs):
    return call_tool('compare_wine_profiles', *args, **kwargs)

def get_varietal_list(*args, **kwargs):
    return call_tool('get_varietal_list', *args, **kwargs)

def get_aroma_clusters(*args, **kwargs):
    return call_tool('get_aroma_clusters', *args, **kwargs)

def create_regional_preset(*args, **kwargs):
    return call_tool('create_regional_preset', *args, **kwargs)

def evolution_sequence(*args, **kwargs):
    return call_tool('evolution_sequence', *args, **kwargs)


class TestVarietalFunctor:
    """Test that varietal functor preserves expected structure"""
    
    def test_all_varietals_have_complete_characteristics(self):
        """Every varietal must have all required attributes"""
        required_keys = [
            "color_base", "color_hue", "opacity", "texture",
            "structure", "visual_weight", "characteristic_notes",
            "edge_quality", "composition"
        ]
        
        for varietal in Varietal:
            char = VARIETAL_CHARACTERISTICS.get(varietal)
            assert char is not None, f"Missing characteristics for {varietal.value}"
            
            for key in required_keys:
                assert key in char, f"Missing {key} for {varietal.value}"
    
    def test_red_vs_white_opacity_patterns(self):
        """Red wines generally more opaque than whites"""
        red_varietals = [
            Varietal.CABERNET_SAUVIGNON,
            Varietal.SYRAH,
            Varietal.MERLOT
        ]
        
        white_varietals = [
            Varietal.SAUVIGNON_BLANC,
            Varietal.RIESLING,
            Varietal.PINOT_GRIGIO
        ]
        
        avg_red_opacity = sum(
            VARIETAL_CHARACTERISTICS[v]["opacity"] for v in red_varietals
        ) / len(red_varietals)
        
        avg_white_opacity = sum(
            VARIETAL_CHARACTERISTICS[v]["opacity"] for v in white_varietals
        ) / len(white_varietals)
        
        # Reds can be equally or more opaque, but never significantly less
        assert avg_red_opacity >= avg_white_opacity * 0.9
    
    def test_pinot_noir_delicacy(self):
        """Pinot Noir should have characteristically light structure"""
        pinot_char = VARIETAL_CHARACTERISTICS[Varietal.PINOT_NOIR]
        
        assert pinot_char["opacity"] < 0.7, "Pinot should be translucent"
        assert "delicate" in pinot_char["texture"].lower() or \
               "silky" in pinot_char["texture"].lower()
        assert "light" in pinot_char["visual_weight"].lower() or \
               "ethereal" in pinot_char["visual_weight"].lower()
    
    def test_cabernet_boldness(self):
        """Cabernet Sauvignon should have bold, structured characteristics"""
        cab_char = VARIETAL_CHARACTERISTICS[Varietal.CABERNET_SAUVIGNON]
        
        assert cab_char["opacity"] > 0.85, "Cabernet should be opaque"
        assert "structured" in cab_char["texture"].lower() or \
               "firm" in cab_char["texture"].lower()
        assert "full" in cab_char["visual_weight"].lower()


class TestClimateFunctor:
    """Test that climate transformations preserve coherence"""
    
    def test_climate_saturation_progression(self):
        """Warmer climates should increase saturation"""
        climates_ordered = [
            ClimateType.COOL,
            ClimateType.MODERATE,
            ClimateType.WARM,
            ClimateType.HOT
        ]
        
        saturations = [
            CLIMATE_MODIFIERS[climate]["saturation_adjust"]
            for climate in climates_ordered
        ]
        
        # Should be monotonically increasing
        for i in range(len(saturations) - 1):
            assert saturations[i] <= saturations[i + 1]
    
    def test_cool_climate_characteristics(self):
        """Cool climate should create angular, tense characteristics"""
        cool_mod = CLIMATE_MODIFIERS[ClimateType.COOL]
        
        assert cool_mod["saturation_adjust"] < 0
        assert cool_mod["brightness_adjust"] >= 0
        assert "angular" in cool_mod["texture_modifier"].lower() or \
               "tense" in cool_mod["texture_modifier"].lower() or \
               "crisp" in cool_mod["texture_modifier"].lower()
    
    def test_warm_climate_characteristics(self):
        """Warm climate should create soft, relaxed characteristics"""
        warm_mod = CLIMATE_MODIFIERS[ClimateType.WARM]
        
        assert warm_mod["saturation_adjust"] > 0
        assert "soft" in warm_mod["texture_modifier"].lower() or \
               "relaxed" in warm_mod["atmosphere"].lower()


class TestAgeFunctor:
    """Test temporal evolution preserves categorical structure"""
    
    def test_age_color_evolution_reds(self):
        """Red wines should progress purple → garnet → brick → brown"""
        youthful = "purple ruby"
        developing = "garnet ruby-brick"
        mature = "brick garnet tawny"
        past_prime = "brown tawny"
        
        # Simplified check that color descriptors evolve appropriately
        from server import AGE_TRANSFORMATIONS
        
        assert "purple" in AGE_TRANSFORMATIONS[AgeCategory.YOUTHFUL]["red_color_shift"].lower() or \
               "ruby" in AGE_TRANSFORMATIONS[AgeCategory.YOUTHFUL]["red_color_shift"].lower()
        
        assert "brick" in AGE_TRANSFORMATIONS[AgeCategory.MATURE]["red_color_shift"].lower() or \
               "tawny" in AGE_TRANSFORMATIONS[AgeCategory.MATURE]["red_color_shift"].lower()
    
    def test_age_integration_progression(self):
        """Wine should become more integrated with age"""
        from server import AGE_TRANSFORMATIONS
        
        youthful_integration = AGE_TRANSFORMATIONS[AgeCategory.YOUTHFUL]["integration"]
        mature_integration = AGE_TRANSFORMATIONS[AgeCategory.MATURE]["integration"]
        
        assert "separate" in youthful_integration.lower() or \
               "distinct" in youthful_integration.lower()
        
        assert "seamless" in mature_integration.lower() or \
               "unified" in mature_integration.lower() or \
               "complete" in mature_integration.lower()
    
    def test_clarity_degradation(self):
        """Clarity should degrade: brilliant → bright → clear → dull"""
        from server import AGE_TRANSFORMATIONS
        
        clarity_sequence = [
            AGE_TRANSFORMATIONS[age]["visual_clarity"]
            for age in [AgeCategory.YOUTHFUL, AgeCategory.DEVELOPING, 
                       AgeCategory.MATURE, AgeCategory.PAST_PRIME]
        ]
        
        assert "brilliant" in clarity_sequence[0].lower() or \
               "star-bright" in clarity_sequence[0].lower()
        
        assert "dull" in clarity_sequence[-1].lower() or \
               "fading" in clarity_sequence[-1].lower()


class TestBalanceMorphism:
    """Test that balance relationships create coherent visual parameters"""
    
    def test_high_acidity_creates_tension(self):
        """High acidity should create angular, taut visual qualities"""
        high_acid = BalanceProfile(
            acidity=9.0,
            tannin=5.0,
            sweetness=2.0,
            alcohol=5.0,
            body=5.0
        )
        
        tension = high_acid.get_visual_tension()
        assert "high" in tension.lower() or "angular" in tension.lower() or \
               "taut" in tension.lower()
    
    def test_low_acidity_creates_softness(self):
        """Low acidity should create soft, relaxed visual qualities"""
        low_acid = BalanceProfile(
            acidity=3.0,
            tannin=3.0,
            sweetness=2.0,
            alcohol=5.0,
            body=5.0
        )
        
        tension = low_acid.get_visual_tension()
        assert "low" in tension.lower() or "soft" in tension.lower() or \
               "relaxed" in tension.lower()
    
    def test_high_body_creates_density(self):
        """High body and alcohol should create visual weight"""
        full_bodied = BalanceProfile(
            acidity=5.0,
            tannin=5.0,
            sweetness=2.0,
            alcohol=9.0,
            body=9.0
        )
        
        weight = full_bodied.get_visual_weight()
        assert "full" in weight.lower() or "dense" in weight.lower() or \
               "heavy" in weight.lower()
    
    def test_light_body_creates_transparency(self):
        """Low body and alcohol should create light visual weight"""
        light_bodied = BalanceProfile(
            acidity=5.0,
            tannin=5.0,
            sweetness=2.0,
            alcohol=3.0,
            body=3.0
        )
        
        weight = light_bodied.get_visual_weight()
        assert "light" in weight.lower() or "ethereal" in weight.lower() or \
               "transparent" in weight.lower()


class TestComposition:
    """Test that multiple functors compose correctly"""
    
    def test_basic_vocabulary_generation(self):
        """Test that vocabulary generation succeeds with valid parameters"""
        result = generate_wine_visual_vocabulary(
            varietal="pinot_noir",
            climate="cool",
            winemaking_style="old_world",
            oak_treatment="french_oak",
            age="developing"
        )
        
        assert "error" not in result
        assert "base_color" in result
        assert "texture_surface" in result
        assert "compositional_structure" in result
        assert "balance_relationships" in result
    
    def test_burgundy_pinot_composition(self):
        """Classic Burgundy Pinot should have expected characteristics"""
        result = generate_wine_visual_vocabulary(
            varietal="pinot_noir",
            climate="cool",
            winemaking_style="old_world",
            oak_treatment="french_oak",
            age="mature",
            acidity=7.5,
            tannin=6.0,
            body=5.5
        )
        
        # Should be translucent
        assert result["opacity_clarity"]["base_opacity"] < 0.7
        
        # Should have delicate texture
        texture = result["texture_surface"]["base_texture"]
        assert "delicate" in texture.lower() or "silky" in texture.lower()
        
        # Cool climate should add angular quality
        climate_mod = result["texture_surface"]["climate_modifier"]
        assert "angular" in climate_mod.lower() or "crisp" in climate_mod.lower()
    
    def test_napa_cabernet_composition(self):
        """Bold Napa Cabernet should have power and density"""
        result = generate_wine_visual_vocabulary(
            varietal="cabernet_sauvignon",
            climate="warm",
            winemaking_style="new_world",
            oak_treatment="american_oak",
            age="youthful",
            acidity=5.5,
            tannin=8.5,
            body=9.0,
            alcohol=8.5
        )
        
        # Should be opaque
        assert result["opacity_clarity"]["base_opacity"] > 0.85
        
        # Should have full visual weight
        assert "full" in result["opacity_clarity"]["visual_weight"].lower()
        
        # New World should be fruit-forward
        aesthetic = result["compositional_structure"]["style_aesthetic"]
        assert "fruit-forward" in aesthetic.lower() or "bold" in aesthetic.lower()
    
    def test_invalid_varietal_handling(self):
        """Invalid varietal should return error"""
        result = generate_wine_visual_vocabulary(
            varietal="invalid_grape",
            climate="cool"
        )
        
        assert "error" in result


class TestRegionalPresets:
    """Test that regional presets produce expected characteristics"""
    
    def test_burgundy_red_preset(self):
        """Burgundy red should be Pinot Noir with cool climate"""
        result = create_regional_preset("burgundy_red")
        
        assert "error" not in result
        assert result["metadata"]["varietal"] == "pinot_noir"
        assert result["metadata"]["climate"] == "cool"
        assert result["metadata"]["winemaking_style"] == "old_world"
    
    def test_napa_cabernet_preset(self):
        """Napa Cabernet should be warm climate New World"""
        result = create_regional_preset("napa_cabernet")
        
        assert "error" not in result
        assert result["metadata"]["varietal"] == "cabernet_sauvignon"
        assert result["metadata"]["climate"] == "warm"
        assert result["metadata"]["winemaking_style"] == "new_world"
    
    def test_mosel_riesling_preset(self):
        """Mosel Riesling should be cool, no oak, high acidity"""
        result = create_regional_preset("mosel_riesling")
        
        assert "error" not in result
        assert result["metadata"]["varietal"] == "riesling"
        assert result["metadata"]["climate"] == "cool"
        assert result["metadata"]["oak_treatment"] == "none"
        assert result["balance_relationships"]["acidity"] >= 8.0
    
    def test_invalid_region_handling(self):
        """Invalid region should return error with available options"""
        result = create_regional_preset("invalid_region")
        
        assert "error" in result
        assert "available_regions" in result


class TestEvolutionSequence:
    """Test temporal transformation sequences"""
    
    def test_evolution_sequence_structure(self):
        """Evolution sequence should have all age categories"""
        result = evolution_sequence(
            varietal="pinot_noir",
            climate="cool"
        )
        
        assert "evolution_sequence" in result
        assert "youthful" in result["evolution_sequence"]
        assert "developing" in result["evolution_sequence"]
        assert "mature" in result["evolution_sequence"]
        assert "past_prime" in result["evolution_sequence"]
    
    def test_color_evolution_in_sequence(self):
        """Color should evolve systematically through sequence"""
        result = evolution_sequence(
            varietal="pinot_noir",
            climate="cool"
        )
        
        youthful_color = result["evolution_sequence"]["youthful"]["base_color"]["age_modified"]
        mature_color = result["evolution_sequence"]["mature"]["base_color"]["age_modified"]
        
        # Youthful should have purple/ruby
        assert "purple" in youthful_color.lower() or "ruby" in youthful_color.lower()
        
        # Mature should have brick/garnet/tawny
        assert "brick" in mature_color.lower() or \
               "garnet" in mature_color.lower() or \
               "tawny" in mature_color.lower()
    
    def test_texture_integration_in_sequence(self):
        """Texture should integrate over time"""
        result = evolution_sequence(
            varietal="cabernet_sauvignon",
            climate="moderate",
            tannin=8.0
        )
        
        youthful_integration = result["evolution_sequence"]["youthful"]["compositional_structure"]["integration"]
        mature_integration = result["evolution_sequence"]["mature"]["compositional_structure"]["integration"]
        
        # Youthful should be separate/distinct
        assert "separate" in youthful_integration.lower() or \
               "distinct" in youthful_integration.lower()
        
        # Mature should be seamless/unified
        assert "seamless" in mature_integration.lower() or \
               "unified" in mature_integration.lower()


class TestComparison:
    """Test wine profile comparisons"""
    
    def test_compare_pinot_vs_cabernet(self):
        """Comparing Pinot vs Cabernet should show clear contrasts"""
        result = compare_wine_profiles(
            wine1_params={
                "varietal": "pinot_noir",
                "climate": "cool",
                "body": 5.0
            },
            wine2_params={
                "varietal": "cabernet_sauvignon",
                "climate": "warm",
                "body": 9.0
            }
        )
        
        assert "color_contrast" in result
        assert "texture_contrast" in result
        assert "weight_contrast" in result
    
    def test_compare_age_difference(self):
        """Same wine at different ages should show evolution"""
        result = compare_wine_profiles(
            wine1_params={
                "varietal": "pinot_noir",
                "age": "youthful"
            },
            wine2_params={
                "varietal": "pinot_noir",
                "age": "mature"
            }
        )
        
        assert "atmospheric_contrast" in result


class TestAromaClusters:
    """Test aroma cluster mappings"""
    
    def test_aroma_clusters_complete(self):
        """All aroma clusters should have required fields"""
        clusters = get_aroma_clusters()
        
        for cluster_name, cluster_data in clusters.items():
            assert "notes" in cluster_data
            assert "color_palette" in cluster_data
            assert "brightness" in cluster_data
            assert "texture" in cluster_data
            
            # Should have multiple colors
            assert len(cluster_data["color_palette"]) >= 2
    
    def test_red_vs_black_fruit_distinction(self):
        """Red and black fruit should have different palettes"""
        clusters = get_aroma_clusters()
        
        red_fruit_colors = set(clusters["red_fruit"]["color_palette"])
        black_fruit_colors = set(clusters["black_fruit"]["color_palette"])
        
        # Should be mostly distinct
        overlap = red_fruit_colors.intersection(black_fruit_colors)
        assert len(overlap) < len(red_fruit_colors) * 0.5


class TestVarietalList:
    """Test varietal listing functionality"""
    
    def test_get_varietal_list_structure(self):
        """Varietal list should include all supported varieties"""
        varietals = get_varietal_list()
        
        # Should have both reds and whites
        assert "pinot_noir" in varietals
        assert "cabernet_sauvignon" in varietals
        assert "chardonnay" in varietals
        assert "riesling" in varietals
    
    def test_varietal_list_completeness(self):
        """Each varietal should have expected information"""
        varietals = get_varietal_list()
        
        for varietal_name, varietal_info in varietals.items():
            assert "color" in varietal_info
            assert "texture" in varietal_info
            assert "structure" in varietal_info
            assert "notes" in varietal_info
            assert len(varietal_info["notes"]) > 0


class TestCoherenceConstraints:
    """Test that categorical coherence is maintained"""
    
    def test_oak_none_vs_french_distinction(self):
        """No oak vs French oak should show clear differences"""
        no_oak = generate_wine_visual_vocabulary(
            varietal="riesling",
            oak_treatment="none"
        )
        
        french_oak = generate_wine_visual_vocabulary(
            varietal="chardonnay",
            oak_treatment="french_oak"
        )
        
        no_oak_texture = no_oak["texture_surface"]["oak_overlay"]
        french_oak_texture = french_oak["texture_surface"]["oak_overlay"]
        
        assert "pure" in no_oak_texture.lower() or \
               "clean" in no_oak_texture.lower() or \
               "unadulterated" in no_oak_texture.lower()
        
        assert "silky" in french_oak_texture.lower() or \
               "refined" in french_oak_texture.lower() or \
               "vanilla" in french_oak["material_references"]["finish_quality"].lower()
    
    def test_finish_length_atmospheric_depth(self):
        """Finish length should affect atmospheric depth consistently"""
        short_finish = generate_wine_visual_vocabulary(
            varietal="pinot_noir",
            finish_length="short"
        )
        
        long_finish = generate_wine_visual_vocabulary(
            varietal="pinot_noir",
            finish_length="very_long"
        )
        
        short_depth = short_finish["atmospheric_qualities"]["finish_depth"]
        long_depth = long_finish["atmospheric_qualities"]["finish_depth"]
        
        assert "shallow" in short_depth.lower() or "immediate" in short_depth.lower()
        assert "deep" in long_depth.lower() or "vast" in long_depth.lower() or \
               "infinite" in long_depth.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
