"""Main entry point for Discord bot with web server."""
import asyncio
import threading
import time
from config_manager import ConfigManager
from discord_bot import DiscordBot
from web_server import WebServer

def run_web_server(config_manager: ConfigManager):
    """Run the web server in a separate thread."""
    web_config = config_manager.get("web_server", {})
    web_server = WebServer(config_manager)
    web_server.run(
        host=web_config.get("host", "0.0.0.0"),
        port=web_config.get("port", 5000),
        debug=False
    )

async def run_discord_bot(config_manager: ConfigManager):
    """Run the Discord bot."""
    bot = DiscordBot(config_manager)
    token = config_manager.get("discord_token")
    
    if not token or token == "YOUR_DISCORD_BOT_TOKEN":
        print("Error: Discord token not configured!")
        print("Please update config.json with your Discord bot token.")
        print("You can also configure the bot at http://localhost:5000")
        return
    
    try:
        await bot.start(token)
    except Exception as e:
        print(f"Error starting Discord bot: {e}")

def main():
    """Main function to run both web server and Discord bot."""
    print("=" * 60)
    print("Discord Bot with OpenAI Integration and Preset System")
    print("=" * 60)
    
    # Load configuration
    config_manager = ConfigManager()
    
    # Start web server in a separate thread
    web_thread = threading.Thread(
        target=run_web_server,
        args=(config_manager,),
        daemon=True
    )
    web_thread.start()
    
    web_config = config_manager.get("web_server", {})
    port = web_config.get("port", 5000)
    print(f"\n🌐 Web configuration interface starting at http://localhost:{port}")
    print("   Configure your bot settings, presets, and character cards through the web UI")
    print("   Please wait a moment for the web server to fully initialize...")
    
    # Give web server time to start
    time.sleep(2)
    print(f"   ✅ Web interface should now be accessible at http://localhost:{port}")
    
    # Run Discord bot
    print("\n🤖 Starting Discord bot...")
    
    try:
        asyncio.run(run_discord_bot(config_manager))
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down...")

if __name__ == "__main__":
    main()
