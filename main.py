__author__ = 'derekbrameyer'

import random
import json

def main():
    maxstealcount = 2
    currentturn=1
    boolines = json.loads(open("boo_lines.json").read())
    reportlines = json.loads(open("report_lines.json").read())

    print "\nWelcome to White Elephant! Please input names line by line. When you are finished inputting names, press enter on a blank line.\n"
    fullname = "tester"
    participants = []
    gifts = []

    while fullname:
        fullname = raw_input("Participant name: ")
        participants.append(Participant(fullname, None))

    participants.pop()

    print "\nRandomizing the order...\n"

    random.shuffle(participants)
    participants.reverse()

    firstparticipant = participants.pop()

    print "======================="
    print "        TURN 1"
    print "======================="
    print firstparticipant.fullname + " is up first! What gift did they get?"

    giftname = raw_input("The gift is a/an: ")
    gift = Gift(giftname, 0, firstparticipant)
    firstparticipant.gift = gift
    gifts.append(gift)

    # 0 = steal
    # 1 = pick new gift
    previous_action = 1

    while len(participants) > 0 or nextparticipant is not None:
        # only iterate through the list if it was a random gift last time
        if previous_action == 1:
            nextparticipant = participants.pop()
            currentturn += 1
            giftsinturn = list(gifts)

        if previous_action == 0:
            print "\n\nWelp, we're on to " + nextparticipant.fullname + ". Are they stealing or picking a new gift?"
        else:
            print "Cool! An amazing " + gift.name + "! What a gift!\n\n"
            print "======================="
            print "        TURN " + str(currentturn)
            print "======================="
            print "Now we're on to " + nextparticipant.fullname + ". Are they stealing or picking a new gift?"

        if len(giftsinturn) > 0:
            action = raw_input("Input 1 to steal or 2 to pick a new gift: ")
        else:
            print "Actually, looks like there are no gifts left to steal! Moving on..."
            action = "0"

        if action == "1":
            print "We're stealing! What does " + nextparticipant.fullname + " want?"
            displayCount = 1
            for gift in giftsinturn:
                print "Gift " + str(displayCount) + ": " + gift.name + " (Owner: " + gift.owner.fullname + ", Steals: " + str(gift.steals) + ")"
                displayCount += 1
            giftstealcount = maxstealcount + 1
            while giftstealcount >= maxstealcount:
                giftselection = raw_input("Gift to steal (a number): ")
                stolengift = giftsinturn[int(giftselection) - 1]
                giftstealcount = stolengift.steals
                if giftstealcount >= maxstealcount:
                    print "I can't let you do that Star Fox! You'll have to select another gift."

            giftsinturn.remove(stolengift)
            newowner = nextparticipant
            nextparticipant = stolengift.owner
            nextparticipant.gift = None
            stolengift.owner = newowner
            newowner.gift = stolengift
            stolengift.steals += 1

            random.shuffle(boolines)
            print boolines[0] % (newowner.fullname, stolengift.name, nextparticipant.fullname)

            # TODO If gift has max steals, print something
            if stolengift.steals >= maxstealcount:
                print "Congrats to " + stolengift.owner.fullname + " for being the true owner of a shiny new " + stolengift.name + "!"

            previous_action = 0
        else:
            print "What gift did " + nextparticipant.fullname + " get?"
            giftname = raw_input("The gift is a/an: ")
            gift = Gift(giftname, 0, nextparticipant)
            nextparticipant.gift = gift
            gifts.append(gift)
            previous_action = 1
            nextparticipant = None

    # wrap up with the first participant optionally stealing again
    if previous_action == 0:
        print "\n\n"
        print "======================="
        print "       LAST TURN"
        print "======================="
        print "Welp, we're almost done. Back to " + firstparticipant.fullname + ", who has the option to force a swap!"
    else:
        print "Cool! An amazing " + gift.name + "! What a gift!\n\n"
        print "======================="
        print "       LAST TURN"
        print "======================="
        print "Back to " + firstparticipant.fullname + ", who has the option to force a swap!"

    print "Select the gift to swap for. If they're not swapping, input 0."
    displayCount = 1
    for gift in gifts:
        # don't display the owner's gift
        if gift.owner.fullname is firstparticipant.fullname:
            continue
        print "Gift " + str(displayCount) + ": " + gift.name + " (Owner: " + gift.owner.fullname + ", Steals: " + str(gift.steals) + ")"
        displayCount += 1

    giftstealcount = maxstealcount + 1
    while giftstealcount >= maxstealcount:
        giftselection = raw_input("Gift to swap (a number): ")
        if giftselection == "0":
            print "No swap! What a pal."
            break
        gifttoswap = gifts[int(giftselection) - 1]
        giftstealcount = gifttoswap.steals
        if giftstealcount >= maxstealcount:
            print "I can't let you do that Star Fox! You'll have to select another gift."

    if giftselection != "0":
        oldowner = gifttoswap.owner
        swappedgift = firstparticipant.gift

        swappedgift.owner = oldowner
        oldowner.gift = swappedgift

        gifttoswap.owner = firstparticipant
        firstparticipant.gift = gifttoswap

    print "\nThat's a wrap! Here's what everyone ended up with:\n"

    for gift in gifts:
        random.shuffle(reportlines)
        print reportlines[0] % (gift.owner.fullname, gift.name)
        # print gift.owner.fullname + " got an amazing " + gift.name + "!"




class Participant(object):
    def __init__(self, name, gift):
        self.fullname = name
        self.gift = gift

class Gift(object):
    def __init__(self, name, steals, owner):
        self.name = name
        self.steals = steals
        self.owner = owner

if __name__ == "__main__":
    main()