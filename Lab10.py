# Lab10.py
#Name: Sylvia Brown
#Date: 3/5/26

import boto3
from boto3.dynamodb.conditions import Key 

# -------------------------------------------------------
# Configuration — update REGION if your table is elsewhere
# -------------------------------------------------------
REGION = "us-east-1"
TABLE_NAME = "Playlist"


def get_table():
    """Return a reference to the DynamoDB Playlist table."""
    dynamodb = boto3.resource("dynamodb", region_name=REGION)
    return dynamodb.Table(TABLE_NAME)

def print_songs_in_playlist(playlist):
    title = playlist.get("Title", "Unknown Title")
    artist = playlist.get("Artist", "Unknown Artist")
    album = playlist.get("Album", "No ratings")


    print(f"  Title  : {title}")
    print(f"  Artist   : {artist}")
    print(f"  Album : {album}")
    print()

def print_playlist():
    """Scan the entire Playlist table and print each item (song)."""
    table = get_table()
    
    # scan() retrieves ALL items in the table.
    # For large tables you'd use query() instead — but for our small
    # dataset, scan() is fine.
    response = table.scan()
    items = response.get("Items", [])
    
    if not items:
        print("No songs found in playlist. Make sure your DynamoDB table has data.")
        return
    
    print(f"Found {len(items)} song(s):\n")
    for playlist in items:
        print_songs_in_playlist(playlist)


def create_song():
    
    title = input("Enter song title: ")
    artist = input("Enter song artist: ")
    album = input("Enter song album: ")

    song = {
        "Title": title,
        "Artist": artist,
        "Album": album,
        
    }
    table = get_table()
    table.put_item(Item=song)

    print("Song added to playlist successfully.\n")

    
def update_song():
    try:
        title = input("Enter the song title you'd like to update: ")
        album = input("Enter the album: ")
        artist = input("Enter the artist: ")

        table = get_table()
        table.update_item(
            Key={"Title": title},
            UpdateExpression="SET Album = :a, Artist = :r",
            ExpressionAttributeValues={":a": album, ":r": artist}
        )
        print("Song updated successfully.")

    except:
        print("Error updating song")


def delete_song():
    try:
        title = input("Please enter song title: ")
        table = get_table()
        table.delete_item(
            Key={"Title": title}
        )
        print(title + " deleted from playlist")
    except:
        print("Error in deleting song from playlist.")

def query_song():
    title = input("Enter a song title: ")

    table = get_table()
    response = table.get_item(Key={"Title": title})
    song = response.get("Item")

    if not song:
        print("song not found in playlist")
        return
    
    #query the song titles in playlist using my fuction from lab 9
    print_songs_in_playlist(song)


def print_menu():
    print("----------------------------")
    print("Press C: to CREATE a new song")
    print("Press R: to READ all songs")
    print("Press U: to UPDATE a song (change album)")
    print("Press D: to DELETE a song")
    print("Press Q: to QUERY a song by title")
    print("Press X: to EXIT application")
    print("----------------------------")


def main():
    input_char = ""
    while input_char.upper() != "X":
        print_menu()
        input_char = input("Choice: ")
        if input_char.upper() == "C":
            create_song()
        elif input_char.upper() == "R":
            print_playlist()
        elif input_char.upper() == "U":
            update_song()
        elif input_char.upper() == "D":
            delete_song()
        elif input_char.upper() == "Q":
            query_song()
        elif input_char.upper() == "X":
            print("exiting...")
        else:
            print("Not a valid option. Try again.")
  


main()