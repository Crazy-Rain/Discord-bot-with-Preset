#!/usr/bin/env python3
"""
Demo script showing how the thinking filter works.
This simulates what happens when the bot receives a response with thinking tags.
"""

import re

def simulate_thinking_filter(response, enabled=True, start_tag="<think>", end_tag="</think>"):
    """Simulate the thinking filter."""
    print("="*70)
    print("THINKING FILTER DEMONSTRATION")
    print("="*70)
    
    print(f"\nConfiguration:")
    print(f"  Enabled: {enabled}")
    print(f"  Start Tag: {start_tag}")
    print(f"  End Tag: {end_tag}")
    
    print(f"\n{'='*70}")
    print("AI RESPONSE (Full - what the AI actually generated):")
    print("="*70)
    print(response)
    
    if enabled:
        # Filter the response
        start_tag_escaped = re.escape(start_tag)
        end_tag_escaped = re.escape(end_tag)
        pattern = f"{start_tag_escaped}.*?{end_tag_escaped}"
        filtered = re.sub(pattern, "", response, flags=re.DOTALL)
        filtered = re.sub(r'\n\n\n+', '\n\n', filtered)
        filtered = filtered.strip()
        
        print(f"\n{'='*70}")
        print("SENT TO DISCORD (Filtered - what users see):")
        print("="*70)
        print(filtered)
        
        print(f"\n{'='*70}")
        print("STORED IN HISTORY (Full - for context):")
        print("="*70)
        print(response)
    else:
        print(f"\n{'='*70}")
        print("Filter is disabled - response sent as-is")
        print("="*70)

def main():
    print("\n" + "="*70)
    print("EXAMPLE 1: Simple reasoning with default tags")
    print("="*70)
    
    response1 = """What's the capital of France?

<think>
The user is asking about France's capital. This is a straightforward question.
I should provide a clear, concise answer with some context.
</think>

The capital of France is Paris. It's the largest city in France and has been 
the capital since 1944, though it has served as the political center for much 
longer throughout French history."""

    simulate_thinking_filter(response1, enabled=True)
    
    print("\n" + "="*70)
    print("EXAMPLE 2: Multiple thinking blocks")
    print("="*70)
    
    response2 = """Let me explain how photosynthesis works:

<think>I should break this down into steps for clarity.</think>

1. **Light Absorption**: Plants absorb sunlight through chlorophyll.
   <think>Should I explain chlorophyll? Yes, briefly.</think>
   Chlorophyll is the green pigment that makes this possible.

2. **Water and CO2**: The plant takes in water through roots and carbon dioxide 
   from the air.

3. **Sugar Production**: These combine to create glucose (sugar) and oxygen."""

    simulate_thinking_filter(response2, enabled=True)
    
    print("\n" + "="*70)
    print("EXAMPLE 3: Custom tags for reasoning")
    print("="*70)
    
    response3 = """<reasoning>
This is a complex math problem. Let me work through it step by step.
First, I need to identify what operation is needed...
</reasoning>

To solve 15% of 80:
- Convert 15% to decimal: 0.15
- Multiply: 0.15 × 80 = 12

The answer is 12."""

    simulate_thinking_filter(response3, enabled=True, start_tag="<reasoning>", end_tag="</reasoning>")
    
    print("\n" + "="*70)
    print("EXAMPLE 4: Filter disabled")
    print("="*70)
    
    response4 = """<think>User asked about the weather</think>
I don't have access to real-time weather data."""

    simulate_thinking_filter(response4, enabled=False)

if __name__ == "__main__":
    main()
    print("\n" + "="*70)
    print("✅ DEMONSTRATION COMPLETE")
    print("="*70)
    print("\nKey Points:")
    print("• Full responses are always logged to console when filtering is enabled")
    print("• Filtered responses go to Discord (cleaner for users)")
    print("• Full responses stored in history (better context for AI)")
    print("• Tags are fully customizable through the web UI")
    print("• Filter can be toggled on/off without restarting")
    print("="*70 + "\n")
