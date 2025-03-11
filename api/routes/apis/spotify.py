from fastapi import APIRouter
from spotipy.oauth2 import SpotifyClientCredentials
from deepdiff import DeepDiff
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
import spotipy
import os
import re
import datetime

from db.spotify import connect_to_db, create_spotify_track, create_spotify_update
from db.spotify import get_spotify_user, get_spotify_playlists, get_spotify_updates, get_spotify_tracks, get_all_spotify_playlists, get_spotify_users
from db.spotify import get_spotify_user_by_id
from db.spotify import create_spotify_playlist, create_spotify_user
from models.spotify import SpotifyPlaylist, SpotifyUser, SpotifyTrack, SpotifyUpdate

load_dotenv()

router = APIRouter(
  prefix="/api/spotify",
  tags=["spotify"],
  responses={404: {"description": "Not found"}},
)

class NewUser(BaseModel):
  spotify_id: str

class UserID(BaseModel):
  user_id: str

class APIKey(BaseModel):
  client_id: str
  client_secret: str

'''
---------------------------------
Spotify User Routes
---------------------------------
'''
'''Add a new user to the database.'''
@router.post('/new-user')
async def new_user(new_user: NewUser):
  # Check if the user already exists; if so, return the user.
  con, cur = connect_to_db()
  db_user = get_spotify_user(cur, new_user.spotify_id)
  if db_user:
    return db_user

  # Get the user from the Spotify API
  client_credentials_manager = SpotifyClientCredentials(
    client_id=os.getenv('SPOTIFY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIFY_CLIENT_SECRET')
  )
  sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
  user = sp.user(new_user.spotify_id)

  # Add the user to the database.
  db_user = SpotifyUser(
    id=None,
    name=user['display_name'],
    spotify_id=user['id']
  )
  db_user.id = create_spotify_user(cur, con, db_user)
  
  # Add playlists and tracks to the database.
  playlists = sp.user_playlists(new_user.spotify_id)
  for playlist in playlists['items']:
    # Add the playlist to the database.
    db_playlist = SpotifyPlaylist(
      id=None,
      name=playlist['name'],
      spotify_id=playlist['id'],
      snapshot_id=playlist['snapshot_id'],
      user_id=db_user.id
    )
    db_playlist.id = create_spotify_playlist(cur, con, db_playlist)
    
    # Get the tracks of the playlist.
    tracks = sp.playlist_tracks(playlist['id'], fields='items(track(name, id, uri))')
    for i, track in enumerate(tracks['items']):
      if not track['track']:
        continue
      db_track = SpotifyTrack(
        id=None,
        name=track['track']['name'],
        spotify_id=track['track']['id'],
        uri=track['track']['uri'],
        order=i,
        playlist_id=db_playlist.id
      )
      create_spotify_track(cur, con, db_track)
  
  con.close()
  return db_user

'''Get a user from the database.'''
@router.get('/user/{user_id}')
async def get_spotify_user_route(user_id: str):
  con, cur = connect_to_db()
  user = get_spotify_user(cur, user_id)
  con.close()
  return user

@router.get('/users')
async def get_spotify_users_route():
  con, cur = connect_to_db()
  users = get_spotify_users(cur)
  con.close()
  return users

