import streamlit as st

class StreamlitSessionState:
    def __init__(self, key: str):
        """Initializes the StreamlitSessionState for a specific key in st.session_state.

        Args:
            key: The main key under which this class's state will be stored in st.session_state.
        """
        self._main_key = key
        if self._main_key not in st.session_state:
            st.session_state[self._main_key] = {}

    def _state(self) -> dict:
        """Returns the dictionary holding the state for this instance."""
        return st.session_state[self._main_key]

    def state_exists(self, sub_key: str) -> bool:
        """Checks if a given sub-key exists within this instance's state.

        Args:
            sub_key: The sub-key of the state variable to check.

        Returns:
            True if the sub-key exists, False otherwise.
        """
        return sub_key in self._state()

    def add_update_state(self, sub_key: str, data):
        """Adds or updates a state variable.

        Args:
            sub_key: The sub-key for the state variable.
            data: The value to store for the sub-key.
        """
        self._state()[sub_key] = data

    def get_state(self, sub_key: str):
        """Retrieves the value of a state variable.

        Args:
            sub_key: The sub-key of the state variable to retrieve.

        Returns:
            The value associated with the sub-key, or None if the sub-key doesn't exist.
        """
        return self._state().get(sub_key)

    def delete_state(self, sub_key: str):
        """Deletes a state variable.

        Args:
            sub_key: The sub-key of the state variable to delete.
        """
        if self.state_exists(sub_key):
            del self._state()[sub_key]

# Example of a class inheriting from StreamlitSessionState
class UserSettings(StreamlitSessionState):
    def __init__(self):
        super().__init__("user_settings")  # Define the main key for user settings

    def set_theme(self, theme: str):
        self.add_update_state("theme", theme)

    def get_theme(self) -> str:
        return self.get_state("theme")

    def set_notifications_enabled(self, enabled: bool):
        self.add_update_state("notifications_enabled", enabled)

    def are_notifications_enabled(self) -> bool:
        return self.get_state("notifications_enabled")

# Example Usage within a Streamlit app:
if __name__ == '__main__':
    st.title("Inherited Streamlit Session State")

    user_config = UserSettings()

    st.subheader("Theme Settings")
    current_theme = user_config.get_theme() or "light"
    new_theme = st.radio("Select Theme:", ["light", "dark"], index=["light", "dark"].index(current_theme))
    if new_theme != current_theme:
        user_config.set_theme(new_theme)
        st.rerun()

    st.write(f"Current Theme: {user_config.get_theme()}")

    st.subheader("Notification Settings")
    notifications_enabled = user_config.are_notifications_enabled() or False
    enable_notifications = st.checkbox("Enable Notifications", notifications_enabled)
    if enable_notifications != notifications_enabled:
        user_config.set_notifications_enabled(enable_notifications)
        st.rerun()

    st.write(f"Notifications Enabled: {user_config.are_notifications_enabled()}")

    st.subheader("Checking and Deleting State")
    if user_config.state_exists("theme"):
        if st.button("Delete Theme Setting"):
            user_config.delete_state("theme")
            st.rerun()
        st.write("Theme setting exists.")
    else:
        st.write("Theme setting does not exist.")