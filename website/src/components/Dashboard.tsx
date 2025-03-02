import './Dashboard.css';
import Sidebar from './Sidebar';
import Database from './database/Database';
import { DashboardContext } from '../context/dashboard_context';
import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function Dashboard() {
  const [selectedUser, setSelectedUser] = useState('');
  const [selectedPlaylist, setSelectedPlaylist] = useState('');
  const [selectedTrack, setSelectedTrack] = useState('');
  const [users, setUsers] = useState([]);
  const [playlists, setPlaylists] = useState([]);
  const [tracks, setTracks] = useState([]);
  const [addedNewUser, setAddedNewUser] = useState(false);

  const context = {
    selectedUser,
    setSelectedUser,
    selectedPlaylist,
    setSelectedPlaylist,
    selectedTrack,
    setSelectedTrack,
    users,
    setUsers,
    playlists,
    setPlaylists,
    tracks,
    setTracks,
    addedNewUser,
    setAddedNewUser
  }

  useEffect(() => {
    axios.get('http://localhost:8000/api/spotify/users')
      .then((response) => {
        console.log(response.data)
        let users = response.data.map((user: any) => user);
        setUsers(users)
      });
  }, [addedNewUser]);

  return (
    <DashboardContext.Provider value={context}>
      <div id="dashboard">
        <Sidebar></Sidebar>
        <Database></Database>
      </div>
    </DashboardContext.Provider>
  )
}