import sqlite3

CONN = sqlite3.connect('music.db')
CURSOR = CONN.cursor()

class Song:
    def __init__(self, name, album):
        self.id = None
        self.name = name
        self.album = album

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS songs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                album TEXT
            )
        """
        try:
            CURSOR.execute(sql)
            CONN.commit()
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS songs
        """
        try:
            CURSOR.execute(sql)
            CONN.commit()
        except sqlite3.Error as e:
            print(f"Error dropping table: {e}")

    def save(self):
        sql = """
            INSERT INTO songs (name, album)
            VALUES (?, ?)
        """
        try:
            CURSOR.execute(sql, (self.name, self.album))
            CONN.commit()
            self.id = CURSOR.lastrowid
        except sqlite3.Error as e:
            print(f"Error saving record: {e}")

    @classmethod
    def new_from_db(cls, row):
        return cls(row[1], row[2])

    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM songs
        """
        try:
            all_rows = CURSOR.execute(sql).fetchall()
            return [cls.new_from_db(row) for row in all_rows]
        except sqlite3.Error as e:
            print(f"Error fetching all records: {e}")

    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT *
            FROM songs
            WHERE name = ?
            LIMIT 1
        """
        try:
            song = CURSOR.execute(sql, (name,)).fetchone()
            return cls.new_from_db(song) if song else None
        except sqlite3.Error as e:
            print(f"Error finding record by name: {e}")

    @classmethod
    def create(cls, name, album):
        song = cls(name, album)
        song.save()
        return song

# Example usage:
# Song.create_table()
# song = Song.create("Song Name", "Album Name")
# Song.get_all()
# found_song = Song.find_by_name("Song Name")
# print(found_song.name) if found_song else print("Song not found")
