"""Discord bot with OpenAI integration and preset support."""
import discord
from discord.ext import commands
from typing import Dict, List, Optional, Tuple
import re
import aiohttp
from config_manager import ConfigManager
from preset_manager import PresetManager
from character_manager import CharacterManager
from user_characters_manager import UserCharactersManager
from lorebook_manager import LorebookManager
from openai_client import OpenAIClient

class DiscordBot(commands.Bot):
    def __init__(self, config: ConfigManager):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)
        
        self.config_manager = config
        self.preset_manager = PresetManager()
        self.character_manager = CharacterManager()
        self.user_characters_manager = UserCharactersManager()
        self.lorebook_manager = LorebookManager()
        
        # Initialize OpenAI client
        openai_config = config.get("openai_config", {})
        self.openai_client = OpenAIClient(
            api_key=openai_config.get("api_key", ""),
            base_url=openai_config.get("base_url", "https://api.openai.com/v1"),
            model=openai_config.get("model", "gpt-3.5-turbo")
        )
        
        # Load default preset
        default_preset = config.get("default_preset", {})
        if default_preset:
            self.preset_manager.current_preset = default_preset
        
        # Conversation history per channel
        self.conversations: Dict[int, List[Dict[str, str]]] = {}
        
        # Store alternative responses for swipe functionality
        self.response_alternatives: Dict[int, List[List[str]]] = {}
        self.current_alternative_index: Dict[int, int] = {}
        
        # Track character names per channel for context
        self.character_names: Dict[int, List[str]] = {}
        
        # Track loaded character per channel for webhook-based avatars
        self.channel_characters: Dict[int, Dict[str, any]] = {}
        
        # Cache webhooks per channel to avoid recreating them
        self.channel_webhooks: Dict[int, discord.Webhook] = {}
        
        # Add commands
        self.add_bot_commands()
    
    async def update_bot_avatar(self, avatar_url: str) -> bool:
        """Update bot's avatar from a URL or base64 data URL.
        
        Args:
            avatar_url: URL to the avatar image or base64 data URL
            
        Returns:
            True if avatar was updated successfully, False otherwise
        """
        if not avatar_url:
            return False
            
        try:
            # Check if it's a base64 data URL
            if avatar_url.startswith('data:image'):
                import base64
                # Extract base64 data from data URL
                # Format: data:image/png;base64,iVBORw0KGgoAAAANS...
                header, encoded = avatar_url.split(',', 1)
                avatar_bytes = base64.b64decode(encoded)
                # Update bot's avatar
                await self.user.edit(avatar=avatar_bytes)
                print(f"Updated bot avatar from uploaded image")
                return True
            else:
                # Download the image from URL
                async with aiohttp.ClientSession() as session:
                    async with session.get(avatar_url) as response:
                        if response.status == 200:
                            avatar_bytes = await response.read()
                            # Update bot's avatar
                            await self.user.edit(avatar=avatar_bytes)
                            print(f"Updated bot avatar from: {avatar_url}")
                            return True
                        else:
                            print(f"Failed to download avatar: HTTP {response.status}")
                            return False
        except Exception as e:
            print(f"Error updating bot avatar: {e}")
            return False
    
    async def get_or_create_webhook(self, channel: discord.TextChannel) -> Optional[discord.Webhook]:
        """Get existing webhook for channel or create a new one.
        
        Args:
            channel: The text channel to get/create webhook for
            
        Returns:
            The webhook object, or None if creation fails
        """
        channel_id = channel.id
        
        # Check cache first
        if channel_id in self.channel_webhooks:
            # Verify webhook still exists
            try:
                webhook = self.channel_webhooks[channel_id]
                # Try to fetch to verify it still exists
                await webhook.fetch()
                return webhook
            except (discord.NotFound, discord.HTTPException):
                # Webhook was deleted, remove from cache
                del self.channel_webhooks[channel_id]
        
        # Try to find existing webhook
        try:
            webhooks = await channel.webhooks()
            for webhook in webhooks:
                if webhook.user == self.user:
                    self.channel_webhooks[channel_id] = webhook
                    return webhook
        except discord.Forbidden:
            print(f"No permission to manage webhooks in channel {channel.name}")
            return None
        except Exception as e:
            print(f"Error fetching webhooks: {e}")
            return None
        
        # Create new webhook
        try:
            webhook = await channel.create_webhook(
                name="Character Bot",
                reason="For per-channel character avatars"
            )
            self.channel_webhooks[channel_id] = webhook
            return webhook
        except discord.Forbidden:
            print(f"No permission to create webhook in channel {channel.name}")
            return None
        except Exception as e:
            print(f"Error creating webhook: {e}")
            return None
    
    async def send_as_character(
        self, 
        channel: discord.TextChannel, 
        content: str,
        character_data: Dict[str, any]
    ) -> bool:
        """Send a message as a character using webhooks.
        
        Args:
            channel: The channel to send the message in
            content: The message content
            character_data: Character data including name and avatar_url
            
        Returns:
            True if message was sent successfully, False otherwise
        """
        webhook = await self.get_or_create_webhook(channel)
        if not webhook:
            return False
        
        try:
            # Get character name and avatar
            character_name = character_data.get('name', 'Character')
            avatar_url = character_data.get('avatar_url')
            
            # Send message via webhook with character's name and avatar
            # Split long messages
            if len(content) > 2000:
                for i in range(0, len(content), 2000):
                    chunk = content[i:i+2000]
                    await webhook.send(
                        content=chunk,
                        username=character_name,
                        avatar_url=avatar_url,
                        wait=True
                    )
            else:
                await webhook.send(
                    content=content,
                    username=character_name,
                    avatar_url=avatar_url,
                    wait=True
                )
            return True
        except Exception as e:
            print(f"Error sending webhook message: {e}")
            return False
    
    def update_openai_config(self, api_key: str = None, base_url: str = None, model: str = None):
        """Update OpenAI client configuration dynamically.
        
        Args:
            api_key: New API key to use
            base_url: New base URL (proxy) to use
            model: New model name to use
        """
        # Store the current config values, use new values if provided
        if api_key is None:
            api_key = self.openai_client.api_key
        if base_url is None:
            # Try to get base_url from client, or fall back to config
            try:
                base_url = str(self.openai_client.client.base_url) if hasattr(self.openai_client.client, 'base_url') else None
            except:
                base_url = self.config_manager.get('openai_config.base_url', 'https://api.openai.com/v1')
        if model is None:
            model = self.openai_client.model
        
        # Recreate the OpenAI client with new configuration
        from openai_client import OpenAIClient
        self.openai_client = OpenAIClient(
            api_key=api_key,
            base_url=base_url,
            model=model
        )
        print(f"Updated OpenAI configuration - Model: {model}, Base URL: {base_url}")

    
    def parse_character_message(self, message: str) -> Tuple[Optional[str], str]:
        """Parse a message for character name format: 'CharacterName:message'.
        
        Returns:
            Tuple of (character_name, actual_message). If no character name is found,
            character_name will be None.
        """
        # Match pattern: CharacterName:message (with optional spaces around colon)
        match = re.match(r'^([^:]+?)\s*:\s*(.+)$', message.strip(), re.DOTALL)
        if match:
            character_name = match.group(1).strip()
            actual_message = match.group(2).strip()
            return character_name, actual_message
        return None, message
    
    async def load_channel_history(self, channel, limit: int = 50) -> List[Dict[str, str]]:
        """Load recent !chat messages from channel history to build context.
        
        Args:
            channel: Discord channel object
            limit: Maximum number of messages to fetch from history
            
        Returns:
            List of conversation messages in chronological order (oldest first)
        """
        conversation = []
        character_names_found = []
        
        try:
            # Fetch recent messages from the channel (newest first by default)
            messages = []
            async for message in channel.history(limit=limit):
                messages.append(message)
            
            # Reverse to get chronological order (oldest first)
            messages.reverse()
            
            # Parse messages to extract !chat commands and responses
            for message in messages:
                # Skip messages from other bots or empty messages
                if message.author.bot and message.author.id != self.user.id:
                    continue
                
                # Check if it's a user message with !chat command
                if message.content.startswith("!chat "):
                    # Extract the message after !chat
                    chat_message = message.content[6:].strip()  # Remove "!chat "
                    
                    # Parse character name if present
                    character_name, actual_message = self.parse_character_message(chat_message)
                    
                    # Track character name
                    if character_name and character_name not in character_names_found:
                        character_names_found.append(character_name)
                    
                    # Add to conversation as user message
                    if character_name:
                        conversation.append({
                            "role": "user", 
                            "content": f"{character_name}: {actual_message}"
                        })
                    else:
                        conversation.append({
                            "role": "user",
                            "content": actual_message
                        })
                
                # Check if it's a bot response (message from this bot, not starting with !)
                elif message.author.id == self.user.id and not message.content.startswith("!"):
                    # Skip meta messages (like "Alternative X/Y")
                    if message.content.startswith("*Alternative "):
                        continue
                    # This is likely a bot response, add it to conversation
                    conversation.append({
                        "role": "assistant",
                        "content": message.content
                    })
            
        except Exception as e:
            print(f"Error loading channel history: {e}")
        
        return conversation, character_names_found
    
    def add_bot_commands(self):
        """Add bot commands."""
        
        @self.command(name="chat", help="Chat with the AI")
        async def chat(ctx, *, message: str):
            """Chat with the AI using current preset and character."""
            channel_id = ctx.channel.id
            
            # Initialize conversation history if needed
            if channel_id not in self.conversations:
                self.conversations[channel_id] = []
            if channel_id not in self.character_names:
                self.character_names[channel_id] = []
            
            # Load channel history if conversation is empty (e.g., after bot restart)
            # This allows the bot to pick up context from previous !chat messages
            if not self.conversations[channel_id]:
                history_messages, history_character_names = await self.load_channel_history(
                    ctx.channel, 
                    limit=50  # Fetch up to 50 recent messages
                )
                self.conversations[channel_id] = history_messages
                # Merge character names found in history
                for char_name in history_character_names:
                    if char_name not in self.character_names[channel_id]:
                        self.character_names[channel_id].append(char_name)
            
            # Parse character name from message
            character_name, actual_message = self.parse_character_message(message)
            
            # Track character name if provided
            if character_name:
                if character_name not in self.character_names[channel_id]:
                    self.character_names[channel_id].append(character_name)
            
            # Build messages using the new formatting system that supports
            # SillyTavern-style presets with proper role separation
            messages = self.build_chat_messages(channel_id, actual_message, character_name)
            
            # Get preset parameters
            preset = self.preset_manager.get_current_preset()
            
            try:
                async with ctx.typing():
                    # Generate response
                    response = await self.openai_client.chat_completion(
                        messages=messages,
                        temperature=preset.get("temperature", 0.7),
                        max_tokens=preset.get("max_response_length", preset.get("max_tokens", 2000)),
                        top_p=preset.get("top_p", 1.0),
                        frequency_penalty=preset.get("frequency_penalty", 0.0),
                        presence_penalty=preset.get("presence_penalty", 0.0)
                    )
                
                # Update conversation history with formatted message
                if character_name:
                    self.conversations[channel_id].append({"role": "user", "content": f"{character_name}: {actual_message}"})
                else:
                    self.conversations[channel_id].append({"role": "user", "content": actual_message})
                self.conversations[channel_id].append({"role": "assistant", "content": response})
                
                # Store response for swipe functionality (initialize with current response)
                if channel_id not in self.response_alternatives:
                    self.response_alternatives[channel_id] = []
                self.response_alternatives[channel_id].append([response])
                self.current_alternative_index[channel_id] = 0
                
                # Limit conversation history
                if len(self.conversations[channel_id]) > 20:
                    self.conversations[channel_id] = self.conversations[channel_id][-20:]
                    # Also limit response alternatives history
                    if len(self.response_alternatives[channel_id]) > 10:
                        self.response_alternatives[channel_id] = self.response_alternatives[channel_id][-10:]
                
                # Send response - use webhook if character is loaded for this channel
                if channel_id in self.channel_characters:
                    # Try to send via webhook with character's avatar
                    character_data = self.channel_characters[channel_id]
                    webhook_sent = await self.send_as_character(
                        ctx.channel, 
                        response, 
                        character_data
                    )
                    if webhook_sent:
                        # Message sent successfully via webhook
                        pass
                    else:
                        # Fallback to normal message if webhook fails
                        if len(response) > 2000:
                            for i in range(0, len(response), 2000):
                                await ctx.send(response[i:i+2000])
                        else:
                            await ctx.send(response)
                else:
                    # No character loaded, send normal message
                    if len(response) > 2000:
                        for i in range(0, len(response), 2000):
                            await ctx.send(response[i:i+2000])
                    else:
                        await ctx.send(response)
            
            except Exception as e:
                await ctx.send(f"Error: {str(e)}")
        
        @self.command(name="clear", help="Clear conversation history")
        async def clear(ctx):
            """Clear conversation history for this channel."""
            channel_id = ctx.channel.id
            if channel_id in self.conversations:
                self.conversations[channel_id] = []
            if channel_id in self.response_alternatives:
                self.response_alternatives[channel_id] = []
            if channel_id in self.current_alternative_index:
                del self.current_alternative_index[channel_id]
            if channel_id in self.character_names:
                self.character_names[channel_id] = []
            if channel_id in self.channel_characters:
                del self.channel_characters[channel_id]
            await ctx.send("Conversation history and character names cleared!")
        
        @self.command(name="reload_history", help="Reload conversation from channel history")
        async def reload_history(ctx, limit: int = 50):
            """Reload conversation history from channel messages.
            
            This command fetches recent !chat messages from the channel and rebuilds
            the conversation context. Useful after bot restart or to refresh context.
            
            Args:
                limit: Number of recent messages to fetch (default: 50, max: 100)
            """
            channel_id = ctx.channel.id
            
            # Limit the maximum to prevent excessive API calls
            limit = min(limit, 100)
            
            async with ctx.typing():
                # Clear current conversation
                self.conversations[channel_id] = []
                self.character_names[channel_id] = []
                
                # Load history
                history_messages, history_character_names = await self.load_channel_history(
                    ctx.channel, 
                    limit=limit
                )
                
                self.conversations[channel_id] = history_messages
                self.character_names[channel_id] = history_character_names
                
                # Clear response alternatives as they're no longer valid
                if channel_id in self.response_alternatives:
                    self.response_alternatives[channel_id] = []
                if channel_id in self.current_alternative_index:
                    del self.current_alternative_index[channel_id]
                
                msg_count = len(history_messages)
                char_count = len(history_character_names)
                
                response = f"Reloaded conversation history!\n"
                response += f"- Loaded {msg_count} messages\n"
                if char_count > 0:
                    response += f"- Found {char_count} character(s): {', '.join(history_character_names)}"
                else:
                    response += f"- No character names found"
                
                await ctx.send(response)
        
        @self.command(name="preset", help="Load a preset")
        async def preset(ctx, preset_name: str):
            """Load a preset by name."""
            try:
                self.preset_manager.load_preset(preset_name)
                await ctx.send(f"Loaded preset: {preset_name}")
            except FileNotFoundError:
                await ctx.send(f"Preset not found: {preset_name}")
        
        @self.command(name="presets", help="List available presets")
        async def presets(ctx):
            """List all available presets."""
            preset_list = self.preset_manager.list_presets()
            if preset_list:
                await ctx.send(f"Available presets: {', '.join(preset_list)}")
            else:
                await ctx.send("No presets available.")
        
        @self.command(name="character", help="Load a character card for this channel")
        async def character(ctx, character_name: str):
            """Load a character card by name for this channel.
            
            This command loads a character specifically for the current channel.
            When a character is loaded, the bot will use webhooks to display
            messages with the character's avatar and name in this channel.
            """
            try:
                character_data = self.character_manager.load_character(character_name)
                channel_id = ctx.channel.id
                
                # Store character data for this channel
                self.channel_characters[channel_id] = character_data
                
                display_name = character_data.get('name', character_name)
                avatar_url = character_data.get('avatar_url')
                
                # Send confirmation message
                if avatar_url:
                    await ctx.send(
                        f"✨ Loaded character **{display_name}** for this channel!\n"
                        f"The bot will now respond with {display_name}'s avatar and name using webhooks."
                    )
                else:
                    await ctx.send(
                        f"✨ Loaded character **{display_name}** for this channel!\n"
                        f"Note: No avatar URL set for this character. Set one to see the character's avatar."
                    )
                
                # Clear conversation when switching characters
                if channel_id in self.conversations:
                    self.conversations[channel_id] = []
                    
            except FileNotFoundError:
                await ctx.send(f"Character not found: {character_name}")
            except Exception as e:
                await ctx.send(f"Error loading character: {str(e)}")
        
        @self.command(name="current_character", help="Show current character for this channel")
        async def current_character(ctx):
            """Show which character is currently loaded for this channel."""
            channel_id = ctx.channel.id
            if channel_id in self.channel_characters:
                character_data = self.channel_characters[channel_id]
                character_name = character_data.get('name', 'Unknown')
                avatar_url = character_data.get('avatar_url', 'None')
                await ctx.send(
                    f"**Current character for this channel:** {character_name}\n"
                    f"**Avatar URL:** {avatar_url if avatar_url else 'Not set'}"
                )
            else:
                await ctx.send("No character is currently loaded for this channel.")
        
        @self.command(name="unload_character", help="Unload current character from this channel")
        async def unload_character(ctx):
            """Unload the current character from this channel."""
            channel_id = ctx.channel.id
            if channel_id in self.channel_characters:
                character_name = self.channel_characters[channel_id].get('name', 'Unknown')
                del self.channel_characters[channel_id]
                await ctx.send(f"✨ Unloaded character **{character_name}** from this channel. Bot will now respond normally.")
            else:
                await ctx.send("No character is currently loaded for this channel.")
        
        @self.command(name="characters", help="List available characters")
        async def characters(ctx):
            """List all available character cards."""
            char_list = self.character_manager.list_characters()
            if char_list:
                await ctx.send(f"Available characters: {', '.join(char_list)}")
            else:
                await ctx.send("No characters available.")
        
        @self.command(name="update", help="Update user character description")
        async def update(ctx, *, message: str):
            """Update a user character description.
            
            Usage: !update <Character Name>: <Description>
            """
            # Parse character name and description
            character_name, description = self.parse_character_message(message)
            
            if not character_name:
                await ctx.send("Invalid format. Use: !update <Character Name>: <Description>")
                return
            
            # Add or update the user character
            self.user_characters_manager.add_or_update_character(character_name, description)
            await ctx.send(f"Updated user character: {character_name}")
        
        @self.command(name="user_chars", help="List saved user characters")
        async def user_chars(ctx):
            """List all saved user character names."""
            char_list = self.user_characters_manager.list_characters()
            if char_list:
                await ctx.send(f"Saved user characters: {', '.join(char_list)}")
            else:
                await ctx.send("No user characters saved.")
        
        @self.command(name="user_char", help="View a user character")
        async def user_char(ctx, character_name: str):
            """View a specific user character's details."""
            char_data = self.user_characters_manager.get_character(character_name)
            if char_data:
                response = f"**{char_data['name']}**\n{char_data['description']}"
                await ctx.send(response)
            else:
                await ctx.send(f"User character not found: {character_name}")
        
        @self.command(name="delete_user_char", help="Delete a user character")
        async def delete_user_char(ctx, character_name: str):
            """Delete a saved user character."""
            if self.user_characters_manager.delete_character(character_name):
                await ctx.send(f"Deleted user character: {character_name}")
            else:
                await ctx.send(f"User character not found: {character_name}")
        
        @self.command(name="lorebook_add", help="Add or update a lorebook entry")
        async def lorebook_add(ctx, key: str, *, content: str):
            """Add or update a lorebook entry.
            
            Usage: !lorebook_add <key> <content>
            Example: !lorebook_add "Kingdom of Aldoria" A vast kingdom ruled by King Aldric...
            """
            # Parse keywords and always_active flag from content if present
            # Format: content [keywords: word1, word2] [always_active]
            import re
            
            keywords = []
            always_active = False
            
            # Check for always_active flag
            if "[always_active]" in content.lower():
                always_active = True
                content = re.sub(r'\[always_active\]', '', content, flags=re.IGNORECASE).strip()
            
            # Check for keywords
            keyword_match = re.search(r'\[keywords?:\s*([^\]]+)\]', content, re.IGNORECASE)
            if keyword_match:
                keywords_str = keyword_match.group(1)
                keywords = [k.strip() for k in keywords_str.split(',')]
                content = re.sub(r'\[keywords?:\s*[^\]]+\]', '', content, flags=re.IGNORECASE).strip()
            
            self.lorebook_manager.add_or_update_entry(key, content, keywords, always_active)
            
            status_parts = [f"Added/updated lorebook entry: **{key}**"]
            if keywords:
                status_parts.append(f"Keywords: {', '.join(keywords)}")
            if always_active:
                status_parts.append("Always active: Yes")
            
            await ctx.send("\n".join(status_parts))
        
        @self.command(name="lorebook_list", help="List all lorebook entries")
        async def lorebook_list(ctx):
            """List all lorebook entry keys."""
            entries = self.lorebook_manager.list_entries()
            if entries:
                await ctx.send(f"Lorebook entries: {', '.join(entries)}")
            else:
                await ctx.send("No lorebook entries saved.")
        
        @self.command(name="lorebook_view", help="View a lorebook entry")
        async def lorebook_view(ctx, key: str):
            """View a specific lorebook entry."""
            entry = self.lorebook_manager.get_entry(key)
            if entry:
                response_parts = [f"**{entry['key']}**", entry['content']]
                if entry.get('keywords'):
                    response_parts.append(f"*Keywords: {', '.join(entry['keywords'])}*")
                if entry.get('always_active'):
                    response_parts.append("*Always active: Yes*")
                await ctx.send("\n".join(response_parts))
            else:
                await ctx.send(f"Lorebook entry not found: {key}")
        
        @self.command(name="lorebook_delete", help="Delete a lorebook entry")
        async def lorebook_delete(ctx, key: str):
            """Delete a lorebook entry."""
            if self.lorebook_manager.delete_entry(key):
                await ctx.send(f"Deleted lorebook entry: {key}")
            else:
                await ctx.send(f"Lorebook entry not found: {key}")
        
        @self.command(name="help_bot", help="Show bot help")
        async def help_bot(ctx):
            """Show bot help information."""
            help_text = """
**Discord Bot Commands:**
`!chat <message>` - Chat with the AI
`!clear` - Clear conversation history and character names
`!reload_history [limit]` - Reload conversation from channel history (default: 50 messages)
`!preset <name>` - Load a preset
`!presets` - List available presets
`!character <name>` - Load a character card for this channel (uses webhooks)
`!current_character` - Show which character is loaded in this channel
`!unload_character` - Unload character from this channel
`!characters` - List available characters
`!swipe` - Generate alternative response to last message
`!swipe_left` - Show previous alternative response
`!swipe_right` - Show next alternative response
`!update <Name>: <Description>` - Update user character description
`!user_chars` - List saved user characters
`!user_char <name>` - View a user character
`!delete_user_char <name>` - Delete a user character
`!lorebook_add <key> <content>` - Add/update lorebook entry
`!lorebook_list` - List all lorebook entries
`!lorebook_view <key>` - View a lorebook entry
`!lorebook_delete <key>` - Delete a lorebook entry
`!help_bot` - Show this help message

**Per-Channel Character Avatars:**
Load different characters in different channels! When you load a character in a channel, the bot uses webhooks to respond with the character's avatar and name. This bypasses Discord's rate limits and allows unlimited character switches.
- No rate limits - switch characters as often as you want
- Different characters can be active in different channels simultaneously
- Requires bot to have "Manage Webhooks" permission
Example: `!character luna` loads Luna for this channel only

**Context & History:**
The bot automatically loads recent !chat messages from the channel when starting a new conversation. This means past conversations persist even after bot restart. Use `!reload_history` to manually refresh the context from channel history.

**Character Name Feature:**
You can identify yourself as a character by using the format:
`!chat CharacterName: message`

**User Character Descriptions:**
Save descriptions for your characters using:
`!update Alice: A brave warrior with long red hair and green eyes`
The AI will use these descriptions for context.

**Lorebook Feature:**
Add world-building and lore information:
`!lorebook_add "Kingdom of Aldoria" A vast kingdom... [keywords: kingdom, aldoria] [always_active]`
- Use `[keywords: word1, word2]` to make entry appear when keywords are mentioned
- Use `[always_active]` to include entry in all conversations

**Formatting Guidelines:**
- Use `"quotes"` for spoken dialogue: `!chat Alice: "Hello, how are you?"`
- Use `*asterisks*` for actions: `!chat Bob: *waves* "Hi everyone!"`
- Text without quotes or asterisks is descriptive or contextual

**Examples:**
`!chat Alice: "Hello!" *waves enthusiastically*`
`!chat Bob: *enters the room* "Good morning everyone!"`
`!chat Charlie: Looks around curiously "Where is everyone?"`


The bot will track character names and understand who is speaking.

**Configuration:**
Visit http://localhost:5000 to configure the bot via web interface.
"""
            await ctx.send(help_text)
        
        @self.command(name="swipe", help="Generate an alternative response")
        async def swipe(ctx):
            """Generate an alternative response to the last user message."""
            channel_id = ctx.channel.id
            
            # Initialize if needed
            if channel_id not in self.conversations:
                self.conversations[channel_id] = []
            if channel_id not in self.character_names:
                self.character_names[channel_id] = []
            
            # Load channel history if conversation is empty
            if not self.conversations[channel_id]:
                history_messages, history_character_names = await self.load_channel_history(
                    ctx.channel, 
                    limit=50
                )
                self.conversations[channel_id] = history_messages
                for char_name in history_character_names:
                    if char_name not in self.character_names[channel_id]:
                        self.character_names[channel_id].append(char_name)
            
            # Check if there's a conversation
            if len(self.conversations[channel_id]) < 2:
                await ctx.send("No previous message to regenerate. Use !chat first.")
                return
            
            # Get the last user message (should be second to last in history)
            last_user_msg = None
            last_user_character = None
            for msg in reversed(self.conversations[channel_id]):
                if msg["role"] == "user":
                    last_user_msg = msg["content"]
                    # Try to parse character name from the message
                    last_user_character, _ = self.parse_character_message(last_user_msg)
                    break
            
            if not last_user_msg:
                await ctx.send("No user message found to regenerate.")
                return
            
            # Remove last assistant message from conversation temporarily
            last_assistant_msg = self.conversations[channel_id].pop()
            
            # Build messages using the new system (it will include everything up to last user msg)
            # Extract just the message content without character prefix for build_chat_messages
            _, clean_message = self.parse_character_message(last_user_msg)
            messages = self.build_chat_messages(channel_id, clean_message, last_user_character)
            
            # Restore the last assistant message (we'll update it with the new response)
            self.conversations[channel_id].append(last_assistant_msg)
            
            # Get preset parameters
            preset = self.preset_manager.get_current_preset()
            
            try:
                async with ctx.typing():
                    # Generate alternative response
                    response = await self.openai_client.chat_completion(
                        messages=messages,
                        temperature=preset.get("temperature", 0.7),
                        max_tokens=preset.get("max_response_length", preset.get("max_tokens", 2000)),
                        top_p=preset.get("top_p", 1.0),
                        frequency_penalty=preset.get("frequency_penalty", 0.0),
                        presence_penalty=preset.get("presence_penalty", 0.0)
                    )
                
                # Add to alternatives
                if channel_id in self.response_alternatives and len(self.response_alternatives[channel_id]) > 0:
                    self.response_alternatives[channel_id][-1].append(response)
                    self.current_alternative_index[channel_id] = len(self.response_alternatives[channel_id][-1]) - 1
                else:
                    # Initialize if needed
                    if channel_id not in self.response_alternatives:
                        self.response_alternatives[channel_id] = []
                    self.response_alternatives[channel_id].append([response])
                    self.current_alternative_index[channel_id] = 0
                
                # Update the last assistant message in history
                self.conversations[channel_id][-1] = {"role": "assistant", "content": response}
                
                alt_count = len(self.response_alternatives[channel_id][-1])
                current_idx = self.current_alternative_index[channel_id]
                
                # Send response - use webhook if character is loaded for this channel
                if channel_id in self.channel_characters:
                    # Try to send via webhook with character's avatar
                    character_data = self.channel_characters[channel_id]
                    webhook_sent = await self.send_as_character(
                        ctx.channel, 
                        response, 
                        character_data
                    )
                    if not webhook_sent:
                        # Fallback to normal message if webhook fails
                        if len(response) > 2000:
                            for i in range(0, len(response), 2000):
                                await ctx.send(response[i:i+2000])
                        else:
                            await ctx.send(response)
                else:
                    # No character loaded, send normal message
                    if len(response) > 2000:
                        for i in range(0, len(response), 2000):
                            await ctx.send(response[i:i+2000])
                    else:
                        await ctx.send(response)
                
                await ctx.send(f"*Alternative {current_idx + 1}/{alt_count} (use !swipe_left/!swipe_right to navigate)*")
            
            except Exception as e:
                await ctx.send(f"Error generating alternative: {str(e)}")
        
        @self.command(name="swipe_left", help="Show previous alternative response")
        async def swipe_left(ctx):
            """Navigate to the previous alternative response."""
            channel_id = ctx.channel.id
            
            if channel_id not in self.response_alternatives or not self.response_alternatives[channel_id]:
                await ctx.send("No alternatives available. Use !swipe to generate alternatives.")
                return
            
            if len(self.response_alternatives[channel_id][-1]) <= 1:
                await ctx.send("No other alternatives available. Use !swipe to generate more.")
                return
            
            # Move to previous alternative (with wrapping)
            current_idx = self.current_alternative_index.get(channel_id, 0)
            current_idx = (current_idx - 1) % len(self.response_alternatives[channel_id][-1])
            self.current_alternative_index[channel_id] = current_idx
            
            # Get the alternative response
            response = self.response_alternatives[channel_id][-1][current_idx]
            
            # Update conversation history
            self.conversations[channel_id][-1] = {"role": "assistant", "content": response}
            
            alt_count = len(self.response_alternatives[channel_id][-1])
            
            # Send response - use webhook if character is loaded for this channel
            if channel_id in self.channel_characters:
                # Try to send via webhook with character's avatar
                character_data = self.channel_characters[channel_id]
                webhook_sent = await self.send_as_character(
                    ctx.channel, 
                    response, 
                    character_data
                )
                if not webhook_sent:
                    # Fallback to normal message if webhook fails
                    if len(response) > 2000:
                        for i in range(0, len(response), 2000):
                            await ctx.send(response[i:i+2000])
                    else:
                        await ctx.send(response)
            else:
                # No character loaded, send normal message
                if len(response) > 2000:
                    for i in range(0, len(response), 2000):
                        await ctx.send(response[i:i+2000])
                else:
                    await ctx.send(response)
            
            await ctx.send(f"*Alternative {current_idx + 1}/{alt_count}*")
        
        @self.command(name="swipe_right", help="Show next alternative response")
        async def swipe_right(ctx):
            """Navigate to the next alternative response."""
            channel_id = ctx.channel.id
            
            if channel_id not in self.response_alternatives or not self.response_alternatives[channel_id]:
                await ctx.send("No alternatives available. Use !swipe to generate alternatives.")
                return
            
            if len(self.response_alternatives[channel_id][-1]) <= 1:
                await ctx.send("No other alternatives available. Use !swipe to generate more.")
                return
            
            # Move to next alternative (with wrapping)
            current_idx = self.current_alternative_index.get(channel_id, 0)
            current_idx = (current_idx + 1) % len(self.response_alternatives[channel_id][-1])
            self.current_alternative_index[channel_id] = current_idx
            
            # Get the alternative response
            response = self.response_alternatives[channel_id][-1][current_idx]
            
            # Update conversation history
            self.conversations[channel_id][-1] = {"role": "assistant", "content": response}
            
            alt_count = len(self.response_alternatives[channel_id][-1])
            
            # Send response - use webhook if character is loaded for this channel
            if channel_id in self.channel_characters:
                # Try to send via webhook with character's avatar
                character_data = self.channel_characters[channel_id]
                webhook_sent = await self.send_as_character(
                    ctx.channel, 
                    response, 
                    character_data
                )
                if not webhook_sent:
                    # Fallback to normal message if webhook fails
                    if len(response) > 2000:
                        for i in range(0, len(response), 2000):
                            await ctx.send(response[i:i+2000])
                    else:
                        await ctx.send(response)
            else:
                # No character loaded, send normal message
                if len(response) > 2000:
                    for i in range(0, len(response), 2000):
                        await ctx.send(response[i:i+2000])
                else:
                    await ctx.send(response)
            
            await ctx.send(f"*Alternative {current_idx + 1}/{alt_count}*")
    
    def get_system_prompt(self) -> str:
        """Get the system prompt from character or preset."""
        # Character takes precedence
        char_prompt = self.character_manager.get_character_system_prompt()
        if char_prompt:
            return char_prompt
        
        # Fall back to preset
        preset = self.preset_manager.get_current_preset()
        return preset.get("system_prompt", "You are a helpful AI assistant.")
    
    def build_chat_messages(
        self, 
        channel_id: int, 
        user_message: str, 
        character_name: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """
        Build the message list for chat completion with proper role separation.
        Follows SillyTavern-style preset formatting with separate system, user, and assistant messages.
        
        Args:
            channel_id: Channel ID for conversation history
            user_message: The user's message content
            character_name: Optional character name if user is roleplaying
        
        Returns:
            List of message dicts with 'role' and 'content' keys
        """
        messages = []
        preset = self.preset_manager.get_current_preset()
        
        # Get character data if loaded for this channel
        character_data = None
        if channel_id in self.channel_characters:
            character_data = self.channel_characters[channel_id]
        elif self.character_manager.current_character:
            character_data = self.character_manager.current_character
        
        # Format character card according to preset rules
        char_format = self.preset_manager.format_character_for_prompt(
            character_data, 
            preset
        )
        
        # 1. Add main system prompt
        system_prompt = char_format.get('system_prompt', '')
        if not system_prompt:
            system_prompt = preset.get('system_prompt', 'You are a helpful AI assistant.')
        
        # Build enhanced system prompt with character context
        enhanced_system_prompt = system_prompt
        
        # Add character system info if present
        char_system = char_format.get('character_system', '')
        if char_system:
            enhanced_system_prompt += '\n\n' + char_system
        
        # Add user character tracking info if needed
        if self.character_names.get(channel_id):
            character_list = ", ".join(self.character_names[channel_id])
            enhanced_system_prompt += f"""

IMPORTANT: In this conversation, users will identify themselves as characters by prefixing their messages with 'CharacterName:'. The following character names are being used by users: {character_list}. You should NEVER pretend to be these characters or respond as if you are them. You are a separate entity having a conversation with these characters.

FORMAT GUIDELINES:
- Text in "quotes" represents spoken dialogue by the character
- Text in *asterisks* represents actions performed by the character
- Text without quotes or asterisks is descriptive text or additional context"""
            
            # Add user character descriptions
            user_char_section = self.user_characters_manager.get_system_prompt_section(
                self.character_names[channel_id]
            )
            if user_char_section:
                enhanced_system_prompt += user_char_section
        
        # Add lorebook entries
        lorebook_section = self.lorebook_manager.get_system_prompt_section(user_message)
        if lorebook_section:
            enhanced_system_prompt += "\n\n" + lorebook_section
        
        # Add the system message
        if enhanced_system_prompt:
            messages.append({"role": "system", "content": enhanced_system_prompt})
        
        # 2. Add example dialogues from character card (if configured in preset)
        example_dialogues = char_format.get('example_dialogues', [])
        if example_dialogues:
            messages.extend(example_dialogues)
        
        # 3. Add conversation history
        if channel_id in self.conversations:
            messages.extend(self.conversations[channel_id])
        
        # 4. Add current user message
        if character_name:
            formatted_message = f"{character_name}: {user_message}"
            messages.append({"role": "user", "content": formatted_message})
        else:
            messages.append({"role": "user", "content": user_message})
        
        return messages
    
    async def on_ready(self):
        """Called when bot is ready."""
        print(f"Bot is ready! Logged in as {self.user}")
        
        # Set bot name and avatar to character if a character is loaded
        current_char = self.character_manager.get_current_character()
        if current_char and current_char.get('name'):
            display_name = current_char['name']
            try:
                for guild in self.guilds:
                    try:
                        await guild.me.edit(nick=display_name)
                        print(f"Set bot nickname to '{display_name}' in guild {guild.name}")
                    except discord.Forbidden:
                        print(f"Permission denied to change nickname in guild {guild.name}")
                    except Exception as e:
                        print(f"Error changing nickname in guild {guild.name}: {e}")
            except Exception as e:
                print(f"Error setting bot name on ready: {e}")
            
            # Set bot avatar if avatar_url is provided
            avatar_url = current_char.get('avatar_url')
            if avatar_url:
                avatar_updated = await self.update_bot_avatar(avatar_url)
                if avatar_updated:
                    print(f"Set bot avatar to match '{display_name}'")
