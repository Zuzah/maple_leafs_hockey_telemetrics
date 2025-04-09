Below field/records are available to you at start

```text
- x (location in feet down length of ice from centre; -100 to 100)

- y (location in feet across width of ice from centre; -42.5 to 42.5)
- 
z (location in feet above the ice surface)

- timestamp (UTC, 0.01-second precision)

- game_second (0.01-second precision)

- game_id

- period

- player_id (official NHL player ID; if null then the row represents the puck)

- player_position ("LW", "C", "RW", "LD", "RD", or "G")

- player_handedness ("L" or "R")

- team_id

- team_current_score

- opponent_current_score

- number_of_skaters_home

- number_of_skaters_away
```