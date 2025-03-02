import React, { useContext, useEffect } from "react";
import axios from "axios";

import { DashboardContext } from "../../../context/dashboard_context";
import { IoChevronDownSharp } from "react-icons/io5";
import { IoChevronUpSharp } from "react-icons/io5";
import SpotifyPlaylist from "./SpotifyPlaylist";

import './SpotifyUser.css';

export default function SpotifyUser(props: { name: string, id: string }) {
  const context = useContext(DashboardContext);

  useEffect(() => {
    axios.get(`http://localhost:8000/api/spotify/playlists/${context?.selectedUser}`)
      .then((response) => {
        console.log(response.data)
        let playlists = response.data.map((playlist: any) => playlist);
        context?.setPlaylists(playlists);
      });
  }, [context?.selectedUser]);

  if(context?.selectedUser === props['id']) {
    return (
      <>
        <div className="spotify-user-container selected" onClick={() => context?.setSelectedUser('')}>
          <p>{props['name']}</p>
          <IoChevronUpSharp />
        </div>
        {
          context?.playlists.map((playlist) => {
            console.log(playlist)
            console.log(context?.selectedUser)
            if (playlist['user_id'] === context?.selectedUser) {
              return <SpotifyPlaylist name={playlist['name']} id={playlist['id']} />
            }
          })
        }
      </>
    );
  }

  return (
    <div className="spotify-user-container" onClick={() => context?.setSelectedUser(props['id'])}>
      <p>{props['name']}</p>
      <IoChevronDownSharp />
    </div>
  );
}