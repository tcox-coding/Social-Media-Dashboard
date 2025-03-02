from pydantic import BaseModel
import datetime

'''Class representing rows in the spotify.user table.'''
class SpotifyUser(BaseModel):
  id: int | None
  name: str
  spotify_id: str

'''Class representing rows in the spotify.playlist table.'''
class SpotifyPlaylist(BaseModel):
  id: int | None
  name: str
  spotify_id: str
  snapshot_id: str
  user_id: int

'''Class representing rows in the spotify.track table.'''
class SpotifyTrack(BaseModel):
  id: int | None
  name: str
  spotify_id: str
  uri: str
  order: int
  playlist_id: int

'''Class representing rows in the spotify.update table.'''
class SpotifyUpdate(BaseModel):
  id: int | None
  user_id: int
  playlist_id: int
  action: str
  created_at: datetime.datetime