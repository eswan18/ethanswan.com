---
title: "No One Can Master Survivor"
subtitle: "A broken game, sadly"
date: 2025-04-09
slug: cant-master-survivor
tags:
- survivor
summary: "Survivor is one of my favorite shows.... But my view is that the game is basically broken."
---

Survivor is one of my favorite shows.
I don't care about the outdoors aspect[^outdoors] and am basically apathetic regarding most of the challenges.
What hooked me about the game is the strategy.

## A quick explanation

The basic structure of Survivor isn't complicated.
Twenty or so people are cast as contestants, and then split into two or three "tribes".
These tribes live separately from each other, and periodically meet up to participate in a "challenge".
The losing tribe or tribes must then vote out one of its members, after returning to camp to allow for some strategizing first.
Votes are cast in secret.

At some point in the show, the producers decide to "merge" the tribes into one.
From this point onward, challenges continue, but the reward is different: the *one* person who wins the challenge is given "immunity".
Then the tribe votes out one of its members (as in the pre-merge part of the game), but for that voting session, the immune contestant cannot be voted for.

Once there are only two or three contestants remaining (it depends on the season), things flip:
now, the people who were recently voted out -- the "jury" -- get to cast their own votes for a winner among the remaining contestants.
There is, probably intentionally, no criteria explained on the show for this vote.
Jury members simply choose who they want to crown as the winner.

## Caveats

I've omitted basically all the strategy.
A whole gamut of conventional wisdom has evolved over the life of the game, covering the obvious (Keep good competitors in your tribe pre-merge, so you can win challenges and avoid voting out members) to the very meta (the "meat shield"[^meat-shield]).

Additionally, I'm intentionally ignoring motivations beyond strategy.
Loyalty and friendship play a real role in decisions, even though juries don't always value honesty and honor above stratetic play (and most audience members probably prefer this).
And interpersonal drama, particularly in the case of players who cause problems for the tribe, can lead players to vote someone out for reasons other than their strategic importance.

## Optimizing

Using a simple outline of the game makes the optimal strategy clearer.
In order to model this, we need to have an estimate of the credibility each player has with the jury.
We'll call this their "winnability"[^winnability].

Now let's work backwards from the end of the game.

If three players have made it to the end and are sitting before the jury, whichever has the highest winnability is definitionally most likely to win the game.

```
A: 50
B: 33
C: 78
```

In this example, C accumulates enough jury votes to win, the plurality of the time.

So what happens when there are four players?

```
A: 50
B: 33
C: 78
D: 41
```

Assuming players are able to judge the winnability of their rivals, A, B, and D should band together and vote out C.
For all of them, C was the most likely person to beat them in the next stage of the game.
It doesn't matter who C would vote for, since everyone else should target them regardless.

And at five players...

```
A: 50
B: 33
C: 78
D: 41
E: 87
```

Everyone should agree that E needs to go.

And so on.

Thus, if the final vote involves three people, the best positioned player is the one with the third-lowest winnability -- no matter how many people are in the tribe in total.
This is always true when everyone is in a single tribe, which happens at the merge.

## Pre-merge

The previous logic applies as long as all players are in a single tribe, which is true starting at the merge (roughly the halfway point of the season).

Strategy before the merge isn't so simple, since you need to make it to the merge, and it's easier to do that if your tribe isn't losing challenges and voting out members.
That means you should be taking into account who can help you in challenges, not just who will beat you in the end -- though you should consider both.

## The sad conclusion

Players don't play the game exactly according to this strategy, and the presence of immunities in the post-merge period can allow highly winnable players to make it further than they otherwise should.

But still, a well-played game of Survivor almost always leads to some of the least-winnable players sitting in front of the jury at the end.
Even if the jury selects the best option, the winner will very rarely be better than the median player from the season.

This is why, as Survivor goes on longer and contestants understand the game better, the notion of a "good player" breaks down.
What is a good player if not one who wins a season?
And yet, anyone considered "good" will be eliminated well before the end of the game.

This makes winners out of less-than-impressive players and makes repeating as a winner almost impossible.
The first repeat winner[^spoilers] required a very unusual circumstance: she was in the final three with another former winner and with an exceptionally unlikable contestant.
It was also much earlier in the history of the game, and other players were less laser-focused on targeting winnable players.

## Can you fix it?

One aspect of Survivor that helps mitigate this problem is contestants' ability to plead their own case in front of the jury.
Players sometimes ask for recognition of actions they took that ran counter to this strategy (of always eliminating the biggest threat).
Maybe they displayed exceptional loyalty to a friend, or they took a strong player along in order to demonstrate their own personal superiority to that player.
And because there's no real criteria for jury votes, sometimes this works.

I haven't seen even half the seasons, but my experience is that this has become less of a factor as the game has gone on.
Serious players on the jury respect serious, competitive play -- and that means ruthlessly optimizing your chance to win through eliminating threats.
So while this helps a little, it's not enough to really change the paradigm.

I think the only real fix is reward "good" play more consistently.
When only one player can earn a personal immunity for each vote, it's just improbable that many good players will survive multiple rounds.
A mechanism like adding one artificial vote against the last place finishers in each challenge would be interesting.
Giving immunity to multiple people in each round of voting could help, and indeed this sometimes happens through "hidden immunity idols" which players can find semi-randomly.

But my view is that the game is basically broken, which is really disappointing.
It's a game in which contestants can choose whom to compete with, and a motivated competitor will naturally remove the most skilled opponents.
The idea is fascinating, but the more strategic the players, the less fun the game is as a fan.

[^outdoors]: It'll be no surprise if you know me, but I find the outdoors skills utterly uninteresting and wish the show would do away with them entirely.
[^meat-shield]: The meat shield is a few levels deep. Firstly, as the game approaches its end, players become more focused on voting out "threats": other competitors who would win more jury votes than them. But to counter this, some threatening players will drag along *another* (ideally even more) threatening player, to attract the attention of others near the end game. This is a sort of human shield -- a distraction that keeps the first player safe when otherwise they'd be a target.
[^winnability]: And I'm not treating this number as purely deterministic, such that a player with a higher winnability wins every time. That would be an oversimplification. Only that they will win *most* of the time. So the gap in winnability between players translates to a gap in the chance of accumulating enough votes.
[^spoilers]: No spoilers. You can google this easily if you're interested. I'll just say that this winner benefitted from seeming quite incompetent socially and physically during the season, illustrating the very point that "good" players don't win.