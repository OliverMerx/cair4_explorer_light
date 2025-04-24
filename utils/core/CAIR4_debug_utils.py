"""
=================================================
CAIR4 Debugging Utility (CAIR4_debug_utils.py)
=================================================

Dieses Modul enthält Debugging-Funktionen für das CAIR4-System.

Funktionen:
- `debug_print(message)`: Gibt Debug-Nachrichten aus, falls der Debug-Modus aktiv ist.
- `is_debug_mode()`: Prüft, ob der Debug-Modus aktiviert ist.
- `toggle_debug_mode()`: Aktiviert/Deaktiviert den Debug-Modus in `st.session_state`.

Verwendung:
    from utils.core.CAIR4_debug_utils import DebugUtils

    DebugUtils.debug_print("Dies ist eine Debug-Nachricht.")
"""

# === 1️⃣ Import externer Bibliotheken ===
from pylibs.streamlit_lib import streamlit as st  


class DebugUtils:
    """
    Eine Sammlung von Debugging-Methoden für das CAIR4-System.
    """

    @staticmethod
    def debug_print(message: str):
        """
        Gibt Debug-Nachrichten aus, falls der Debug-Modus aktiv ist.

        Args:
            message (str): Die Debug-Nachricht, die ausgegeben werden soll.
        """
        if DebugUtils.is_debug_mode():
            print(f"[DEBUG] {message}")

    @staticmethod
    def is_debug_mode() -> bool:
        """
        Prüft, ob der Debug-Modus aktiviert ist.

        Returns:
            bool: `True`, wenn der Debug-Modus aktiv ist, sonst `False`.
        """
        return st.session_state.get("debug_modus_model", False)

    @staticmethod
    def toggle_debug_mode():
        """
        Aktiviert oder deaktiviert den Debug-Modus in `st.session_state`.
        """
        st.session_state["debug_modus_model"] = not DebugUtils.is_debug_mode()
        print(f"[INFO] Debug-Modus {'aktiviert' if DebugUtils.is_debug_mode() else 'deaktiviert'}.")