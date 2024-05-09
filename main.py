from resources import *
import winsound
import time

# Initialize game state variables
screen = "newGame"
hotkey = "space"
ending = "none"

# Score management
localhighscore = 0
undrawScore = Text(Point(100, 100), "hi")
tempScore = 0

# Main game loop
while screen == "newGame":
    if ending == "win":  # classic mode win screen
        winScreen = GraphWin("WINNER WINNER CHICKEN DINNER", 500, 500)
        youWin = Image(Point(250, 250), "resources/youWin.gif")
        youWin.draw(winScreen)
        time.sleep(3)
        winScreen.close()
        screen = "title"

    elif ending == "lose":  # classic mode lose screen
        loseScreen = GraphWin("Wow so sad you lost", 500, 500)
        gameOver = Image(Point(250, 250), "resources/gameOver.gif")
        gameOver.draw(loseScreen)       

        coverWatermark = Rectangle(Point(175, 455), Point(355, 480))
        coverWatermark.setFill("black")
        coverWatermark.draw(loseScreen)

        while screen == "newGame":  # option for user to quit or start new game
            click = loseScreen.getMouse()
            if 217 >= click.getX() >= 154 and 410 >= click.getY() >= 380:
                loseScreen.close()
                screen = "title"
            elif 346 >= click.getX() >= 296 and 410 >= click.getY() >= 380:
                quit()      

    elif ending == "finalscore":  # when user finally loses in endless mode
        winScreen = GraphWin("End Screen", 500, 500)
        highscoreBackground = Image(Point(250, 250), "resources/highscoreBackground.gif")
        highscoreBackground.draw(winScreen)
        finalText = Image(Point(250, 50), "resources/finalText.gif")
        finalText.draw(winScreen)

        displayNumber = Text(Point(250, 130), str(tempScore))
        displayNumber.setSize(35)
        displayNumber.setFill("Green")
        displayNumber.draw(winScreen)

        newGameText = Image(Point(250, 220), "resources/newGameText.gif")
        newGameText.draw(winScreen)

        exitGameText = Image(Point(250, 270), "resources/exitGameText.gif")
        exitGameText.draw(winScreen)

        while screen == "newGame":  # option for quitting or starting new game
            click = winScreen.getMouse()
            if 338 >= click.getX() >= 163 and 241 >= click.getY() >= 200:
                winScreen.close()
                screen = "title"
            elif 345 >= click.getX() >= 155 and 291 >= click.getY() >= 250:
                quit()

    titleScreen = GraphWin("Stacker", 600, 600, autoflush=False)
    titleBackground = Image(Point(300, 300), "resources/titleBackground.gif")
    titleBackground.draw(titleScreen)
    stackerTitle = Image(Point(300, 75), "resources/stackerTitle.gif")
    stackerTitle.draw(titleScreen)

    classic = Image(Point(300, 230), "resources/classic.gif")
    classic.draw(titleScreen)

    endless = Image(Point(300, 285), "resources/endless.gif")
    endless.draw(titleScreen)

    hotkeyTitle = Image(Point(300, 400), "resources/hotkeyTitle.gif")
    hotkeyTitle.draw(titleScreen)

    rules = Image(Point(300, 447), "resources/rules.gif")
    rules.draw(titleScreen)

    leaveText = Text(Point(550, 550), "/Quit")
    leaveText.setSize(20)
    leaveText.setTextColor("light grey")
    leaveText.draw(titleScreen)

    aboutText = Text(Point(50, 550), "About")
    aboutText.setSize(20)
    aboutText.setTextColor("light grey")
    aboutText.draw(titleScreen)

    resetScore = Text(Point(410, 550), "Reset score")
    resetScore.setSize(13)
    resetScore.setTextColor("light grey")
    resetScore.draw(titleScreen)

    screen = "title"

    highscoreimg = Image(Point(300, 525), "resources/highscore.gif")
    highscoreimg.draw(titleScreen)

    #  ^^^^ all visuals for the menu

    while screen == "title":
        
        undrawScore.undraw()

        with open("resources/highscore.txt",
                  "r") as highscorefile:  # context manager "highscorefile" is the var that stores the .txt
            contents = highscorefile.readline()
            # looks at local highscore and saves it in a variable

        highscoreText = Text(Point(300, 561), contents)
        undrawScore = highscoreText
        highscoreText.setSize(20)
        highscoreText.setFill("red")
        highscoreText.draw(titleScreen)
        localhighscore = int(contents)

        update()

        click = titleScreen.getMouse()

        # images used consistently
        sizes = [114, 76, 38]
        blocks = [
            "resources/3block.gif",
            "resources/2block.gif",
            "resources/1block.gif",
        ]

        buttons = [
            "resources/add1.gif",
            "resources/slowspeed.gif",
            "resources/scoremultiply.gif"
        ]

        blackbuttons = [
            "resources/add1black.gif",
            "resources/slowspeedblack.gif",
            "resources/scoremultiplyblack.gif"
        ]

        # algorithm variables
        level = 0
        n = 0
        block = blocks[n]
        starter = "left"
        position = 0
        size = sizes[n]
        placing = True
        stacking = True
        end = False
        direction = 1
        prevPosition = 0
        endless = False
        height = 0
        force = "none"
        powerupping = False
        temp = []
        score = 0
        count = 0
        multiplier = False
        slowed = 1
        block_counter = 0
        addBlock = False

        if 450 >= click.getX() >= 150 and 300 >= click.getY() >= 270:  # if user wants to endless
            endless = True
            click = Point(385, 240)

        if 450 >= click.getX() >= 150 and 245 >= click.getY() >= 215:  # if user clicks on classic
            titleScreen.close()
            if endless:  # gameScreen will be bigger if endless mode is chosen
                gameScreen = GraphWin("Stacker", 1200, 900, autoflush=False)
                endlessBackground = Image(Point(600, 450), "resources/endlessBackground.gif")
                endlessBackground.draw(gameScreen)
            else:  # gameScreen will be smaller if classic mode is chosen
                gameScreen = GraphWin("Stacker", 900, 900, autoflush=False)
                classicBackground = Image(Point(450, 450), "resources/classicBackground.gif")
                classicBackground.draw(gameScreen)

            winsound.PlaySound("gameMusic", winsound.SND_ASYNC | winsound.SND_LOOP)

            if not endless:  # visuals to tell you what mode you chose
                modeText = Text(Point(450, 40), "Classic Mode")
                modeText.setSize(35)
            else:
                modeText = Text(Point(950, 50), "ENDLESS MODE")
                modeText.setSize(30)
                square = Rectangle(Point(800, 150), Point(1100, 670))
                square.draw(gameScreen)
                square.setFill("white")

                for x in range(3):
                    grey_image = Image(Point(950, 200 + x * 200), blackbuttons[x])
                    grey_image.draw(gameScreen)
                    temp.append(grey_image)

                # more visuals
                addText = Text(Point(950, 260), "Press 1: Add One Block")
                addText.draw(gameScreen)
                addTextBottom = Text(Point(950, 275), "* Only for 1 and 2 blocks to increase chance of stacking *")
                addTextBottom.draw(gameScreen)
                addTextBottom.setSize(8)

                slowText = Text(Point(950, 450), "Press 2: Slow Down For One Level")
                slowText.draw(gameScreen)
                multiplierText = Text(Point(950, 650), "Press 3: Double Score for 5 Levels")
                multiplierText.draw(gameScreen)

                george = Text(Point(950, 130), "*** Power ups only work when lit up ***")
                george.setSize(15)
                george.draw(gameScreen)

            modeText.draw(gameScreen)

            scoreText = Text(Point(450, 50), "Score: " + str(score))

            base = Line(Point(184, 832), Point(716, 832))
            base.setWidth(5)
            border2 = Line(Point(181, 70), Point(181, 835))
            border3 = Line(Point(718, 70), Point(718, 835))

            base.draw(gameScreen)
            border2.draw(gameScreen)
            border2.setWidth(5)
            border3.draw(gameScreen)
            border3.setWidth(5)

            update()

            drawnblocks = []

            while stacking:
                # Power up becomes available once 5 blocks have been placed
                if block_counter == 5:
                    powerupping = True
                    block_counter = 0

                if not endless:
                    if level == 4 and n == 0:
                        n = 1
                        force = "force2"
                        block = blocks[n]
                        size = sizes[n]
                    elif level == 7 and n == 1:
                        n = 2
                        force = "force1"
                        block = blocks[n]
                        size = sizes[n]

                if starter == "left":
                    position = 184 + size
                    direction = 1
                elif starter == "right":
                    position = 184 + 532 - size
                    direction = -1

                # condition to "light up" the buttons
                if endless:
                    if powerupping:
                        for x in range(len(temp)):
                            if x == 0:
                                if n == 0:
                                    continue
                            temp[x].undraw()

                        for x in range(3):
                            if x == 0:
                                if n == 0:
                                    temp = temp[:1]
                                    continue
                                else:
                                    temp = []
                            grey_image = Image(Point(950, 200 + x * 200), buttons[x])
                            grey_image.draw(gameScreen)
                            temp.append(grey_image)

                # this block right here is the block that is first drawn either
                # in the right side or the left side
                drawnblock = Image(Point(position, 792 - height * 76), block)
                drawnblock.draw(gameScreen)
                placing = True

                # this updates the score
                if endless:
                    scoreText.undraw()
                    scoreText = Text(Point(450, 50), "Score: " + str(score))
                    scoreText.draw(gameScreen)
                    scoreText.setSize(25)
                    update()

                # this changes the speed back to normal, as the power up only slows down for 1 level
                if slowed == 2:
                    slowed = 1

                while placing:
                    draw = True
                    classicEnd = time.time() + (0.75 - 0.075 * level)
                    endlessEnd = time.time() + ((0.75 - 0.01 * level) * slowed)
                    timeEnd = 0

                    # these 2 if and else statements differentiates the time restraints to place
                    # a block depending if you are doing classic mode or endless mode
                    # classic mode is faster, endless mode is slower
                    if endless:
                        timeEnd = endlessEnd
                    else:
                        timeEnd = classicEnd

                    # while the current time is equal to the current time + whatever the speed is set to
                    while time.time() < timeEnd:  # time for input

                        # algorithm to check keys you pressed
                        key = gameScreen.checkKey()
                        if key == hotkey:

                            # if you placed a block, all the code under this will run
                            # set placing to false and drawing to false because we don't
                            # want it to move when it is already placed
                            placing = False
                            draw = False

                            # - - - Hit Reg - - - -
                            # Each individual block is 76 x 76
                            # I knew how much to add the previousPosition variables by because when I drew the
                            # block stacking occurrences myself I also noted the centre points of each image.
                            # Sometimes because the centre point of a two block is involved, I have to add / subtract
                            # prevPositions by 38 or 114 (38 + 76) instead of 76 or 152

                            if level == 0:
                                prevPosition = position
                            #     will be previous position when they get to level 2 (when level = 1)
                            elif not endless:
                                # user can only "win" if they are in classic mode
                                if level == 9 and prevPosition == position and n == 2:
                                    # print("WINNER WINNER CHICKEN DINNER")
                                    end = True
                                    ending = "win"

                            # - - - - - - - - - - - - - Hit Reg Added Block Power Up - - - - - - - - - - - - - - - - -

                            if endless and addBlock is True:
                                if n == 0:
                                    # if the block after being added is a three block
                                    if (position + 38 == prevPosition) or (position - 38 == prevPosition):
                                        # if the three block "fully stacks" on the two block
                                        n = 1
                                        block = blocks[n]
                                        size = sizes[n]
                                        drawnblock.undraw()
                                        drawnblock = Image(Point(prevPosition, 792 - height * 76), block)
                                        drawnblock.draw(gameScreen)
                                    elif (position + 114 == prevPosition) or (position - 114 == prevPosition):
                                        # if the three block only got one block aligned on the two block
                                        n = 2
                                        block = blocks[n]
                                        size = sizes[n]
                                        if position < prevPosition:
                                            prevPosition = prevPosition - 38
                                        else:
                                            prevPosition = prevPosition + 38
                                        drawnblock.undraw()
                                        drawnblock = Image(Point(prevPosition, 792 - height * 76), block)
                                        drawnblock.draw(gameScreen)
                                    else:
                                        # anything else means the block is completely off
                                        end = True
                                        ending = "lose"
                                else:
                                    # if the block becomes a two block after power up
                                    if (position + 38 == prevPosition) or (position - 38 == prevPosition):
                                        n = 2
                                        block = blocks[n]
                                        size = sizes[n]
                                        drawnblock.undraw()
                                        drawnblock = Image(Point(prevPosition, 792 - height * 76), block)
                                        drawnblock.draw(gameScreen)
                                    else:
                                        end = True
                                        ending = "lose"

                            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

                            if force == "force2":
                                # if the user got forced down to 2 blocks
                                # When 2block is completely on top the previous 3 block
                                if prevPosition + 38 == position:
                                    prevPosition = position
                                elif prevPosition - 38 == position:
                                    prevPosition = position
                                # When 2block is only partially on top the previous 3 block
                                elif prevPosition + 114 == position:
                                    prevPosition = position - 38
                                    n = 2
                                    block = blocks[2]
                                    size = sizes[n]
                                    drawnblock.undraw()
                                    drawnblock = Image(Point(prevPosition, 792 - height * 76), block)
                                    drawnblock.draw(gameScreen)
                                elif prevPosition - 114 == position:
                                    prevPosition = position + 38
                                    n = 2
                                    block = blocks[2]
                                    size = sizes[n]
                                    drawnblock.undraw()
                                    drawnblock = Image(Point(prevPosition, 792 - height * 76), block)
                                    drawnblock.draw(gameScreen)
                                else:
                                    # anything else means the 2 block is completely off
                                    end = True
                                    ending = "lose"
                            elif force == "force1":
                                # if the user got forced down to one block
                                # if the one block is completely on top of the previous 2 block
                                if prevPosition + 38 == position:
                                    prevPosition = position
                                elif prevPosition - 38 == position:
                                    prevPosition = position
                                else:
                                    # anything else means they missed the whole stack
                                    end = True
                                    # print("GAME OVER, You lose")
                                    ending = "lose"

                            if (prevPosition - position >= size * 2 or position - prevPosition >= size * 2) and (addBlock is False) and (force == "none"):
                                # when the stacked block is completely misaligned; only time we use the "size" variable
                                # for hit reg
                                end = True
                                # print("GAME OVER, You lose")
                                ending = "lose"
                                if endless:
                                    ending = "finalscore"

                            elif (position != prevPosition) and (force == "none") and (addBlock is False):
                                # when the block is not completely aligned with the previous block
                                # I put the other two ands so that the program won't go through this chunk of code
                                # by accident and mess up everything
                                if (n == 0 or n == 1) and (position + 76 == prevPosition or position - 76 == prevPosition):
                                    # if a three block or two block misalign one block
                                    n = n + 1
                                    block = blocks[n]
                                    size = sizes[n]
                                    drawnblock.undraw()
                                    if prevPosition > position:
                                        prevPosition = position + 38
                                        drawnblock = Image(Point(prevPosition, 792 - height * 76), block)
                                        drawnblock.draw(gameScreen)

                                    elif prevPosition < position:
                                        prevPosition = position - 38
                                        drawnblock = Image(Point(prevPosition, 792 - height * 76), block)
                                        drawnblock.draw(gameScreen)

                                elif n == 0 and position + 152 == prevPosition or position - 152 == prevPosition:
                                    # If the block is a three block and 2 blocks get misaligned
                                    n = 2
                                    block = blocks[n]
                                    size = sizes[n]
                                    drawnblock.undraw()

                                    if prevPosition > position:
                                        prevPosition = position + 76
                                        drawnblock = Image(Point(prevPosition, 792 - height * 76), block)
                                        drawnblock.draw(gameScreen)

                                    elif prevPosition < position:
                                        prevPosition = position - 76
                                        drawnblock = Image(Point(prevPosition, 792 - height * 76), block)
                                        drawnblock.draw(gameScreen)

                            # - - - - - - - - - - -

                            addBlock = False
                            force = "none"
                            # Update the addblock and force variables back to false and "none"

                            if end:
                                winsound.PlaySound(None, winsound.SND_PURGE)
                                stacking = False
                                placing = False
                                draw = False

                                # plays either winning or losing sound depending on outcome
                                if ending == "lose" or ending == "finalscore":
                                    winsound.PlaySound("losingSoundEffect", winsound.SND_ASYNC)
                                elif ending == "win":
                                    winsound.PlaySound("winningSoundEffect", winsound.SND_ASYNC)

                                # Makes the block flicker 3 times

                                for z in range(3):
                                    drawnblock.undraw()
                                    update()
                                    time.sleep(0.5)
                                    drawnblock = Image(Point(position, 792 - (height * 76)), block)
                                    drawnblock.draw(gameScreen)
                                    update()
                                    time.sleep(0.5)
                                screen = "newGame"

                                # checks if your endless score beat the local score and saves it
                                if endless:
                                    with open("resources/highscore.txt", "w") as highscorefile:
                                        if score > localhighscore:
                                            highscorefile.write(str(score))
                                            newHighscore = True
                                        else:
                                            highscorefile.write(str(localhighscore))

                                gameScreen.close()
                                tempScore = score
                                break

                            drawnblocks.append(drawnblock)
                            # print(drawnblocks)
                            # print("Previous Position:", prevPosition, "New Position:", position)

                            # changes the start position to the opposite side for the next block and level
                            if starter == "left":
                                starter = "right"
                            else:
                                starter = "left"

                            score += 1
                            level += 1
                            height += 1
                            if not powerupping:
                                block_counter += 1

                            # a power up that multiplies your score for the next 5 blocks by 2 when placed
                            if multiplier:
                                if not count == 5:
                                    score += 1  # adds more 1 more score, 1 + 1 = 2 for next 5 blocks
                                    count += 1
                                else:
                                    count = 0
                                    multiplier = False

                            # print("level = " + str(level))  # test code

                            # checks if the block placed was at the very top, then it clears the grid and keeps the
                            # recently placed block at the bottom
                            if (level == 10 or (level - 10) % 9 == 0 and not level == 1) and endless:
                                # if it hits the top block
                                for i in drawnblocks:
                                    i.undraw()
                                height = 1
                                prevBlock = Image(Point(prevPosition, 792), block)
                                prevBlock.draw(gameScreen)
                                drawnblocks = [prevBlock]
                                # print("went thru")

                        # checks if the keys are any hotkeys for power ups
                        elif endless:
                            if powerupping:
                                if key == "":
                                    continue
                                elif key == "1":  # adds 1 block
                                    # if you still have a 3 block, then this will not do anything
                                    if n == 0:
                                        continue

                                    # adds 1 block to your current block
                                    else:
                                        if (position - 184) > (716 - position):
                                            position = position - 38
                                        else:
                                            position = position + 38
                                        # this elif and elif statement is here so that the updated block will be
                                        # aligned with the grid

                                        n = n - 1
                                        block = blocks[n]
                                        size = sizes[n]
                                        drawnblock.undraw()
                                        drawnblock = Image(Point(position, 792 - height * 76), block)
                                        drawnblock.draw(gameScreen)
                                        addBlock = True

                                # slows down the speed only for the current block
                                elif key == "2":  # slow the speed down
                                    slowed = 2

                                # sets the score of the next 5 blocks for 2
                                elif key == "3":  # score multiplier
                                    multiplier = True

                                # sets powerupping to false after you use it
                                powerupping = False
                                draw = False
                                for x in temp:
                                    x.undraw()

                                # grey out all the images to indicate you do not have any power ups available
                                temp = []
                                for x in range(3):
                                    grey_image = Image(Point(950, 200 + x * 200), blackbuttons[x])
                                    grey_image.draw(gameScreen)
                                    temp.append(grey_image)

                    # moves the block left and right forever until it has been placed
                    if draw:  # physical moving of the block
                        drawnblock.move(76 * direction, 0)
                        update()
                        position += 76 * direction
                        if position - size <= 184 or position + size >= 716:
                            direction *= -1

        elif 360 <= click.getX() <= 460 and 540 <= click.getY() <= 560:  # if user clicks resets score
            # overwrites the text file used with "0"
            with open("resources/highscore.txt", "w") as highscorefile:
                highscorefile.write("0")

        elif 463 >= click.getX() >= 137 and 415 >= click.getY() >= 385:  # if user clicks on hotkey
            titleScreen.close()

            # visuals
            hotkeyScreen = GraphWin("Hot Key Edit", 500, 500, autoflush=False)
            hotkeyBackground = Image(Point(250, 250), "resources/hotkeyBackground.gif")
            hotkeyBackground.draw(hotkeyScreen)

            screen = "hotkey fix"

            currentHotkey = Text(Point(250, 450), "Current Hotkey: " + hotkey.upper())
            currentHotkey.draw(hotkeyScreen)
            currentHotkey.setSize(17)
            currentHotkey.setFill("white")

            changeKey = Image(Point(250, 275), "resources/hotkeyText1.gif")
            changeKey.draw(hotkeyScreen)

            confirmChange = Image(Point(250, 325), "resources/hotkeyText2.gif")
            confirmChange.draw(hotkeyScreen)

            # lets user choose options
            while screen == "hotkey fix":
                click = hotkeyScreen.getMouse()
                if 395 >= click.getX() >= 105 and 292 >= click.getY() >= 258:  # if user chooses to change hotkey
                    changeKey.undraw()
                    selectKey = Image(Point(250, 275), "resources/hotkeyText3.gif")
                    selectKey.draw(hotkeyScreen)

                    confirmChange.undraw()

                    update()

                    # sets hotkey to whatever typed
                    hotkey = hotkeyScreen.getKey()
                    if hotkey == "1" or hotkey == "2" or hotkey == "3":  # invalid hotkeys
                        hotkey = "space"

                        # flashes an error message if they choose 1 2 or 3 because those keys are used for
                        # power ups
                        for i in range(3):
                            errorText = Text(Point(350, 50), "Hotkeys cannot be 1, 2, or 3!")
                            errorText.setSize(15)
                            errorText.setFill("red")
                            errorText.setSize(13)
                            errorText.draw(hotkeyScreen)
                            update()
                            time.sleep(0.5)
                            errorText.undraw()
                            update()
                            time.sleep(0.5)

                    currentHotkey.undraw()
                    selectKey.undraw()
                    currentHotkey = Text(Point(250, 450), "Current Hotkey: " + hotkey.upper())
                    currentHotkey.draw(hotkeyScreen)
                    currentHotkey.setSize(17)
                    currentHotkey.setFill("lightgrey")

                    changeKey = Image(Point(250, 275), "resources/hotkeyText1.gif")
                    changeKey.draw(hotkeyScreen)

                    confirmChange = Image(Point(250, 325), "resources/hotkeyText2.gif")
                    confirmChange.draw(hotkeyScreen)

                elif 89 <= click.getX() <= 411 and 338 >= click.getY() >= 312:
                    # exits the hotkey change tab
                    hotkeyScreen.close()
                    screen = "newGame"
                    ending = "none"
                    continue

        elif 335 >= click.getX() >= 265 and 460 >= click.getY() >= 435:  # if user clicks on rules
            rulesScreen = GraphWin("Rules", 500, 500, autoflush=False)
            rulesscreenBackground = Image(Point(250, 250), "resources/rulesBackground.gif")
            rulesscreenBackground.draw(rulesScreen)
            skip = False
            while True:
                page1 = True
                page2 = False

                # lists to store the elements of their pages so we can undraw them
                # when we switch to the previous or next page
                pg1 = []
                pg2 = []
                if skip:
                    cont = True
                    break
                if page1:

                    # visuals
                    text1 = Text(Point(250, 25), "Classic Mode")
                    text1.setSize(25)
                    text1.draw(rulesScreen)
                    text1.setFill("blue")
                    pg1.append(text1)

                    rule1 = Text(Point(250, 125),
                                 "1. You will be given a starter 3x1 block to stack that is constantly moving")
                    rule1.setSize(10)
                    rule1.draw(rulesScreen)
                    rule1.setFill("white")
                    pg1.append(rule1)
                    rule2 = Text(Point(250, 162), "2. The default hot key to stack is space, try to stack all "
                                                  "blocks on your previous one")
                    pg1.append(rule2)
                    rule2.setSize(10)
                    rule2.draw(rulesScreen)
                    rule2.setFill("white")

                    pg1.append(rule2)
                    rule3 = Text(Point(250, 200),
                                 "3. Everytime you misalign your new block with the previous block under it, \n"
                                 "you will lose the misaligned blocks, making a smaller base for you to stack on")
                    rule3.setSize(10)
                    rule3.draw(rulesScreen)
                    rule3.setFill("white")

                    pg1.append(rule3)
                    rule4 = Text(Point(250, 250),
                                 "4. Speeds of the block constantly moving will \nincrease after each level")
                    rule4.setSize(10)
                    rule4.draw(rulesScreen)
                    rule4.setFill("white")

                    pg1.append(rule4)
                    rule5 = Text(Point(250, 300), "5. If you make it to level 4 with 3 block\n"
                                                  " remaining, you will be forced to lose one block")
                    rule5.setSize(10)
                    rule5.draw(rulesScreen)
                    rule5.setFill("white")

                    pg1.append(rule5)
                    rule6 = Text(Point(250, 350), "6. If you make it to level 7 with more than one block remaining, \n "
                                                  "you will also be forced to lose one block")
                    rule6.setSize(10)
                    rule6.draw(rulesScreen)
                    rule6.setFill("white")

                    pg1.append(rule6)

                    blackbox = Rectangle(Point(130, 390), Point(370, 410))
                    blackbox.setFill("black")
                    blackbox.draw(rulesScreen)
                    pg1.append(blackbox)
                    rule7 = Text(Point(250, 400), "7. Once you stack to the top, you win!")
                    rule7.setSize(10)
                    rule7.draw(rulesScreen)
                    rule7.setFill("white")

                    pg1.append(rule7)

                    rule8 = Text(Point(250, 450), "TL;DR \n Time each placement of blocks on top of the \n"
                                                  "previous one, when you hit the top you win!")
                    rule8.setSize(13)
                    rule8.setFill("white")
                    rule8.draw(rulesScreen)
                    rule8.setFill("white")

                    pg1.append(rule8)

                    exittext = Text(Point(475, 485), "Next")
                    exittext.setFill("red")
                    exittext.draw(rulesScreen)
                    pg1.append(exittext)

                    click = rulesScreen.getMouse()

                    # only allows you to click next so you read the endless rules
                    while True:
                        if 460 <= click.getX() <= 490 and 480 <= click.getY() <= 490:
                            page2 = True
                            page1 = False
                            for i in pg1:
                                i.undraw()
                            break
                        click = rulesScreen.getMouse()

                if page2:

                    # visuals
                    text1 = Text(Point(250, 50), "Endless Mode")
                    text1.setSize(25)
                    text1.draw(rulesScreen)
                    text1.setFill("blue")
                    pg2.append(text1)

                    rule1 = Text(Point(250, 100), "1. Same as classic mode but..")
                    rule1.setSize(10)
                    rule1.setFill("white")
                    rule1.draw(rulesScreen)
                    pg2.append(rule1)

                    rule123 = Text(Point(250, 150), "2. Speed will increase slower than classic mode")
                    rule123.setSize(10)
                    rule123.setFill("white")
                    rule123.draw(rulesScreen)
                    pg2.append(rule123)

                    rule2 = Text(Point(250, 200),
                                 "3. You will be given power ups every 5 blocks you stack (these can be saved)")
                    rule2.setSize(10)
                    rule2.setFill("white")

                    rule2.draw(rulesScreen)
                    pg2.append(rule2)

                    rule3 = Text(Point(250, 250), "* Slow-mo: Slow down the speed \nfor your next block by 2x")
                    rule3.setSize(10)
                    rule3.setFill("white")

                    rule3.draw(rulesScreen)
                    pg2.append(rule3)

                    rule4 = Text(Point(250, 300), "* Extended block: Extends your current \n block by 1 to get a"
                                                  " higher chance of \n stacking it correctly")
                    rule4.setSize(10)
                    rule4.draw(rulesScreen)
                    rule4.setFill("white")

                    pg2.append(rule4)

                    rule7 = Text(Point(250, 350), "* Score multiplier: Your next 5 blocks have a \n"
                                                  "score of 2 if stacked properly")
                    rule7.setSize(10)
                    rule7.draw(rulesScreen)
                    rule7.setFill("white")

                    pg2.append(rule7)

                    rule5 = Text(Point(250, 450), "ALSO, ENDLESS STACKING >:)")
                    rule5.setFill("white")
                    rule5.setSize(25)
                    rule5.setFill("white")

                    pg2.append(rule5)
                    rule5.draw(rulesScreen)

                    exittext = Text(Point(475, 485), "Exit")
                    exittext.setFill("red")
                    exittext.draw(rulesScreen)
                    pg2.append(exittext)

                    backtext = Text(Point(25, 485), "Back")
                    backtext.setFill("red")
                    backtext.draw(rulesScreen)
                    pg2.append(backtext)

                    click = rulesScreen.getMouse()
                    while True:
                        # either allows you to go back to classic rules (page 1) or quit the rules tab
                        if 460 <= click.getX() <= 490 and 480 <= click.getY() <= 490:  # quit
                            page2 = False
                            page1 = False
                            skip = True
                            rulesScreen.close()
                            break
                        elif 10 <= click.getX() <= 40 and 480 <= click.getY() <= 490:  # back
                            for i in pg2:
                                i.undraw()
                            page1 = True
                            page2 = False
                            break
                        click = rulesScreen.getMouse()

        elif 520 <= click.getX() <= 580 and 535 <= click.getY() <= 565:  # if user wants to quit from menu
            quit()

        elif 10 <= click.getX() <= 90 and 535 <= click.getY() <= 565:  # if user wants to go to the about screen
            aboutScreen = GraphWin("About", 500, 500)

            # visuals
            aboutscreenBackground = Image(Point(250, 250), "resources/aboutBackground.gif")
            aboutscreenBackground.draw(aboutScreen)

            exitAbout = Text(Point(450, 450), "Exit")
            exitAbout.setSize(20)
            exitAbout.draw(aboutScreen)

            contrib = Text(Point(250, 70), "Jacky Men")
            contrib.draw(aboutScreen)

            aboutGame = Text(Point(250, 125), "About the Game:")
            aboutGame.draw(aboutScreen)
            aboutGame.setSize(20)

            aboutGameText = Text(Point(250, 225), "Stacker is a game where the user tries to align (aka stack) blocks\n"
                                                  "vertically. The blocks will be moving left and right while the user\n"
                                                  "is stacking. When the user inputs the specified key, the moving block\n"
                                                  " will stop and hopefully be aligned with previous stacked blocks.\n"
                                                  "After every level, the speed of the moving blocks will increase.\n"
                                                  "If the stacked newly block is only partially aligned with previous blocks,\n"
                                                  "the misaligned portion of blocks blocks will disappear and the user\n"
                                                  "will be stacking with a smaller block than before; increases the\n"
                                                  "difficulty for future stacking.")
            aboutGameText.draw(aboutScreen)
            version = Text(Point(250, 25), "Version 1.0.0")
            version.draw(aboutScreen)

            features = Text(Point(250, 350), "Additional Features:")
            features.draw(aboutScreen)
            features.setSize(15)
            featuresText = Text(Point(250, 380), "Endless mode, power ups (slow speed, add block, score multiplier),\n"
                                                 "achievements, hot key switch")
            featuresText.draw(aboutScreen)

            eggText = Image(Point(50, 450), "resources/eastereggsmall.gif")
            eggText.draw(aboutScreen)

            easteregg = False
            click = aboutScreen.getMouse()
            while True:
                if 425 <= click.getX() <= 475 and 435 <= click.getY() <= 465:
                    aboutScreen.close()
                    break
                elif 25 <= click.getX() <= 75 and 425 <= click.getY() <= 475:
                    easteregg = True
                    break
                click = aboutScreen.getMouse()

            if easteregg:  # if you click on the easteregg
                aboutScreen.close()

                # visuals
                easterwin = GraphWin("can't believe its all over", 400, 400)

                egg = Image(Point(200, 110), "resources/easteregg.gif")
                egg.draw(easterwin)

                smiley1 = Image(Point(75, 350), "resources/smiley.gif")
                smiley2 = Image(Point(325, 350), "resources/smiley.gif")
                smiley1.draw(easterwin)
                smiley2.draw(easterwin)

                text2 = Text(Point(200, 300), "N\n"
                                              "i\n"
                                              "c\n"
                                              "e\n"
                                              "!")
                text2.draw(easterwin)
                text3 = Text(Point(200, 380), "Just wasted your time :)")
                text3.draw(easterwin)
                easterwin.getMouse()
                easterwin.close() 
