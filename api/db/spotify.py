import psycopg2
import pprint
from typing import List
import json

from models.spotify import SpotifyUser, SpotifyPlaylist, SpotifyTrack, SpotifyUpdate

'''---------------------------------'''
'''       Database Connection       '''
'''---------------------------------'''

def connect_to_db():
  '''Connects to the database and returns the connection and cursor.'''
  con = psycopg2.connect(
    host='localhost',
    database='social_media_dashboard',
    user='postgres',
    password='postgres'
  )
  cur = con.cursor()
  return con, cur


'''---------------------------------'''
'''Spotify User CRUD Operations'''
'''---------------------------------'''
def create_spotify_user(cur, con, user: SpotifyUser) -> int:
  '''Creates a new Spotify user in the database, and returns the id.'''
  cur.execute(
    'INSERT INTO spotify.user (name, spotify_id) VALUES (%s, %s) RETURNING id;',
    (user.name, user.spotify_id)
  )
  con.commit()
  return cur.fetchone()[0]

def get_spotify_user(cur, spotify_id: str) -> SpotifyUser | None:
  '''Returns the Spotify user with the given spotify_id.'''
  cur.execute(
    'SELECT * FROM spotify.user WHERE spotify_id = %s;',
    (spotify_id,)
  )
  user = cur.fetchone()
  if not user:
    return None
  return SpotifyUser(id=user[0], name=user[1], spotify_id=user[2])

def get_spotify_users(cur) -> List[SpotifyUser]:
  '''Returns all Spotify users.'''
  cur.execute('SELECT * FROM spotify.user;')
  users = cur.fetchall()
  return [SpotifyUser(id=user[0], name=user[1], spotify_id=user[2]) for user in users]

def update_spotify_user(cur, con, user: SpotifyUser) -> None:
  '''Updates the Spotify user with the given id.'''
  cur.execute(
    'UPDATE spotify.user SET name = %s, spotify_id = %s WHERE id = %s;',
    (user.name, user.spotify_id, user.id)
  )
  con.commit()

def delete_spotify_user(cur, con, user_id: int) -> None:
  '''Deletes the Spotify user with the given id.'''
  cur.execute('DELETE FROM spotify.user WHERE id = %s;', (user_id,))
  con.commit()

'''---------------------------------'''
'''Spotify Playlist CRUD Operations'''
'''---------------------------------'''
def create_spotify_playlist(cur, con, playlist: SpotifyPlaylist) -> int:
  '''Creates a new Spotify playlist in the database, and returns the id.'''
  cur.execute(
    'INSERT INTO spotify.playlist (name, spotify_id, snapshot_id, user_id) VALUES (%s, %s, %s, %s) RETURNING id;',
    (playlist.name, playlist.spotify_id, playlist.snapshot_id, playlist.user_id)
  )
  con.commit()
  return cur.fetchone()[0]

def get_spotify_playlist(cur, playlist_id: int) -> SpotifyPlaylist:
  '''Returns the Spotify playlist with the given id.'''
  cur.execute(
    'SELECT * FROM spotify.playlist WHERE id = %s;',
    (playlist_id,)
  )
  playlist = cur.fetchone()
  return SpotifyPlaylist(id=playlist[0], name=playlist[1], spotify_id=playlist[2], snapshot_id=playlist[3], user_id=playlist[4])

def get_all_spotify_playlists(cur) -> List[SpotifyPlaylist]:
  '''Returns all Spotify playlists.'''
  cur.execute('SELECT * FROM spotify.playlist;')
  playlists = cur.fetchall()
  return [SpotifyPlaylist(id=playlist[0], name=playlist[1], spotify_id=playlist[2], snapshot_id=playlist[3], user_id=playlist[4]) for playlist in playlists]

def get_spotify_playlists(cur, user_id) -> List[SpotifyPlaylist]:
  '''Returns all Spotify playlists for the given user, sorted by the last added playlist.'''
  cur.execute(
    'SELECT DISTINCT on (spotify_id) * FROM (SELECT * FROM spotify.playlist ORDER BY id DESC) WHERE user_id = %s ORDER BY spotify_id DESC;',
    (user_id,)
  )
  playlists = cur.fetchall()
  return [SpotifyPlaylist(id=playlist[0], name=playlist[1], spotify_id=playlist[2], snapshot_id=playlist[3], user_id=playlist[4]) for playlist in playlists]

def get_spotify_playlist(cur: psycopg2.extensions.cursor, spotify_playlist_id: str) -> SpotifyPlaylist:
  '''Returns the Spotify playlist with the given id.'''
  cur.execute(
    'SELECT * FROM spotify.playlist WHERE spotify_id=%s;',
    (spotify_playlist_id,)
  )
  playlist = cur.fetchone()
  return SpotifyPlaylist(id=playlist[0], name=playlist[1], spotify_id=playlist[2], snapshot_id=playlist[3], user_id=playlist[4])

