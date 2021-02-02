function playerClick(playerStr) {
    const clickedPlayer = JSON.parse(playerStr);
    document.getElementById('currPlayer').innerHTML = clickedPlayer.name;
    document.getElementById('playerPosition').innerHTML = 'Position: ' + clickedPlayer.position;
    document.getElementById('playerTeam').innerHTML = clickedPlayer.team;
    document.getElementById('id_player_id').value = clickedPlayer.id;

    if (clickedPlayer.position === "QB") {
        document.getElementById('yards').innerHTML = "Passing Yards: " + clickedPlayer.passingyds;
        document.getElementById('td').innerHTML = "Passing TDs: " + clickedPlayer.passingtds;
        document.getElementById('turnovers').innerHTML = "Interceptions: " + clickedPlayer.interceptions;
    }
    else if (clickedPlayer.position === "RB") {
        document.getElementById('yards').innerHTML = "Rushing Yards: " + clickedPlayer.rushingyds;
        document.getElementById('td').innerHTML = "Rushing TDs: " + clickedPlayer.rushingtds;
        document.getElementById('turnovers').innerHTML = "Fumbles Lost: " + clickedPlayer.fumbles;
    }
    else if (clickedPlayer.position === "WR") {
        document.getElementById('yards').innerHTML = "Receiving Yards: " + clickedPlayer.recyds;
        document.getElementById('td').innerHTML = "Receiving TDs: " + clickedPlayer.rectds;
        document.getElementById('turnovers').innerHTML = "Fumbles Lost: " + clickedPlayer.fumbles;
    }
    else {
        document.getElementById('yards').innerHTML = "n/a";
        document.getElementById('td').innerHTML = "n/a";
        document.getElementById('turnovers').innerHTML = "n/a";
    }

    const draftList = document.getElementById('draftOrder');
    draftList.removeChild(draftlist.childNodes[0]);
    return false
}

