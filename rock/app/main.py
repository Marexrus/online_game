import sqlite3
import game.game as gm

def main():
    connect=sqlite3.connect("database//database.db")
    cursor=connect.cursor()
    
    game=gm.Game()
    game.main()

if __name__ == "__main__":
    main()
