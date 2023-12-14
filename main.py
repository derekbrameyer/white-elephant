__author__ = 'derekbrameyer'

import random
import json
import datetime
from subprocess import call

def main():
    maxstealcount = 2
    currentturn = 1
    boolines = json.loads(open("boo_lines.json").read())
    reportlines = json.loads(open("report_lines.json").read())

    print(greenify("\nWelcome to White Elephant! Please input names line by line. When you are finished inputting names, press enter on a blank line.\n"))
    say("Welcome to White Elephant! Who's playing?", voice_samantha)
    fullname = "tester"
    participants = []
    gifts = []

    while fullname:
        fullname = input(greenify("Participant name: "))
        participants.append(Participant(fullname, None))
        if 0 < len(fullname):
            play(sound_sent_message)
        else:
            play(sound_logged_in)

    participants.pop()

    global should_save
    should_save = input(greenify("\nType 1 to also generate a document of the game: "))
    if should_save is '1':
        should_save = True
        global save_document
        filename = datetime.datetime.now().strftime("%Y%m%d") + "_" + datetime.datetime.now().strftime("%H%M") + "_white_elephant.txt"
        print(filename)
        save_document = open(filename, "w")

    print("\nRandomizing the order...\n")
    say("Randomizing the order... Excuse me, I meant to say, reticulating splines!", voice_samantha)

    random.shuffle(participants)
    participants.reverse()
    say(" ", voice_samantha)
    play(sound_glass)

    say("Take it away, Alex.", voice_samantha)

    firstparticipant = participants.pop()

    print_and_save("=======================", True)
    print_and_save("        TURN 1", True, voice_alex)
    print_and_save("=======================", True)
    print_and_save(firstparticipant.fullname + " is up first! What gift did they get?", False)
    say(firstparticipant.fullname + " is up first! Pick any gift.", voice_alex)

    giftname = input(greenify("The gift is a/an: "))
    save_to_file("The gift is a/an: " + giftname)
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
            print_and_save("\n\nWelp, we're on to " + nextparticipant.fullname + ". Are they stealing or picking a new gift?", False)
            say("Welp, we're on to " + nextparticipant.fullname + ". You can steal or pick a new gift.", voice_alex)
        else:
            print_and_save("Cool! An amazing " + gift.name + "! What a gift!\n\n", False, voice_alex)
            print_and_save("=======================", True)
            print_and_save("        TURN " + str(currentturn), True, voice_alex)
            print_and_save("=======================", True)
            print_and_save("Now we're on to " + nextparticipant.fullname + ". Are they stealing or picking a new gift?", False)
            say("Now we're on to " + nextparticipant.fullname + ". You can steal or pick a new gift.", voice_alex)

        if len(giftsinturn) > 0:
            action = input(greenify("Input 1 to steal or 2 to pick a new gift: "))
            save_to_file("Input 1 to steal or 2 to pick a new gift: " + action)
        else:
            play(sound_basso)
            print_and_save("Actually, looks like there are no gifts left to steal! Moving on...", False, voice_alex)
            action = "0"

        if action == "1":
            print_and_save("We're stealing! What does " + nextparticipant.fullname + " want?\n", False)
            play(sound_sosumi)
            say("We're stealing!", voice_alex)
            displayCount = 1
            for gift in giftsinturn:
                print_and_save("Gift " + str(displayCount) + ": " + gift.name + " (Owner: " + gift.owner.fullname + ", Steals: " + str(gift.steals) + ")", False)
                displayCount += 1
            giftstealcount = maxstealcount + 1
            while giftstealcount >= maxstealcount:
                giftselection = input(greenify("\nGift to steal (a number): "))
                save_to_file("\nGift to steal (a number): " + giftselection)
                stolengift = giftsinturn[int(giftselection) - 1]
                giftstealcount = stolengift.steals
                if giftstealcount >= maxstealcount:
                    play(sound_basso)
                    print_and_save("I can't let you do that, " + nextparticipant.fullname + "! You'll have to select another gift.", False, voice_fred)

            giftsinturn.remove(stolengift)
            newowner = nextparticipant
            nextparticipant = stolengift.owner
            nextparticipant.gift = None
            stolengift.owner = newowner
            newowner.gift = stolengift
            stolengift.steals += 1

            random.shuffle(boolines)
            print_and_save(boolines[0] % (newowner.fullname, stolengift.name, nextparticipant.fullname), False, voice_samantha)

            # TODO If gift has max steals, print something
            if stolengift.steals >= maxstealcount:
                print_and_save("Congrats to " + stolengift.owner.fullname + " for being the true owner of a shiny new " + stolengift.name + "!", False, voice_alex)
            
            play(sound_file_transfer_complete)

            previous_action = 0
        else:
            print_and_save("What gift did " + nextparticipant.fullname + " get?", False)
            giftname = input(greenify("The gift is a/an: "))
            save_to_file("The gift is a/an: " + giftname)
            gift = Gift(giftname, 0, nextparticipant)
            nextparticipant.gift = gift
            gifts.append(gift)
            previous_action = 1
            nextparticipant = None

    # wrap up with the first participant optionally stealing again
    if previous_action == 0:
        print_and_save("\n\n", False)
        print_and_save("=======================", True)
        print_and_save("       LAST TURN", True, voice_alex)
        print_and_save("=======================", True)
        print_and_save("Welp, we're almost done. Back to " + firstparticipant.fullname + ", who has the option to force a swap!", False, voice_alex)
    else:
        print_and_save("Cool! An amazing " + gift.name + "! What a gift!\n\n", False, voice_alex)
        print_and_save("=======================", True)
        print_and_save("       LAST TURN", True, voice_alex)
        print_and_save("=======================", True)
        print_and_save("Back to " + firstparticipant.fullname + ", who has the option to force a swap!", False, voice_alex)

    print_and_save("Select the gift to swap for. If they're not swapping, input 0.\n", False)
    displayCount = 1
    owner_pivot_idx = 0
    for gift in gifts:
        # don't display the owner's gift
        if gift.owner.fullname is firstparticipant.fullname:
            owner_pivot_idx = displayCount - 1
            continue
        print_and_save("Gift " + str(displayCount) + ": " + gift.name + " (Owner: " + gift.owner.fullname + ", Steals: " + str(gift.steals) + ")", False)
        displayCount += 1

    giftstealcount = maxstealcount + 1
    while giftstealcount >= maxstealcount:
        giftselection = input(greenify("\nGift to swap (a number): "))
        save_to_file("\nGift to swap (a number): " + giftselection)
        if giftselection == "0":
            print_and_save("No swap! What a pal.", False, voice_alex)
            break
        if giftselection > owner_pivot_idx:
            giftselection = str(int(giftselection) + 1)
        gifttoswap = gifts[int(giftselection) - 1]
        giftstealcount = gifttoswap.steals
        if giftstealcount >= maxstealcount:
            play(sound_basso)
            print_and_save("I can't let you do that, " + nextparticipant.fullname + "! You'll have to select another gift.", False, voice_fred)

    if giftselection != "0":
        oldowner = gifttoswap.owner
        swappedgift = firstparticipant.gift

        swappedgift.owner = oldowner
        oldowner.gift = swappedgift

        gifttoswap.owner = firstparticipant
        firstparticipant.gift = gifttoswap

    play(sound_glass)
    print_and_save("\nThat's a wrap! Here's what everyone ended up with:\n", False, voice_samantha)

    for gift in gifts:
        random.shuffle(reportlines)
        print_and_save(reportlines[0] % (gift.owner.fullname, gift.name), False, voice_samantha)

    print_and_save("\n\n", False)

    say("Thanks for playing! Now enjoy the rest of Happy Hour. The forecast calls for ugly sweaters.", voice_samantha)

    if should_save is '1':
        save_file.close()

