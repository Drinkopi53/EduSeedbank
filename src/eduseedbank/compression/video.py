"""
Video compression system for EduSeedbank.
Optimizes educational content for LoRa transmission.
"""

import os
import subprocess
from typing import Optional


class VideoCompressor:
    """Handles compression of video content for low-bandwidth transmission."""

    def __init__(self):
        # Check if ffmpeg is available
        self.ffmpeg_available = self._check_ffmpeg()

    def _check_ffmpeg(self) -> bool:
        """Check if ffmpeg is installed and available."""
        try:
            subprocess.run(["ffmpeg", "-version"], 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL)
            return True
        except FileNotFoundError:
            return False

    def compress_video(self, input_path: str, output_path: str, 
                      target_size_mb: int = 5) -> bool:
        """
        Compress a video file to a target size.
        
        Args:
            input_path: Path to the input video file
            output_path: Path where compressed video will be saved
            target_size_mb: Target size in megabytes (default 5MB for LoRa)
            
        Returns:
            True if compression was successful, False otherwise
        """
        if not self.ffmpeg_available:
            raise RuntimeError("FFmpeg is not installed or not available in PATH")
            
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input video file not found: {input_path}")
            
        try:
            # Calculate bitrate based on target size
            # This is a simplified calculation
            target_bitrate = self._calculate_bitrate(input_path, target_size_mb)
            
            # Run ffmpeg compression
            cmd = [
                "ffmpeg",
                "-i", input_path,
                "-b:v", f"{target_bitrate}k",
                "-maxrate", f"{target_bitrate}k",
                "-bufsize", f"{target_bitrate*2}k",
                "-vf", "scale=480:270",  # Reduce resolution for low bandwidth
                "-r", "15",  # Reduce frame rate
                "-c:a", "aac",
                "-b:a", "32k",  # Low bitrate audio
                "-ac", "1",  # Mono audio
                "-y",  # Overwrite output file
                output_path
            ]
            
            result = subprocess.run(cmd, 
                                  stdout=subprocess.DEVNULL,
                                  stderr=subprocess.DEVNULL)
            
            return result.returncode == 0
        except Exception as e:
            print(f"Error compressing video: {e}")
            return False

    def _calculate_bitrate(self, input_path: str, target_size_mb: int) -> int:
        """
        Calculate target video bitrate based on target file size.
        This is a simplified calculation.
        """
        # Get video duration (simplified)
        try:
            cmd = [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                input_path
            ]
            
            result = subprocess.run(cmd, 
                                  capture_output=True, 
                                  text=True,
                                  stdout=subprocess.DEVNULL,
                                  stderr=subprocess.DEVNULL)
            
            if result.returncode == 0:
                duration = float(result.stdout.strip())
                # Simple calculation: (target_size * 8192) / duration
                # 8192 = 8 * 1024 (convert MB to kbits)
                return int((target_size_mb * 8192) / duration)
        except:
            pass
            
        # Default bitrate if we can't calculate
        return 128  # kbps