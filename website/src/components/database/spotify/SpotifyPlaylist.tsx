import React, { useContext, useEffect } from "react";
import { DashboardContext } from "../../../context/dashboard_context";
import { IoChevronDownSharp } from "react-icons/io5";
import { IoChevronUpSharp } from "react-icons/io5";
import SpotifyTrack from './SpotifyTrack';

import './SpotifyPlaylist.css';
import axios from "axios";

export default function SpotifyPlaylist(props: { name: string, id: string }) {
  const context = useContext(DashboardContext);

  useEffect(() => {
    if(context?.selectedPlaylist === props['id']) {
      axios.get(`http://localhost:3000/api/spotify/tracks/${props.id}`)
        .then((response) => {
          let tracks = response.data.map((track: any) => track);
          context?.setTracks(tracks);
        });
    }
  }, [context?.selectedPlaylist]);

  if(context?.selectedPlaylist === props['id']) {
    return (
      <>
        <div className="spotify-playlist-container selected" onClick={() => context?.setSelectedPlaylist('')}>
          <p>{props.name}</p>
          <IoChevronUpSharp />
        </div>
        {
          context?.tracks.map((track) => {
            return <SpotifyTrack name={track['name']} id={track['id']}/>
          })
        }
      </>
    );
  }

  return (
    <>
      <div className="spotify-playlist-container" onClick={() => context?.setSelectedPlaylist(props['id'])}>
        <p>{props.name}</p>
        <IoChevronDownSharp />
      </div>
    </>
  )
}