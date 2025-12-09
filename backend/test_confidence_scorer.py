"""
Quick test to verify confidence scorer word boundary matching.
Run with: python -m pytest test_confidence_scorer.py -v
"""

from app.services.confidence_scorer import ConfidenceScorer


def test_nike_vs_jannike():
    """Test that 'Nike' doesn't match 'Jannike' (word boundary bug fix)."""
    scorer = ConfidenceScorer()

    # Test case 1: "Jannike wedge NEW" should NOT match "Nike"
    jannike_product = {
        "name": "Jannike wedge NEW",
        "type": "Wedge",
        "color": "Black",
        "department": "Shoes",
        "product_group_name": "Shoes",
        "garment_group_name": "Shoes",
        "index_name": "Divided",
        "perceived_colour_master_name": "Black",
        "perceived_colour_value_name": "Dark"
    }

    parsed_query = {
        "keywords": ["Nike", "running", "shoes"],
        "attributes": {
            "brand": "Nike",
            "type": "shoes",
            "color": None,
            "style": "running"
        }
    }

    score = scorer.score_product(jannike_product, parsed_query)

    print(f"\n🧪 Test: 'Jannike wedge NEW' vs 'Nike running shoes'")
    print(f"   Score: {score}")
    print(f"   Expected: < 0.5 (should be low since no real match)")

    # Should be very low score since:
    # - Brand: "Nike" should NOT match "Jannike" (word boundary)
    # - Type: "shoes" might partially match
    # - No color specified
    assert score < 0.5, f"Score {score} is too high! 'Nike' should not match 'Jannike'"
    print("   ✅ PASS: Word boundary matching working correctly!\n")


def test_nike_actual_match():
    """Test that actual Nike shoes get high scores."""
    scorer = ConfidenceScorer()

    # Test case 2: Actual Nike running shoes should get high score
    nike_product = {
        "name": "Nike Running Shoes Elite",
        "type": "Shoes",
        "color": "Black",
        "department": "Sport",
        "product_group_name": "Shoes",
        "garment_group_name": "Shoes",
        "index_name": "Nike",
        "perceived_colour_master_name": "Black",
        "perceived_colour_value_name": "Dark"
    }

    parsed_query = {
        "keywords": ["Nike", "running", "shoes"],
        "attributes": {
            "brand": "Nike",
            "type": "shoes",
            "color": None,
            "style": "running"
        }
    }

    score = scorer.score_product(nike_product, parsed_query)

    print(f"🧪 Test: 'Nike Running Shoes Elite' vs 'Nike running shoes'")
    print(f"   Score: {score}")
    print(f"   Expected: > 0.8 (should be very high match)")

    # Should be high score since:
    # - Brand: "Nike" matches "Nike" in name (1.0)
    # - Type: "shoes" matches "Shoes" (1.0)
    # - Name has "running" keyword
    assert score > 0.8, f"Score {score} is too low! Real Nike shoes should score high"
    print("   ✅ PASS: Actual Nike shoes get high score!\n")


def test_word_boundary_helper():
    """Test the word boundary helper function directly."""
    scorer = ConfidenceScorer()

    print("🧪 Test: Word boundary helper function")

    # Should NOT match
    assert not scorer._contains_word("Jannike wedge", "Nike"), "❌ 'Nike' should NOT be in 'Jannike'"
    assert not scorer._contains_word("running-shoes", "shoe"), "❌ 'shoe' should NOT be in 'running-shoes'"

    # Should match
    assert scorer._contains_word("Nike shoes", "Nike"), "❌ 'Nike' should be in 'Nike shoes'"
    assert scorer._contains_word("running shoes", "running"), "❌ 'running' should be in 'running shoes'"
    assert scorer._contains_word("Nike Running Shoes", "Nike"), "❌ 'Nike' should be in 'Nike Running Shoes'"
    assert scorer._contains_word("NIKE SHOES", "nike"), "❌ Case insensitive should work"

    print("   ✅ PASS: Word boundary matching works correctly!\n")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Testing Confidence Scorer - Word Boundary Fix")
    print("="*60)

    test_word_boundary_helper()
    test_nike_vs_jannike()
    test_nike_actual_match()

    print("="*60)
    print("✅ All tests passed!")
    print("="*60 + "\n")
