"""
Example usage of Wine Tasting Visual Vocabulary MCP Server

This script demonstrates all the tools and common workflows.
"""

import server
import json

# Helper to call wrapped MCP functions
def call_tool(tool_name, *args, **kwargs):
    """Helper to call FastMCP-wrapped tools"""
    tool = getattr(server, tool_name)
    return tool.fn(*args, **kwargs)

# Create convenience wrappers
generate_wine_visual_vocabulary = lambda *args, **kwargs: call_tool('generate_wine_visual_vocabulary', *args, **kwargs)
compare_wine_profiles = lambda *args, **kwargs: call_tool('compare_wine_profiles', *args, **kwargs)
get_varietal_list = lambda *args, **kwargs: call_tool('get_varietal_list', *args, **kwargs)
get_aroma_clusters = lambda *args, **kwargs: call_tool('get_aroma_clusters', *args, **kwargs)
create_regional_preset = lambda *args, **kwargs: call_tool('create_regional_preset', *args, **kwargs)
evolution_sequence = lambda *args, **kwargs: call_tool('evolution_sequence', *args, **kwargs)


def print_section(title):
    """Print formatted section header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")


def example_1_basic_burgundy_pinot():
    """Generate visual vocabulary for classic Burgundy Pinot Noir"""
    print_section("Example 1: Classic Burgundy Pinot Noir")
    
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
    
    print("INPUT: Mature Burgundy Pinot Noir")
    print("  - Cool climate, Old World, French oak")
    print("  - High acidity (7.5), Moderate tannin (6.0)")
    print("  - Cherry, mushroom, rose aromatics")
    print()
    
    print("VISUAL VOCABULARY OUTPUT:")
    print(f"  Color: {result['base_color']['description']}")
    print(f"  Age modification: {result['base_color']['age_modified']}")
    print(f"  Opacity: {result['opacity_clarity']['base_opacity']}")
    print(f"  Texture: {result['texture_surface']['base_texture']}")
    print(f"  Structure: {result['texture_surface']['structure']}")
    print(f"  Composition: {result['compositional_structure']['base_composition']}")
    print(f"  Visual tension: {result['balance_relationships']['visual_tension']}")
    print(f"  Visual weight: {result['balance_relationships']['visual_weight']}")
    print(f"  Atmosphere: {result['atmospheric_qualities']['style_atmosphere']}")
    print()
    
    print("IMAGE GENERATION PROMPT:")
    print(f"  Create an image with {result['base_color']['description']} color,")
    print(f"  {result['texture_surface']['base_texture']} texture,")
    print(f"  {result['compositional_structure']['base_composition']} composition,")
    print(f"  {result['atmospheric_qualities']['climate_atmosphere']} atmosphere,")
    print(f"  with {result['compositional_structure']['edge_quality']} edges")


def example_2_bold_napa_cabernet():
    """Generate visual vocabulary for bold Napa Cabernet"""
    print_section("Example 2: Bold Napa Valley Cabernet Sauvignon")
    
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
    
    print("INPUT: Young Napa Cabernet Sauvignon")
    print("  - Warm climate, New World, American oak")
    print("  - High tannin (8.5), High alcohol (8.5), Full body (9.0)")
    print("  - Blackcurrant, vanilla, cedar aromatics")
    print()
    
    print("VISUAL VOCABULARY OUTPUT:")
    print(f"  Color: {result['base_color']['description']}")
    print(f"  Opacity: {result['opacity_clarity']['base_opacity']}")
    print(f"  Texture: {result['texture_surface']['base_texture']}")
    print(f"  Structure: {result['texture_surface']['structure']}")
    print(f"  Visual weight: {result['balance_relationships']['visual_weight']}")
    print(f"  Oak influence: {result['texture_surface']['oak_overlay']}")
    print(f"  Finish: {result['finish_dimension']['descriptor']}")


def example_3_crisp_mosel_riesling():
    """Generate visual vocabulary for crystalline Mosel Riesling"""
    print_section("Example 3: Mosel Riesling - Crystalline Precision")
    
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
    
    print("INPUT: Young Mosel Riesling")
    print("  - Cool climate, No oak, High acidity (9.0)")
    print("  - Light body (4.0), Low alcohol (4.5)")
    print("  - Lime, slate, petrol aromatics")
    print()
    
    print("VISUAL VOCABULARY OUTPUT:")
    print(f"  Color: {result['base_color']['description']}")
    print(f"  Texture: {result['texture_surface']['base_texture']}")
    print(f"  Structure: {result['texture_surface']['structure']}")
    print(f"  Visual tension: {result['balance_relationships']['visual_tension']}")
    print(f"  Climate modifier: {result['texture_surface']['climate_modifier']}")
    print(f"  Composition: {result['compositional_structure']['base_composition']}")


def example_4_regional_presets():
    """Demonstrate regional preset usage"""
    print_section("Example 4: Regional Presets")
    
    regions = [
        "burgundy_red",
        "napa_cabernet", 
        "barolo",
        "mosel_riesling"
    ]
    
    for region in regions:
        result = create_regional_preset(region)
        
        print(f"{region.upper().replace('_', ' ')}:")
        print(f"  Varietal: {result['metadata']['varietal']}")
        print(f"  Climate: {result['metadata']['climate']}")
        print(f"  Style: {result['metadata']['winemaking_style']}")
        print(f"  Visual signature: {result['compositional_structure']['base_composition']}")
        print()


def example_5_evolution_sequence():
    """Show wine evolution over time"""
    print_section("Example 5: Wine Evolution - Pinot Noir Through Time")
    
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
    
    ages = ["youthful", "developing", "mature", "past_prime"]
    
    for age in ages:
        wine = result["evolution_sequence"][age]
        
        print(f"{age.upper()}:")
        print(f"  Color: {wine['base_color']['age_modified']}")
        print(f"  Clarity: {wine['opacity_clarity']['clarity']}")
        print(f"  Texture state: {wine['texture_surface']['age_state']}")
        print(f"  Integration: {wine['compositional_structure']['integration']}")
        print(f"  Aromatics: {wine['aromatic_descriptors']['aroma_category']}")
        print(f"  Time signature: {wine['atmospheric_qualities']['time_signature']}")
        print()
    
    print("KEY TRANSFORMATIONS:")
    for key, value in result["key_transformations"].items():
        print(f"  {key}: {value}")


def example_6_comparison():
    """Compare two different wines"""
    print_section("Example 6: Comparing Pinot Noir vs Cabernet Sauvignon")
    
    result = compare_wine_profiles(
        wine1_params={
            "varietal": "pinot_noir",
            "climate": "cool",
            "winemaking_style": "old_world",
            "age": "mature",
            "body": 5.5,
            "tannin": 6.0,
            "acidity": 7.5
        },
        wine2_params={
            "varietal": "cabernet_sauvignon",
            "climate": "warm",
            "winemaking_style": "new_world",
            "age": "youthful",
            "body": 9.0,
            "tannin": 8.5,
            "acidity": 5.5
        }
    )
    
    print("BURGUNDY PINOT NOIR vs NAPA CABERNET:")
    print()
    
    print("COLOR CONTRAST:")
    print(f"  Pinot: {result['color_contrast']['wine1']['description']}")
    print(f"  Cabernet: {result['color_contrast']['wine2']['description']}")
    print(f"  Difference: {result['color_contrast']['difference']}")
    print()
    
    print("TEXTURE CONTRAST:")
    print(f"  Pinot: {result['texture_contrast']['wine1']}")
    print(f"  Cabernet: {result['texture_contrast']['wine2']}")
    print()
    
    print("WEIGHT CONTRAST:")
    print(f"  Pinot: {result['weight_contrast']['wine1']}")
    print(f"  Cabernet: {result['weight_contrast']['wine2']}")
    print()
    
    print("BALANCE COMPARISON:")
    print(f"  Pinot tension: {result['balance_comparison']['wine1_tension']}")
    print(f"  Cabernet tension: {result['balance_comparison']['wine2_tension']}")


def example_7_aroma_exploration():
    """Explore aroma clusters and their visual mappings"""
    print_section("Example 7: Aroma Cluster Visual Mappings")
    
    clusters = get_aroma_clusters()
    
    featured_clusters = ["red_fruit", "black_fruit", "earth_mineral", "oak_spice"]
    
    for cluster_name in featured_clusters:
        cluster = clusters[cluster_name]
        
        print(f"{cluster_name.upper().replace('_', ' ')}:")
        print(f"  Notes: {', '.join(cluster['notes'][:5])}")
        print(f"  Brightness: {cluster['brightness']}")
        print(f"  Texture: {cluster['texture']}")
        print(f"  Color palette: {cluster['color_palette'][:3]}")
        print()


def example_8_varietal_reference():
    """Show all available varietals"""
    print_section("Example 8: Available Varietals Reference")
    
    varietals = get_varietal_list()
    
    print("RED VARIETALS:")
    reds = [
        "pinot_noir", "cabernet_sauvignon", "merlot", 
        "syrah", "nebbiolo", "tempranillo"
    ]
    for varietal in reds:
        if varietal in varietals:
            v = varietals[varietal]
            print(f"  {varietal.replace('_', ' ').title()}: {v['texture']}, {v['structure']}")
    
    print("\nWHITE VARIETALS:")
    whites = [
        "chardonnay", "sauvignon_blanc", "riesling",
        "viognier", "pinot_grigio"
    ]
    for varietal in whites:
        if varietal in varietals:
            v = varietals[varietal]
            print(f"  {varietal.replace('_', ' ').title()}: {v['texture']}, {v['structure']}")


def example_9_balance_exploration():
    """Show how balance parameters affect visuals"""
    print_section("Example 9: Balance Parameters - Visual Impact")
    
    # High acid, high tannin - angular and tense
    high_tension = generate_wine_visual_vocabulary(
        varietal="nebbiolo",
        acidity=9.0,
        tannin=9.0,
        body=7.0
    )
    
    # Low acid, low tannin - soft and relaxed
    low_tension = generate_wine_visual_vocabulary(
        varietal="grenache",
        acidity=4.0,
        tannin=4.0,
        body=7.0
    )
    
    print("HIGH TENSION (High Acid + High Tannin - Nebbiolo):")
    print(f"  Visual tension: {high_tension['balance_relationships']['visual_tension']}")
    print(f"  Texture: {high_tension['texture_surface']['structure']}")
    print(f"  Edge quality: {high_tension['compositional_structure']['edge_quality']}")
    print()
    
    print("LOW TENSION (Low Acid + Low Tannin - Grenache):")
    print(f"  Visual tension: {low_tension['balance_relationships']['visual_tension']}")
    print(f"  Texture: {low_tension['texture_surface']['structure']}")
    print(f"  Edge quality: {low_tension['compositional_structure']['edge_quality']}")


def example_10_finish_dimension():
    """Demonstrate finish length impact on visuals"""
    print_section("Example 10: Finish Length - Atmospheric Depth")
    
    finish_lengths = ["short", "medium", "long", "very_long"]
    
    for finish in finish_lengths:
        result = generate_wine_visual_vocabulary(
            varietal="cabernet_sauvignon",
            finish_length=finish
        )
        
        print(f"{finish.upper()} FINISH:")
        print(f"  Descriptor: {result['finish_dimension']['descriptor']}")
        print(f"  Atmospheric depth: {result['atmospheric_qualities']['finish_depth']}")
        print(f"  Fade pattern: {result['atmospheric_qualities']['fade_pattern']}")
        print()


if __name__ == "__main__":
    print("\n")
    print("*" * 80)
    print("  WINE TASTING VISUAL VOCABULARY MCP SERVER")
    print("  Example Usage Demonstrations")
    print("*" * 80)
    
    # Run all examples
    example_1_basic_burgundy_pinot()
    example_2_bold_napa_cabernet()
    example_3_crisp_mosel_riesling()
    example_4_regional_presets()
    example_5_evolution_sequence()
    example_6_comparison()
    example_7_aroma_exploration()
    example_8_varietal_reference()
    example_9_balance_exploration()
    example_10_finish_dimension()
    
    print("\n" + "="*80)
    print("  Examples complete!")
    print("="*80 + "\n")