def get_latest_spotify_playlist(cur: psycopg2.extensions.cursor, user_id: int) -> SpotifyPlaylist:
  '''Returns the latest Spotify playlist for the given user.'''
  cur.execute(
    'SELECT * FROM spotify.playlist WHERE user_id=%s ORDER BY id DESC LIMIT 1;',
    (user_id,)
  )
  playlist = cur.fetchone()
  return SpotifyPlaylist(id=playlist[0], name=playlist[1], spotify_id=playlist[2], snapshot_id=playlist[3], user_id=playlist[4])

def update_spotify_playlist(cur, con, playlist: SpotifyPlaylist) -> None:
  '''Updates the Spotify playlist with the given id.'''
  cur.execute(
    'UPDATE spotify.playlist SET name = %s, spotify_id = %s, snapshot_id = %s, user_id = %s WHERE id = %s;',
    (playlist.name, playlist.spotify_id, playlist.snapshot_id, playlist.user_id, playlist.id)
  )
  con.commit()

def delete_spotify_playlist(cur, con, playlist_id: int) -> None:
  '''Deletes the Spotify playlist with the given id.'''
  cur.execute('DELETE FROM spotify.playlist WHERE id = %s;', (playlist_id,))
  con.commit()

'''---------------------------------'''
'''Spotify Track CRUD Operations'''
'''---------------------------------'''
def create_spotify_track(cur, con, track: SpotifyTrack) -> int:
  '''Creates a new Spotify track in the database, and returns the id.'''
  cur.execute(
    'INSERT INTO spotify.track (name, spotify_id, uri, "order", playlist_id) VALUES (%s, %s, %s, %s, %s) RETURNING id;',
    (track.name, track.spotify_id, track.uri, track.order, track.playlist_id)
  )
  con.commit()
  return cur.fetchone()[0]

def get_spotify_track(cur, track_id: int) -> SpotifyTrack:
  '''Returns the Spotify track with the given id.'''
  cur.execute(
    'SELECT * FROM spotify.track WHERE id = %s;',
    (track_id,)
  )
  track = cur.fetchone()
  return SpotifyTrack(id=track[0], user_id=track[1], playlist_id=track[2], action=track[3], created_at=track[4])

def get_spotify_tracks(cur, playlist_id: int) -> List[SpotifyTrack]:
  '''Returns all Spotify tracks.'''
  cur.execute(f'SELECT * FROM spotify.track WHERE playlist_id={playlist_id};')
  # id: int | None
  # name: str
  # spotify_id: str
  # uri: str
  # order: int
  # playlist_id: int
  tracks = cur.fetchall()
  return [SpotifyTrack(id=track[0], name=track[1], spotify_id=track[2], uri=track[3], order=track[4], playlist_id=track[5]) for track in tracks]

def update_spotify_track(cur, con, track: SpotifyTrack) -> None:
  '''Updates the Spotify track with the given id.'''
  cur.execute(
    'UPDATE spotify.track SET user_id = %s, playlist_id = %s, action = %s, created_at = %s WHERE id = %s;',
    (track.user_id, track.playlist_id, track.action, track.created_at, track.id)
  )
  con.commit()

def delete_spotify_track(cur, con, track_id: int) -> None:
  '''Deletes the Spotify track with the given id.'''
  cur.execute('DELETE FROM spotify.track WHERE id = %s;', (track_id,))
  con.commit()

'''---------------------------------'''
'''Spotify Update CRUD Operations'''
'''---------------------------------'''
def create_spotify_update(cur, con, update: SpotifyUpdate) -> int:
  '''Creates a new Spotify update in the database, and returns the id.'''
  cur.execute(
    'INSERT INTO spotify.update (user_id, playlist_id, action, created_at) VALUES (%s, %s, %s, %s) RETURNING id;',
    (update.user_id, update.playlist_id, update.action, update.created_at)
  )
  con.commit()
  return cur.fetchone()[0]

def get_spotify_update(cur, update_id: int) -> SpotifyUpdate:
  '''Returns the Spotify update with the given id.'''
  cur.execute(
    'SELECT * FROM spotify.update WHERE id = %s;',
    (update_id,)
  )
  update = cur.fetchone()
  return SpotifyUpdate(id=update[0], user_id=update[1], playlist_id=update[2], action=update[3], created_at=update[4])

def get_spotify_updates(cur) -> List[SpotifyUpdate]:
  '''Returns all Spotify updates.'''
  cur.execute('SELECT * FROM spotify.update;')
  updates = cur.fetchall()
  return [SpotifyUpdate(id=update[0], user_id=update[1], playlist_id=update[2], action=update[3], created_at=update[4]) for update in updates]

def update_spotify_update(cur, con, update: SpotifyUpdate) -> None:
  '''Updates the Spotify update with the given id.'''
  cur.execute(
    'UPDATE spotify.update SET user_id = %s, playlist_id = %s, action = %s, created_at = %s WHERE id = %s;',
    (update.user_id, update.playlist_id, update.action, update.created_at, update.id)
  )
  con.commit()

def delete_spotify_update(cur, con, update_id: int) -> None:
  '''Deletes the Spotify update with the given id.'''
  cur.execute('DELETE FROM spotify.update WHERE id = %s;', (update_id,))
  con.commit()