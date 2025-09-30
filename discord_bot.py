"""Discord bot with OpenAI integration and preset support."""
import discord
from discord.ext import commands
from typing import Dict, List, Optional, Tuple
import re
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
        
        # Add commands
        self.add_bot_commands()
    
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
            
            # Parse character name from message
            character_name, actual_message = self.parse_character_message(message)
            
            # Track character name if provided
            if character_name:
                if character_name not in self.character_names[channel_id]:
                    self.character_names[channel_id].append(character_name)
            
            # Get system prompt
            system_prompt = self.get_system_prompt()
            
            # Build enhanced system prompt with character context
            enhanced_system_prompt = system_prompt
            if self.character_names[channel_id]:
                character_list = ", ".join(self.character_names[channel_id])
                enhanced_system_prompt = f"""{system_prompt}

IMPORTANT: In this conversation, users will identify themselves as characters by prefixing their messages with 'CharacterName:'. The following character names are being used by users: {character_list}. You should NEVER pretend to be these characters or respond as if you are them. You are a separate entity having a conversation with these characters.

FORMAT GUIDELINES:
- Text in "quotes" represents spoken dialogue by the character
- Text in *asterisks* represents actions performed by the character
- Text without quotes or asterisks is descriptive text or additional context"""
                
                # Add user character descriptions to the system prompt
                user_char_section = self.user_characters_manager.get_system_prompt_section(
                    self.character_names[channel_id]
                )
                if user_char_section:
                    enhanced_system_prompt += user_char_section
            
            # Add lorebook entries to the system prompt
            # Use the message content to find relevant lorebook entries
            lorebook_section = self.lorebook_manager.get_system_prompt_section(message)
            if lorebook_section:
                enhanced_system_prompt += "\n\n" + lorebook_section
            
            # Build messages
            messages = []
            if enhanced_system_prompt:
                messages.append({"role": "system", "content": enhanced_system_prompt})
            
            # Add conversation history
            messages.extend(self.conversations[channel_id])
            
            # Add user message (use the actual message content for conversation)
            # If character name was provided, format it to show who is speaking
            if character_name:
                formatted_message = f"{character_name}: {actual_message}"
                messages.append({"role": "user", "content": formatted_message})
            else:
                messages.append({"role": "user", "content": actual_message})
            
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
                
                # Send response (split if too long)
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
            await ctx.send("Conversation history and character names cleared!")
        
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
        
        @self.command(name="character", help="Load a character card")
        async def character(ctx, character_name: str):
            """Load a character card by name."""
            try:
                self.character_manager.load_character(character_name)
                await ctx.send(f"Loaded character: {character_name}")
                # Clear conversation when switching characters
                channel_id = ctx.channel.id
                if channel_id in self.conversations:
                    self.conversations[channel_id] = []
            except FileNotFoundError:
                await ctx.send(f"Character not found: {character_name}")
        
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
`!preset <name>` - Load a preset
`!presets` - List available presets
`!character <name>` - Load a character card
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
            
            # Check if there's a conversation
            if channel_id not in self.conversations or len(self.conversations[channel_id]) < 2:
                await ctx.send("No previous message to regenerate. Use !chat first.")
                return
            
            # Get the last user message (should be second to last in history)
            last_user_msg = None
            for msg in reversed(self.conversations[channel_id]):
                if msg["role"] == "user":
                    last_user_msg = msg["content"]
                    break
            
            if not last_user_msg:
                await ctx.send("No user message found to regenerate.")
                return
            
            # Get system prompt
            system_prompt = self.get_system_prompt()
            
            # Build messages (exclude last assistant response)
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            # Add conversation history except the last assistant message
            conv_without_last = self.conversations[channel_id][:-1] if self.conversations[channel_id] else []
            messages.extend(conv_without_last)
            
            # Add the last user message again
            messages.append({"role": "user", "content": last_user_msg})
            
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
                
                # Send response (split if too long)
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
            
            # Send response
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
            
            # Send response
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
    
    async def on_ready(self):
        """Called when bot is ready."""
        print(f"Bot is ready! Logged in as {self.user}")
