"""
Font utility module with fallback support for missing fonts.
If Space Grotesk is not available, falls back to system fonts.
"""
import customtkinter as ctk

# Primary font choice with fallback
PRIMARY_FONT = "Space Grotesk"
FALLBACK_FONT = "Segoe UI"
MONOSPACE_FONT = "Consolas"
MONOSPACE_FALLBACK = "Courier New"

def get_font(family: str = PRIMARY_FONT, size: int = 12, weight: str = "normal", slant: str = "roman"):
    """
    Create a CTkFont with automatic fallback if the primary font isn't available.
    
    Args:
        family: Primary font family name
        size: Font size in points
        weight: Font weight ('normal', 'bold')
        slant: Font slant ('roman', 'italic')
    
    Returns:
        ctk.CTkFont object with fallback support
    """
    try:
        return ctk.CTkFont(family=family, size=size, weight=weight, slant=slant)
    except:
        # Fallback: Try with Segoe UI or Courier New
        fallback = FALLBACK_FONT if family == PRIMARY_FONT else MONOSPACE_FALLBACK
        try:
            return ctk.CTkFont(family=fallback, size=size, weight=weight, slant=slant)
        except:
            # Final fallback: Use system default
            return ctk.CTkFont(size=size, weight=weight, slant=slant)