'''
---------------------------------
Spotify Update Routes
---------------------------------
'''
'''Check for updates in the Spotify API.'''
@router.get('/{user_id}/check-updates')
async def check_spotify_updates(user_id: str):
  con, cur = connect_to_db()
  client_credentials_manager = SpotifyClientCredentials(
    client_id=os.getenv('SPOTIFY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIFY_CLIENT_SECRET')
  )
  sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
  api_playlists = sp.user_playlists(user_id)

  # Get the updates from the api and the database.
  db_user: SpotifyUser = get_spotify_user_by_id(cur, user_id)
  db_playlist: List[SpotifyPlaylist] = get_spotify_playlists(cur, db_user.id)
  db_playlist_snapshots = [playlist.snapshot_id for playlist in db_playlist]
  api_playlist_snapshots = [playlist['snapshot_id'] for playlist in api_playlists['items']]
  playlist_updates = DeepDiff(db_playlist_snapshots, api_playlist_snapshots)

  if len(playlist_updates) == 0:
    return 'No updates found between the API response and the database response.'
  
  print('Updates found between the API response and the database response.')

  for update_type in playlist_updates:
    # Add the playlist to the database.
    for value in playlist_updates[update_type]:
      playlist_index = int(re.search(r'[(\d+)]', value).group())
      playlist = api_playlists['items'][playlist_index]
      db_playlist = SpotifyPlaylist(
        id=None,
        name=playlist['name'],
        spotify_id=playlist['id'],
        snapshot_id=playlist['snapshot_id'],
        user_id=db_user.id
      )
      db_playlist.id = create_spotify_playlist(cur, con, db_playlist)

      create_spotify_update(cur, con, SpotifyUpdate(
        id=None,
        playlist_id=db_playlist.id,
        user_id=db_user.id,
        updates=playlist_updates,
        action=update_type,
        created_at=datetime.datetime.now()
      ))

      # Get the tracks of the playlist.
      tracks = sp.playlist_tracks(playlist['id'], fields='items(track(name, id, uri))')
      for i, track in enumerate(tracks['items']):
        if not track['track']:
          continue
        db_track = SpotifyTrack(
          id=None,
          name=track['track']['name'],
          spotify_id=track['track']['id'],
          uri=track['track']['uri'],
          order=i,
          playlist_id=db_playlist.id
        )
        create_spotify_track(cur, con, db_track)
  
  return 'Updates found between the API response and the database response.'

'''Get the updates from the database.'''
@router.get('/updates')
async def get_spotify_updates_route():
  con, cur = connect_to_db()
  updates = get_spotify_updates(cur)
  con.close()
  return updates

'''
---------------------------------
Spotify Playlists Routes
---------------------------------
'''
'''Get playlists from the database.'''
@router.get('/playlists/{user_id}')
async def get_spotify_playlists_route(user_id: str):
  con, cur = connect_to_db()
  playlists = []
  playlists = get_spotify_playlists(cur, user_id)
  con.close()
  return playlists

'''Get all playlists from the database.'''
@router.get('/playlists')
async def get_all_spotify_playlists_route():
  con, cur = connect_to_db()
  playlists = get_all_spotify_playlists(cur)
  con.close()
  return playlists

'''
---------------------------------
Spotify Tracks Routes
---------------------------------
'''
'''Get tracks from the database.'''
@router.get('/tracks/{playlist_id}')
async def get_spotify_tracks_route(playlist_id: str):
  con, cur = connect_to_db()
  tracks = get_spotify_tracks(cur, playlist_id)
  con.close()
  return tracks

'''
---------------------------------
Spotify API Key Routes
---------------------------------
'''
@router.post('/api-key')
async def set_api_key(api_key: APIKey):
  previous_keys = ''

  if not os.path.exists('.env'):
    f = open('.env', 'w+')
    f.close()

  with open('.env', 'r') as f:
    previous_keys = f.read()

  print(previous_keys)

  if previous_keys.find('SPOTIFY_CLIENT_ID') == -1 or previous_keys.find('SPOTIFY_CLIENT_SECRET') == -1:
    with open('.env', 'w+') as f:
      f.write(f'SPOTIFY_CLIENT_ID={api_key.client_id}\n')
      f.write(f'SPOTIFY_CLIENT_SECRET={api_key.client_secret}\n')
      f.close()
  else:
    previous_keys = re.sub(r'SPOTIFY_CLIENT_ID=.*\n', f'SPOTIFY_CLIENT_ID={api_key.client_id}\n', previous_keys)
    previous_keys = re.sub(r'SPOTIFY_CLIENT_SECRET=.*\n', f'SPOTIFY_CLIENT_SECRET={api_key.client_secret}\n', previous_keys)
    with open('.env', 'w') as f:
      f.write(previous_keys)
      f.close()

  load_dotenv()
  return 'API Key set.' 