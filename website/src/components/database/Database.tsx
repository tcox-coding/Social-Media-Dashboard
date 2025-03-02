import React, { useState } from 'react';
import { IoAddOutline } from "react-icons/io5";
import { useContext } from 'react';
import { Popover } from 'react-tiny-popover'
import { DashboardContext } from '../../context/dashboard_context';

import SpotifyUser from './spotify/SpotifyUser';
import axios from 'axios';

import './Database.css';

export default function Database() {
  const [newUserrDialogOpen, setNewUserDialogOpen] = useState(false);
  const [newAPIKeyDialogOpen, setAPIKeyDialogOpen] = useState(false);
  const dashboardContext = useContext(DashboardContext);

  // New User Dialog
  const addUser = () => {
    setNewUserDialogOpen(true);
  }

  const closeNewUserPopover = () => {
    setNewUserDialogOpen(false);
  };

  const addNewUser = () => {
    // TODO:
    let new_username = (document.getElementById('spotify-new-username') as HTMLInputElement)?.value;
    axios.post('http://localhost:8000/api/spotify/new-user', {spotify_id: new_username})
      .then((response) => {
        setNewUserDialogOpen(false);
        dashboardContext?.setAddedNewUser(true);
      });
  }

  // API Key Dialog
  const addAPIKey = () => {
    setAPIKeyDialogOpen(true);
  }

  const closeNewAPIKeyModal = () => {
    setAPIKeyDialogOpen(false);
  }

  const addNewAPIKey = () => {
    let new_client_id = (document.getElementById('spotify-client-id') as HTMLInputElement)?.value;
    let new_client_secret = (document.getElementById('spotify-client-secret') as HTMLInputElement)?.value;
    axios.post('http://localhost:8000/api/spotify/api-key', {client_id: new_client_id, client_secret: new_client_secret})
      .then((response) => {
        setAPIKeyDialogOpen(false);
      });
  }


  return (
    <div id="main-content">
      <div id="database">
        <div id="button-dialog">
          <Popover
            isOpen={newUserrDialogOpen}
            positions={['bottom', 'top', 'right', 'left']}
            onClickOutside={closeNewUserPopover}
            content={(
              <div id="new-user-dialog">
                <h3>New User</h3>
                <input type="text" id='spotify-new-username' placeholder="Name" />
                <button onClick={addNewUser}>Add</button>
              </div>
            )}
          >
          <button id='add-user' onClick={addUser}>
            <IoAddOutline />
            <p>Add User</p>
          </button>
          </Popover>
          <Popover
            isOpen={newAPIKeyDialogOpen}
            positions={['bottom', 'top', 'right', 'left']}
            onClickOutside={closeNewAPIKeyModal}
            content={(
              <div id="new-user-dialog">
                <h3>New API Key</h3>
                <input type="text" id="spotify-client-id" placeholder="Spotify Client ID" />
                <input type="text" id="spotify-client-secret" placeholder="Spotify Client Secret" />
                <button onClick={addNewAPIKey}>Add</button>
              </div>
            )}
          >
            <button id='add-user' onClick={addAPIKey}>
              <IoAddOutline />
              <p>Add API Key</p>
            </button>
          </Popover>
          
        </div>
        {
          dashboardContext?.users.map((user) => {
            return <SpotifyUser name={user.name} id={user.id}/>
          })
        }
      </div>
    </div>
  )
}