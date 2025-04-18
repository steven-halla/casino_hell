import pygame
import logging
from typing import Dict


class Controller:
    def __init__(self):
        self.isLeftPressed: bool = False
        self.isRightPressed: bool = False
        self.isUpPressed: bool = False
        self.isDownPressed: bool = False
        self.isExitPressed: bool = False
        self.isAPressed: bool = False
        self.isQPressed: bool = False
        self.isLPressed: bool = False
        self.isKPressed: bool = False
        self.isJPressed: bool = False
        self.isRPressed: bool = False
        self.isEPressed: bool = False
        self.isWPressed: bool = False
        self.is1Pressed: bool = False
        self.isTPressed: bool = False
        self.isPPressed: bool = False
        self.isOPressed: bool = False
        self.isBPressed: bool = False
        self.keyPressedTimes: Dict[int, int] = {}  # Map<key number, key pressed millisecond
        self.keyReleasedTimes: Dict[int, int] = {}  # Map<key number, key pressed millisecond
        # might need to delete this bottom line pygame.init()
        self.isAPressedSwitch: bool = False
        self.isStartPressedSwitch: bool = False

        self.isBPressedSwitch: bool = False
        self.isXPressedSwitch: bool = False
        self.isYPressedSwitch: bool = False
        self.isLeftStickPressed: bool = False
        self.isRightStickPressed: bool = False

        # Initialize D-pad flags
        self.isLeftPressedSwitch: bool = False
        self.isRightPressedSwitch: bool = False
        self.isUpPressedSwitch: bool = False
        self.isDownPressedSwitch: bool = False
        pygame.init()
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            logging.info(f"Controller connected: {self.joystick.get_name()}")
        else:
            self.joystick = None
            logging.info("No joystick detected!")

    def timeSinceKeyPressed(self, key: int):
        if key not in self.keyPressedTimes:
            return -1
        return pygame.time.get_ticks() - self.keyPressedTimes[key]

    def timeSinceKeyReleased(self, key: int):
        if key not in self.keyReleasedTimes:
            return -1
        return pygame.time.get_ticks() - self.keyReleasedTimes[key]



    def update(self):
        # current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                continue


            if event.type == pygame.QUIT:
                self.isExitPressed = True

            # Handle D-pad input (JOYHATMOTION)
            # Handle D-pad input (JOYHATMOTION)
            if event.type == pygame.JOYHATMOTION and self.joystick:
                # logging.info(f"JOYHATMOTION detected: hat={event.hat}, value={event.value}")
                if event.hat == 0:  # Assuming the D-pad is the first hat
                    if event.value == (0, 1):  # Up
                        self.isUpPressedSwitch = True
                        self.isDownPressedSwitch = False
                        self.isLeftPressedSwitch = False
                        self.isRightPressedSwitch = False
                        # self.isXPressedSwitch = False

                    elif event.value == (0, -1):  # Down
                        self.isUpPressedSwitch = False
                        self.isDownPressedSwitch = True
                        self.isLeftPressedSwitch = False
                        self.isRightPressedSwitch = False
                        # self.isXPressedSwitch = False

                    elif event.value == (-1, 0):  # Left
                        self.isUpPressedSwitch = False
                        self.isDownPressedSwitch = False
                        self.isLeftPressedSwitch = True
                        self.isRightPressedSwitch = False
                        # self.isXPressedSwitch = False

                    elif event.value == (1, 0):  # Right
                        self.isUpPressedSwitch = False
                        self.isDownPressedSwitch = False
                        self.isLeftPressedSwitch = False
                        self.isRightPressedSwitch = True
                        # self.isXPressedSwitch = False

                    elif event.button == 2:  # X button
                        self.isXPressedSwitch = True
                        self.isUpPressedSwitch = False
                        self.isDownPressedSwitch = False
                        self.isLeftPressedSwitch = False
                        self.isRightPressedSwitch = False
                    elif event.value == (0, 0):  # Neutral
                        self.isUpPressedSwitch = False
                        self.isDownPressedSwitch = False
                        self.isLeftPressedSwitch = False
                        self.isRightPressedSwitch = False
                        # self.isXPressedSwitch = False


            # Handle button input (JOYBUTTONDOWN and JOYBUTTONUP)
            if event.type == pygame.JOYBUTTONDOWN:

                if event.button == 0:  # A button
                    self.isAPressedSwitch = True
                    logging.info("Controller A button pressed!!!!!")

                elif event.button == 1:  # B button
                    self.isBPressedSwitch = True
                elif event.button == 2:  # X button
                    self.isXPressedSwitch = True


                elif event.button == 11:  # D-pad Up
                    self.isUpPressedSwitch = True
                elif event.button == 12:  # D-pad Down
                    self.isDownPressedSwitch = True
                elif event.button == 13:  # D-pad Left
                    self.isLeftPressedSwitch = True
                elif event.button == 14:  # D-pad Right
                    self.isRightPressedSwitch = True
                elif event.button == 6:  # Start
                    self.isStartPressedSwitch = True

                elif event.button == 4:  # select
                    self.isRightPressedSwitch = True




            elif event.type == pygame.JOYBUTTONUP:
                # logging.info("is up pressed switch ")

                if event.button == 0:  # A button
                    self.isAPressedSwitch = False
                elif event.button == 1:  # B button
                    self.isBPressedSwitch = False

                elif event.button == 6:  # Start
                    self.isStartPressedSwitch = False
                # elif event.button == 2:  # X button
                #     self.isXPressedSwitch = False
                elif event.button == 11:  # D-pad Up
                    self.isUpPressedSwitch = False
                elif event.button == 12:  # D-pad Down
                    self.isDownPressedSwitch = False
                elif event.button == 13:  # D-pad Left
                    self.isLeftPressedSwitch = False
                elif event.button == 14:  # D-pad Right
                    self.isRightPressedSwitch = False

                # # Handle analog stick movement (JOYAXISMOTION)
                # if event.type == pygame.JOYAXISMOTION:
                #     if event.axis == 0:  # Left stick horizontal
                #         if event.value < -0.5:
                #             self.isLeftStickPressed = True
                #         elif event.value > 0.5:
                #             self.isRightStickPressed = True
                #         else:
                #             self.isLeftStickPressed = False
                #             self.isRightStickPressed = False

            if event.type == pygame.KEYDOWN:
                # logging.info("nononono yes")

                self.keyPressedTimes[event.key] = pygame.time.get_ticks()

                if event.key == pygame.K_LEFT:
                    self.isLeftPressed = True
                elif event.key == pygame.K_RIGHT:
                    self.isRightPressed = True
                elif event.key == pygame.K_UP:
                    self.isUpPressed = True
                elif event.key == pygame.K_DOWN:
                    self.isDownPressed = True
                elif event.key == pygame.K_a:
                    self.isAPressed = True
                elif event.key == pygame.K_q:
                    self.isQPressed = True
                elif event.key == pygame.K_j:
                    self.isJPressed = True
                elif event.key == pygame.K_k:
                    self.isKPressed = True
                elif event.key == pygame.K_l:
                    self.isLPressed = True
                elif event.key == pygame.K_r:
                    self.isRPressed = True
                elif event.key == pygame.K_e:
                    self.isEPressed = True
                elif event.key == pygame.K_t:
                    logging.info("KEYBOARD T button pressed!")

                    self.isTPressed = True
                elif event.key == pygame.K_w:
                    self.isWPressed = True
                elif event.key == pygame.K_1:
                    self.is1Pressed = True
                elif event.key == pygame.K_p:
                    self.isPPressed = True
                elif event.key == pygame.K_o:
                    self.isOPressed = True
                elif event.key == pygame.K_1:
                    self.is1Pressed = True
                elif event.key == pygame.K_b:
                    self.isBPressed = True


            elif event.type == pygame.KEYUP:
                self.keyReleasedTimes[event.key] = pygame.time.get_ticks()
                # print(self.keyReleasedTimes)

                if event.key == pygame.K_LEFT:
                    self.isLeftPressed = False
                elif event.key == pygame.K_RIGHT:
                    self.isRightPressed = False
                elif event.key == pygame.K_UP:
                    self.isUpPressed = False
                elif event.key == pygame.K_DOWN:
                    self.isDownPressed = False
                elif event.key == pygame.K_a:
                    self.isAPressed = False
                elif event.key == pygame.K_q:
                    self.isQPressed = False
                elif event.key == pygame.K_j:
                    self.isJPressed = False
                elif event.key == pygame.K_k:
                    self.isKPressed = False
                elif event.key == pygame.K_l:
                    self.isLPressed = False
                elif event.key == pygame.K_r:
                    self.isRPressed = False
                elif event.key == pygame.K_e:
                    self.isEPressed = False
                elif event.key == pygame.K_t:
                    self.isTPressed = False
                elif event.key == pygame.K_w:
                    self.isWPressed = False
                elif event.key == pygame.K_1:
                    self.is1Pressed = False
                elif event.key == pygame.K_p:
                    self.isPPressed = False
                elif event.key == pygame.K_o:
                    self.isOPressed = False
                elif event.key == pygame.K_1:
                    self.is1Pressed = False
                elif event.key == pygame.K_b:
                    self.isBPressed = False

    @property
    def confirm_button(self) -> bool:
        if self.isTPressed or self.isAPressedSwitch:
            self.isTPressed = False
            self.isAPressedSwitch = False
            return True
        return False

    @property
    def action_and_cancel_button(self) -> bool:
        if self.isBPressed or self.isBPressedSwitch:
            self.isBPressed = False
            self.isBPressedSwitch = False
            return True
        return False

    @property
    def up_button(self) -> bool:
        if self.isUpPressed or self.isUpPressedSwitch:
            self.isUpPressed = False
            self.isUpPressedSwitch = False
            return True
        return False

    @property
    def down_button(self) -> bool:
        if self.isDownPressed or self.isDownPressedSwitch:
            self.isDownPressed = False
            self.isDownPressedSwitch = False
            return True
        return False

    @property
    def left_button(self) -> bool:
        if self.isLeftPressed or self.isLeftPressedSwitch:
            self.isLeftPressed = False
            self.isLeftPressedSwitch = False
            return True
        return False

    @property
    def right_button(self) -> bool:
        if self.isRightPressed or self.isRightPressedSwitch:
            self.isRightPressed = False
            self.isRightPressedSwitch = False
            return True
        return False

    @property
    def start_button(self) -> bool:
        if self.isStartPressedSwitch or self.isPPressed:
            self.isStartPressedSwitch = False
            self.isPPressed = False
            return True
        return False

