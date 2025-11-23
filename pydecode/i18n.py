"""
pyDecode i18n (Internationalization) Module

Stub for future translation and localization support.
Currently, supports a Hinglish translation stub (for demonstration only).

Author: Md. Yahya Ab. Wahid Mundewadi
Email: yahyabuilds@gmail.com
Organization: Dominal Group
License: MIT
"""

from typing import Dict, Optional

_supported_languages = ["en", "hi-IN-hinglish"]

# Key-based stub, real translation systems would use gettext or similar.
TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "hi-IN-hinglish": {
        "Your code has a mistake in the structure or spelling, so Python could not understand it. This often happens if you forget brackets, colons, or put things in the wrong place. 📝":
            "Aapke code me kuch galti hai structure ya spelling me, isliye Python samajh nahi paaya. Jyada tar brackets, colon ya line galat jagah likhne par hota hai. 📝",
        "Check your spelling and make sure the variable or function exists before using it.":
            "Naam sahi likha hai ya variable/function define kiya hai ya nahi, yeh dekhein.",
    }
}

def translate(text: str, lang: str = "en") -> str:
    """
    Translate the given text to the specified language, if available.
    
    Args:
        text: Original explanation text in English.
        lang: Language code (e.g., 'en', 'hi-IN-hinglish')
        
    Returns:
        Translated text if available, else original text
    """
    if lang == "en" or lang not in _supported_languages:
        return text
    lang_map = TRANSLATIONS.get(lang, {})
    return lang_map.get(text, text)

def supported_languages() -> list:
    """
    Return list of available translation languages.

    Returns:
        List of language codes as strings
    """
    return _supported_languages[:]

__all__ = ["translate", "supported_languages", "TRANSLATIONS"]
