import React, { useState } from 'react';
import Modal from 'react-modal';
import { IoAddOutline } from "react-icons/io5";
import { useContext } from 'react';
import { DashboardContext } from '../../context/dashboard_context';

import SpotifyUser from './spotify/SpotifyUser';
import axios from 'axios';

import './Database.css';

export default function Database() {
  const [dialogOpen, setDialogOpen] = useState(false);
  const dashboardContext = useContext(DashboardContext);

  const addUser = () => {
    setDialogOpen(true);
    Modal.setAppElement('body');
  }

  const closeModal = () => {
    setDialogOpen(false);
  };


  return (
    <div id="main-content">
      <Modal
        isOpen={dialogOpen}
      >
        <form action="post">
          Example
        </form>
        <button onClick={closeModal}>X</button>
      </Modal>
      <div id="database">
        <div id="button-dialog">
          <button id='add-user' onClick={addUser}>
            <IoAddOutline />
            <p>Add User</p>
          </button>
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