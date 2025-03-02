import { createContext } from "react";

interface User {
  name: string;
  id: string;
}

interface Playlist {
  name: string;
  id: string;
}

interface Track {
  name: string;
  id: string;
}

export interface DashboardContext {
  selectedUser: string | undefined;
  setSelectedUser: (selected: string) => void;
  selectedPlaylist: string | undefined;
  setSelectedPlaylist: (selected: string) => void;
  selectedTrack: string | undefined;
  setSelectedTrack: (selected: string) => void;
  users: User[];
  setUsers: (users: never[]) => void;
  playlists: Playlist[];
  setPlaylists: (playlists: never[]) => void;
  tracks: Track[];
  setTracks: (tracks: never[]) => void;
  addedNewUser: boolean;
  setAddedNewUser: (added: boolean) => void;
}

export const DashboardContext = createContext<DashboardContext | undefined>(undefined);