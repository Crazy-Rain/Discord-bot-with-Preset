"""Main entry point for Discord bot with web server."""
import asyncio
import threading
import time
import signal
import sys
from config_manager import ConfigManager
from discord_bot import DiscordBot
from web_server import WebServer

# Global bot instance that web server can access
bot_instance = None
# Global flag for graceful shutdown
shutdown_flag = False

def run_web_server(config_manager: ConfigManager):
    """Run the web server in a separate thread."""
    web_config = config_manager.get("web_server", {})
    web_server = WebServer(config_manager, bot_instance)
    web_server.run(
        host=web_config.get("host", "0.0.0.0"),
        port=web_config.get("port", 5000),
        debug=False
    )

async def run_discord_bot(config_manager: ConfigManager):
    """Run the Discord bot with automatic reconnection."""
    global bot_instance, shutdown_flag
    token = config_manager.get("discord_token")
    
    if not token or token == "YOUR_DISCORD_BOT_TOKEN":
        print("Error: Discord token not configured!")
        print("Please update config.json with your Discord bot token.")
        print("You can also configure the bot at http://localhost:5000")
        return
    
    # Run bot with automatic reconnection on connection errors
    max_retries = 5
    retry_count = 0
    retry_delay = 5  # seconds
    
    while not shutdown_flag and retry_count < max_retries:
        try:
            # Always create a fresh bot instance for each connection attempt
            # (cannot reuse a bot instance after it has been started/closed)
            if retry_count == 0:
                print("🔄 Creating bot instance for initial connection...")
            else:
                print("🔄 Creating fresh bot instance for reconnection...")
            bot_instance = DiscordBot(config_manager)
            
            await bot_instance.start(token)
            # If we get here, bot stopped normally
            break
        except KeyboardInterrupt:
            # Handle graceful shutdown
            break
        except Exception as e:
            retry_count += 1
            if retry_count < max_retries and not shutdown_flag:
                print(f"❌ Bot connection error: {e}")
                print(f"🔄 Retrying in {retry_delay} seconds... (Attempt {retry_count}/{max_retries})")
                # Close the failed bot instance before retrying
                if bot_instance and not bot_instance.is_closed():
                    try:
                        await bot_instance.close()
                    except:
                        pass
                await asyncio.sleep(retry_delay)
                # Increase retry delay exponentially (up to 30 seconds)
                retry_delay = min(retry_delay * 2, 30)
            else:
                print(f"❌ Bot failed to connect after {max_retries} attempts: {e}")
                raise
    
    # Ensure proper cleanup
    if bot_instance and not bot_instance.is_closed():
        await bot_instance.close()

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    global shutdown_flag
    print("\n\n👋 Shutdown signal received. Cleaning up...")
    shutdown_flag = True
    sys.exit(0)

def main():
    """Main function to run both web server and Discord bot."""
    global bot_instance, shutdown_flag
    
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("=" * 60)
    print("Discord Bot with OpenAI Integration and Preset System")
    print("=" * 60)
    
    # Load configuration
    config_manager = ConfigManager()
    
    # Initialize bot instance placeholder (web server will access via global)
    # The actual connection will use fresh instances created in run_discord_bot()
    bot_instance = DiscordBot(config_manager)
    
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
    
    token = config_manager.get("discord_token")
    if not token or token == "YOUR_DISCORD_BOT_TOKEN":
        print("Error: Discord token not configured!")
        print("Please update config.json with your Discord bot token.")
        print("You can also configure the bot at http://localhost:5000")
        # Keep the web server running even if bot can't start
        try:
            while not shutdown_flag:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n👋 Shutting down...")
        return
    
    try:
        # Run bot with reconnection handling
        asyncio.run(run_discord_bot(config_manager))
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down...")
    finally:
        # Ensure bot is properly closed
        if bot_instance and not bot_instance.is_closed():
            try:
                # Use a new event loop for cleanup if the main one is closed
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(bot_instance.close())
                loop.close()
            except Exception as e:
                print(f"Error during cleanup: {e}")

if __name__ == "__main__":
    main()
