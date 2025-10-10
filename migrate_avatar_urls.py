#!/usr/bin/env python3
"""
Migration utility to convert base64 avatar URLs to HTTP URLs.

This script will:
1. Find all characters with base64 data URLs as avatars
2. Extract and save the image data to files
3. Update the character cards to use HTTP URLs instead
"""

import os
import json
import base64
import re
from pathlib import Path

def is_base64_data_url(url):
    """Check if a URL is a base64 data URL."""
    if not url:
        return False
    return url.startswith('data:image')

def extract_base64_image(data_url):
    """Extract image data from base64 data URL.
    
    Returns: (image_bytes, file_extension)
    """
    # Parse the data URL: data:image/png;base64,<data>
    match = re.match(r'data:image/(\w+);base64,(.+)', data_url)
    if not match:
        return None, None
    
    mime_type = match.group(1)
    base64_data = match.group(2)
    
    # Decode base64
    try:
        image_bytes = base64.b64decode(base64_data)
        # Convert mime type to file extension
        file_ext = 'jpg' if mime_type == 'jpeg' else mime_type
        return image_bytes, file_ext
    except Exception as e:
        print(f"Error decoding base64: {e}")
        return None, None

def migrate_character_avatars(characters_dir='character_cards', avatars_dir='character_avatars', web_server_url='http://localhost:5000'):
    """Migrate all character avatars from base64 to HTTP URLs.
    
    Args:
        characters_dir: Directory containing character JSON files
        avatars_dir: Directory to save avatar image files
        web_server_url: Base URL of the web server
    """
    if not os.path.exists(characters_dir):
        print(f"❌ Characters directory not found: {characters_dir}")
        return
    
    # Create avatars directory if it doesn't exist
    if not os.path.exists(avatars_dir):
        os.makedirs(avatars_dir)
        print(f"✓ Created avatars directory: {avatars_dir}")
    
    migrated_count = 0
    skipped_count = 0
    error_count = 0
    
    # Process each character file
    for filename in os.listdir(characters_dir):
        if not filename.endswith('.json'):
            continue
        
        filepath = os.path.join(characters_dir, filename)
        character_name = filename[:-5]  # Remove .json extension
        
        try:
            with open(filepath, 'r') as f:
                character_data = json.load(f)
            
            avatar_url = character_data.get('avatar_url')
            
            # Check if avatar needs migration
            if not is_base64_data_url(avatar_url):
                print(f"⊘ Skipping {character_name}: Already using HTTP URL or no avatar")
                skipped_count += 1
                continue
            
            # Extract image data
            image_bytes, file_ext = extract_base64_image(avatar_url)
            if not image_bytes:
                print(f"❌ Error extracting image from {character_name}")
                error_count += 1
                continue
            
            # Save image file
            image_filename = f"{character_name}.{file_ext}"
            image_filepath = os.path.join(avatars_dir, image_filename)
            with open(image_filepath, 'wb') as f:
                f.write(image_bytes)
            
            # Update character with HTTP URL
            new_avatar_url = f"{web_server_url}/character_avatars/{image_filename}"
            character_data['avatar_url'] = new_avatar_url
            
            # Save updated character
            with open(filepath, 'w') as f:
                json.dump(character_data, f, indent=2)
            
            size_kb = len(image_bytes) / 1024
            print(f"✓ Migrated {character_name}: {size_kb:.1f} KB → {new_avatar_url}")
            migrated_count += 1
            
        except Exception as e:
            print(f"❌ Error processing {character_name}: {e}")
            error_count += 1
    
    # Print summary
    print("\n" + "=" * 70)
    print("MIGRATION SUMMARY")
    print("=" * 70)
    print(f"✓ Migrated: {migrated_count}")
    print(f"⊘ Skipped: {skipped_count}")
    print(f"❌ Errors: {error_count}")
    print(f"Total: {migrated_count + skipped_count + error_count}")
    
    if migrated_count > 0:
        print("\n✅ Migration complete!")
        print(f"\nMigrated characters now use HTTP URLs instead of base64 data URLs.")
        print(f"Avatar images saved to: {avatars_dir}/")
        print(f"\nMake sure your web server is running on {web_server_url}")

def main():
    """Run the migration."""
    print("=" * 70)
    print("CHARACTER AVATAR MIGRATION UTILITY")
    print("=" * 70)
    print("\nThis utility converts base64 data URLs to HTTP URLs for character avatars.")
    print("This fixes the Discord webhook error:")
    print('  "...is not supported. Scheme must be one of (\'http\', \'https\')."')
    print("\n" + "=" * 70)
    
    # Load config to get web server URL
    web_server_url = 'http://localhost:5000'
    if os.path.exists('config.json'):
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                web_config = config.get('web_server', {})
                host = web_config.get('host', '0.0.0.0')
                port = web_config.get('port', 5000)
                if host == '0.0.0.0':
                    host = 'localhost'
                web_server_url = f"http://{host}:{port}"
                print(f"\nUsing web server URL from config: {web_server_url}")
        except Exception as e:
            print(f"\n⚠ Could not read config.json: {e}")
            print(f"Using default web server URL: {web_server_url}")
    else:
        print(f"\n⚠ config.json not found, using default web server URL: {web_server_url}")
    
    print("\n" + "=" * 70)
    
    # Run migration
    migrate_character_avatars(web_server_url=web_server_url)

if __name__ == "__main__":
    main()
