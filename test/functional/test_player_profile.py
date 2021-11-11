import unittest
from source.models import Player
from source import db
from werkzeug.security import generate_password_hash


class TestPlayerProfile(unittest.TestCase):
    def test_create_users_w_duplicate_emails(self):
        Player.query.delete()
        player1 = Player(email='password@gmail.com', player_name='password', password=generate_password_hash('password', method='sha256'))
        player2 = Player(email='password@gmail.com', player_name='password2', password=generate_password_hash('password2', method='sha256'))
        db.session.add(player1)
        self.assertRaises(Exception, db.session.add(player2))

    def test_change_to_duplicate_email(self):
        Player.query.delete()
        player1 = Player(email='password1@gmail.com', player_name='password', password=generate_password_hash('password', method='sha256'))
        player2 = Player(email='password2@gmail.com', player_name='password2', password=generate_password_hash('password2', method='sha256'))
        db.session.add(player1)
        db.session.add(player2)

        player2 = Player.query.filter_by(email='password2@gmail.com').first()
        player2.email = 'password1@gmail.com'
        self.assertRaises(Exception, db.session.commit())


if __name__ == '__main__':
    unittest.main()
