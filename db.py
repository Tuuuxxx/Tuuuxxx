import sqlite3

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            return bool(len(result))
        
    def add_user(self, user_id, referrer_id=None):
        with self.connection:
            if referrer_id != None:
                return self.cursor.execute("INSERT INTO `users` (`user_id`, `referrer_id`) VALUES (?, ?)", (user_id, referrer_id,))
            else:
                return self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,)).fetchone()
    def add_coin(self, user_id, value):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `balance` = `balance` + ? WHERE `user_id` = ?", ( value, user_id,))
    
    def remove_coin(self, user_id, value):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `balance` = `balance` - ? WHERE `user_id` = ?", ( value, user_id,))
    
    def view_balance(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT `balance` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchone()