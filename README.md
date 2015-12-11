# white-elephant
Python script that handles a White Elephant game.

```> python main.py```

Sample output:

```
Welcome to White Elephant! Please input names line by line. When you are finished inputting names, press enter on a blank line.

Participant name: Derek
Participant name: Emily
Participant name: Jeff
Participant name: 

Randomizing the order...

=======================
        TURN 1
=======================
Jeff is up first! What gift did they get?
The gift is a/an: new car
Cool! An amazing new car! What a gift!


=======================
        TURN 2
=======================
Now we're on to Derek. Are they stealing or picking a new gift?
Input 1 to steal or 2 to pick a new gift: 1
We're stealing! What does Derek want?
Gift 1: new car (Owner: Jeff, Steals: 0)
Gift to steal (a number): 1
Not sure what's going through the mind of Derek, no one wants that new car...Jeff lucked out there!


Welp, we're on to Jeff. Are they stealing or picking a new gift?
Actually, looks like there are no gifts left to steal! Moving on...
What gift did Jeff get?
The gift is a/an: cute dog
Cool! An amazing cute dog! What a gift!


=======================
        TURN 3
=======================
Now we're on to Emily. Are they stealing or picking a new gift?
Input 1 to steal or 2 to pick a new gift: 1
We're stealing! What does Emily want?
Gift 1: new car (Owner: Derek, Steals: 1)
Gift 2: cute dog (Owner: Jeff, Steals: 0)
Gift to steal (a number): 2
What is Emily thinking taking that cute dog? Jeff played them like a fiddle!


Welp, we're on to Jeff. Are they stealing or picking a new gift?
Input 1 to steal or 2 to pick a new gift: 2
What gift did Jeff get?
The gift is a/an: new guitar
Cool! An amazing new guitar! What a gift!


=======================
       LAST TURN
=======================
Back to Jeff, who has the option to force a swap!
Select the gift to swap for. If they're not swapping, input 0.
Gift 1: new car (Owner: Derek, Steals: 1)
Gift 2: cute dog (Owner: Emily, Steals: 1)
Gift to swap (a number): 0
No swap! What a pal.

That's a wrap! Here's what everyone ended up with:

Congratulations to Derek who ended up with the new car! Nice score!
Can you believe that Emily was able to snag the cute dog?!?
Would you look at that! Jeff has their very own new guitar!
```