def greenify(string):
    attr = []
    attr.append('32')
    return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), string)

def print_and_save(string, should_greenify, voice = None):
    if should_greenify:
        print(greenify(string))
    else:
        print(string)
    save_to_file(string)
    if voice != None:
        say(string, voice)

def save_to_file(string):
    global should_save
    if should_save:
        global save_document
        save_document.write(string)
        save_document.write("\n")

class Participant(object):
    def __init__(self, name, gift):
        self.fullname = name
        self.gift = gift

class Gift(object):
    def __init__(self, name, steals, owner):
        self.name = name
        self.steals = steals
        self.owner = owner

should_save = False
save_document = None

should_play_sounds = True

voice_samantha = "Samantha"
voice_fred = "Fred"
voice_alex = "Alex"

def say(message, voice):
    if should_play_sounds:
        call(["say", message, "-v", voice])

sound_glass = "/System/Library/Sounds/Glass.aiff"
sound_hero = "/System/Library/Sounds/Hero.aiff"
sound_basso = "/System/Library/Sounds/Basso.aiff"
sound_sosumi = "/System/Library/Sounds/Sosumi.aiff"
sound_sent_message = "/Applications/Messages.app/Contents/Resources/Sent Message.aiff"
sound_logged_in = "/Applications/Messages.app/Contents/Resources/Logged In.aiff"
sound_file_transfer_complete = "/Applications/Messages.app/Contents/Resources/File Transfer Complete.aiff"

def play(sound):
    if should_play_sounds:
        call(["afplay", sound])

if __name__ == "__main__":
    main()