# Fantasy_Football_App

By: Michael Whitaker

This is a prototype for an app to play fantasy football with friends. To play the game, each person chooses (drafts)
from a list of current NFL players. Then each of these fantasy team plays against someone else's fantasy team every
week. Based on the performance of the real players in their respective game, each player on the fantasy team accumulates
points - 6 points for scoring a touchdown, for example. These points are totaled and the team with the highest point total
wins.

This app is not yet complete as it is only for one player. To start, you select a player from the list in the center of the
screen. That players will then appear at the top of the screen so you can view the previous year's statistics. If you want
to select that player for your fantasy team, you should click the "Draft Player" button to add them to your fantasy team.
That player will then appear to the left of the screen. Then the computer players will select their players in order and
the draft process will cycle back to your turn. You can only choose a player when it is your turn to draft. Whoever chooses
first in the first round will choose last in the second round, then first in the third round and so forth. Once your team is
complete, click the "Finalize Draft" button to go to the matchup screen. At this time, you can only select 3 players - a
Quarterback (QB), a Running Back (RB) and a Wide Receiver (WR).

Each week, you can cycle through the pages to view the stats for each player and your fantasy team. The point totals are
what determines a winner each week. To advance to the next week, click the "Advance Week" button.

User stories:
1. As a fantasy football fan, I want to use a fantasy football app that doesn't have all the ads.

Technologies used:
Python Django, Javascript, CSS

Ideas for Improvement:
The only statistics I could find were from 2019. Ideally, I would need statistics from the current season to do this
effectively. Also, it needs to be a multiplayer game. I have created a lobby to display all the users prior to starting a 
draft, but I did not use it yet. It also needs to include options that the admin for the league can use to set the league 
scoring rules, as well as the number and type of players available for each person's fantasy roster. It will also need to 
allow for additional players that do not accumulate points in a given week ("Bench" players) as well as the ability to move 
players from the "Bench" to the active roster. Lastly, there should be a way to add or remove players from your roster if a 
player gets injured.
