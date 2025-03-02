import React from 'react';

import './Sidebar.css'
import SpotifyLogo from '../assets/spotify.png';

export default function Sidebar() {
  return (
    <div id="sidebar">
      <p>Apps</p>
      <button className='sidebar-button'>
        <img src={SpotifyLogo} alt="" id="spotify-logo" />
      </button>
    </div>
  )
}