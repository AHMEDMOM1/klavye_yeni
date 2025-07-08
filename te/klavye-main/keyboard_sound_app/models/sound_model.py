from keyboard_sound_app.utils.database import Database

class SoundModel:
    def __init__(self):
        self.db = Database()
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS sound_settings (
            user_id INTEGER,
            sound_path TEXT,
            volume REAL DEFAULT 1.0,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
        self.db.execute(query)

    def save_sound_setting(self, user_id, sound_path, volume=1.0):
        self.db.execute("DELETE FROM sound_settings WHERE user_id = ?", (user_id,))
        query = "INSERT INTO sound_settings (user_id, sound_path, volume) VALUES (?, ?, ?)"
        self.db.execute(query, (user_id, sound_path, volume))

    def get_sound_setting(self, user_id):
        query = "SELECT sound_path, volume FROM sound_settings WHERE user_id = ?"
        return self.db.fetch_one(query, (user_id,))