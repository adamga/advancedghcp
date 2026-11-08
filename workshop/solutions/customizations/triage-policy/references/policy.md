# Fictional triage policy v1

Closed issues override every other rule: score 0, level P3, and the sole reason
`closed issue (0)`.

For active issues start with high=60, medium=30, low=10. Add 25 if blocked, 10
if affectedUsers >=100, and 5 if ageDays >=7. P1 is score >=80; P2 is score >=40;
otherwise P3. Under these input rules, 75 and 85 are the nearest reachable scores
around the P1 threshold; do not invent a fixture score of 80.

Return `{ level, score, reasons }`. Reason order and text:

1. `<impact> impact (+<base>)`
2. `blocked workflow (+25)` if blocked
3. `100+ affected users (+10)` if the users threshold applies
4. `7+ days old (+5)` if the age threshold applies

ISS-101: 60+25+10+5=100, P1, four reasons.
ISS-102: 30+25=55, P2, two reasons.
ISS-105: closed, 0/P3, only the closed reason even though blocked/high-impact.

Input is a valid issue from the documented schema. Return fresh objects/arrays;
do not mutate input. No clock, randomness, network, external services, or hidden
fixture imports. Unknown active impact values should fail explicitly.
