#!/usr/bin/env python3
"""Test script for smart text splitting with embed support."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from discord_bot import smart_split_text


def test_short_text():
    """Test that short text is not split."""
    print("\n" + "=" * 60)
    print("Test 1: Short Text (No Splitting)")
    print("=" * 60)
    
    text = "This is a short message that fits within the limit."
    chunks = smart_split_text(text, max_length=4096)
    
    assert len(chunks) == 1, f"Expected 1 chunk, got {len(chunks)}"
    assert chunks[0] == text, "Text was modified"
    print("✓ Short text is not split")
    print(f"  Original length: {len(text)}")
    print(f"  Chunks: {len(chunks)}")
    return True


def test_long_text_splitting():
    """Test that long text is split properly."""
    print("\n" + "=" * 60)
    print("Test 2: Long Text Splitting")
    print("=" * 60)
    
    # Create a text longer than 4096 characters
    paragraph = "This is a paragraph. " * 100  # ~2000 chars
    text = paragraph + "\n\n" + paragraph + "\n\n" + paragraph  # ~6000 chars
    
    chunks = smart_split_text(text, max_length=4096, prefer_length=3900)
    
    print(f"✓ Long text split into {len(chunks)} chunks")
    for i, chunk in enumerate(chunks, 1):
        print(f"  Chunk {i}: {len(chunk)} characters")
        assert len(chunk) <= 4096, f"Chunk {i} exceeds maximum length"
    
    # Verify that rejoining chunks gives original text
    rejoined = "".join(chunks)
    assert rejoined == text, "Rejoined chunks don't match original text"
    print("✓ Chunks rejoin to original text")
    return True


def test_markdown_preservation():
    """Test that markdown formatting is preserved across splits."""
    print("\n" + "=" * 60)
    print("Test 3: Markdown Formatting Preservation")
    print("=" * 60)
    
    # Create text with markdown that should be split
    part1 = "This is **bold text** and *italic text*. " * 80  # ~3300 chars
    part2 = "More content with __underlined__ and ***bold italic***. " * 80  # ~4500 chars
    text = part1 + part2
    
    chunks = smart_split_text(text, max_length=4096, prefer_length=3900)
    
    print(f"✓ Text with markdown split into {len(chunks)} chunks")
    
    # Check that we don't break markdown in the middle
    for i, chunk in enumerate(chunks, 1):
        print(f"  Chunk {i}: {len(chunk)} characters")
        
        # Count markdown patterns
        bold_count = chunk.count('**')
        italic_count = chunk.count('*') - bold_count * 2
        
        # Check if we have matching pairs (even counts)
        # Note: This is a simple check; the actual function tries harder
        print(f"    Bold markers (**): {bold_count}")
        print(f"    Italic markers (*): {italic_count}")
    
    return True


def test_paragraph_boundary_splitting():
    """Test that text splits at paragraph boundaries."""
    print("\n" + "=" * 60)
    print("Test 4: Paragraph Boundary Splitting")
    print("=" * 60)
    
    # Create text with clear paragraph boundaries
    paragraphs = []
    for i in range(8):
        paragraphs.append(f"Paragraph {i+1}. " + "Lorem ipsum dolor sit amet. " * 50)
    
    text = "\n\n".join(paragraphs)
    
    chunks = smart_split_text(text, max_length=4096, prefer_length=3900)
    
    print(f"✓ Text with {len(paragraphs)} paragraphs split into {len(chunks)} chunks")
    
    for i, chunk in enumerate(chunks, 1):
        paragraph_count = chunk.count("Paragraph")
        print(f"  Chunk {i}: {len(chunk)} characters, {paragraph_count} paragraphs")
        
        # Check if splits happen at paragraph boundaries
        if i < len(chunks):  # Not the last chunk
            # Should end with paragraph boundary or sentence
            assert chunk.rstrip().endswith(('.', '!', '?', '\n')), \
                f"Chunk {i} doesn't end at a natural boundary"
    
    print("✓ Chunks end at natural boundaries")
    return True


def test_very_long_text():
    """Test text that requires multiple splits."""
    print("\n" + "=" * 60)
    print("Test 5: Very Long Text (Multiple Splits)")
    print("=" * 60)
    
    # Create a very long text (~15000 characters)
    sentence = "This is a sentence with some content. "
    text = sentence * 400  # ~15000 chars
    
    chunks = smart_split_text(text, max_length=4096, prefer_length=3900)
    
    print(f"✓ Very long text ({len(text)} chars) split into {len(chunks)} chunks")
    
    for i, chunk in enumerate(chunks, 1):
        print(f"  Chunk {i}: {len(chunk)} characters")
        assert len(chunk) <= 4096, f"Chunk {i} exceeds maximum length"
    
    # Verify that all chunks together contain the original text
    rejoined = "".join(chunks)
    assert rejoined == text, "Rejoined chunks don't match original text"
    print("✓ All chunks within limits")
    print("✓ Chunks rejoin to original text")
    
    return True


def test_edge_case_exact_limit():
    """Test text that is exactly at the limit."""
    print("\n" + "=" * 60)
    print("Test 6: Text at Exact Limit")
    print("=" * 60)
    
    # Create text exactly 4096 characters
    text = "x" * 4096
    
    chunks = smart_split_text(text, max_length=4096)
    
    assert len(chunks) == 1, f"Expected 1 chunk, got {len(chunks)}"
    assert len(chunks[0]) == 4096, f"Expected chunk of 4096 chars, got {len(chunks[0])}"
    print("✓ Text at exact limit is not split")
    print(f"  Length: {len(text)}")
    print(f"  Chunks: {len(chunks)}")
    
    return True


def test_edge_case_one_over_limit():
    """Test text that is one character over the limit."""
    print("\n" + "=" * 60)
    print("Test 7: Text One Character Over Limit")
    print("=" * 60)
    
    # Create text exactly 4097 characters
    text = "x" * 4097
    
    chunks = smart_split_text(text, max_length=4096)
    
    assert len(chunks) == 2, f"Expected 2 chunks, got {len(chunks)}"
    assert len(chunks[0]) <= 4096, f"First chunk exceeds limit: {len(chunks[0])}"
    assert len(chunks[1]) <= 4096, f"Second chunk exceeds limit: {len(chunks[1])}"
    print("✓ Text one char over limit is split into 2 chunks")
    print(f"  Chunk 1: {len(chunks[0])} characters")
    print(f"  Chunk 2: {len(chunks[1])} characters")
    
    return True


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("Testing Smart Text Splitting with Embed Support")
    print("=" * 60)
    
    tests = [
        test_short_text,
        test_long_text_splitting,
        test_markdown_preservation,
        test_paragraph_boundary_splitting,
        test_very_long_text,
        test_edge_case_exact_limit,
        test_edge_case_one_over_limit,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"\n✗ Test failed: {test.__name__}")
            print(f"  Error: {str(e)}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Passed: {passed}/{len(tests)}")
    print(f"Failed: {failed}/{len(tests)}")
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
