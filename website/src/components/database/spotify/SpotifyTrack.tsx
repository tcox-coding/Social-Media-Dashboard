import React from "react"

import './SpotifyTrack.css';

export default function SpotifyTrack(props: { name: string, id: string }) {
  return (
    <>
      <div className="spotify-track-container">
        <p>{props.name}</p>
      </div>
    </>
  )
}