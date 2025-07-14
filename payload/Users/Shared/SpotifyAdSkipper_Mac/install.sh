#!/bin/bash
echo "Installing Spotify Ad Skipper..."

# Copy app to shared directory with root ownership
sudo mkdir -p /Users/Shared/SpotifyAdSkipper_Mac
sudo cp -R . /Users/Shared/SpotifyAdSkipper_Mac

# Set ownership to root:wheel for all copied files
sudo chown -R root:wheel /Users/Shared/SpotifyAdSkipper_Mac

# Make main shell script executable
sudo chmod +x /Users/Shared/SpotifyAdSkipper_Mac/run_ad_skipper.sh

# Copy LaunchAgent plist to current user's LaunchAgents directory
mkdir -p "$HOME/Library/LaunchAgents"
cp /Users/Shared/SpotifyAdSkipper_Mac/com.aadi.spotifyads.plist "$HOME/Library/LaunchAgents/"

# Ensure plist file ownership and permissions
chown "$USER":staff "$HOME/Library/LaunchAgents/com.aadi.spotifyads.plist"
chmod 644 "$HOME/Library/LaunchAgents/com.aadi.spotifyads.plist"

# Unload plist if already loaded (ignore errors)
launchctl unload "$HOME/Library/LaunchAgents/com.aadi.spotifyads.plist" 2>/dev/null

# Load LaunchAgent for current user
launchctl bootstrap gui/$(id -u) "$HOME/Library/LaunchAgents/com.aadi.spotifyads.plist"

# Start (kickstart) the LaunchAgent immediately
launchctl kickstart -k gui/$(id -u) com.aadi.spotifyads

echo "Installation complete. Spotify Ad Skipper is now running."
