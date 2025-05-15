import sys
import os

class MenuSystem:
    def __init__(self, strBackKey: str = "b", strForwardKey: str = "f", strMainMenuKey: str = "m", pseudoRefresh: bool = False):
        self.backKey = strBackKey
        self.forwardKey = strForwardKey
        self.mainMenuKey = strMainMenuKey
        self.headers: list[str] = list()
        self.mainMenu: Menu = None
        self.currentMenu: Menu = None
        self.menuStack: list[Menu] = []
        self.pseudoRefresh = pseudoRefresh

    def set_main_menu(self, menu):
        if isinstance(menu, Menu):
            menu.__class__.menuSystemInstance = self
            self.mainMenu = menu
            self.currentMenu = menu
            self.menuStack = [menu]

    def set_default_headers(self):
        self.headers.append("-------Navigation------")
        self.headers.append("b - back  m - main menu")
        self.headers.append("-----------------------")
        self.headers.append("")

    def show(self):
        self.currentMenu.show_menu()

    def show_main(self):
        self.currentMenu = self.mainMenu
        self.show()
    
    # def create_menu(self, type, menuName):



    def navigate_forward(self):
        if self.currentMenu in self.menuStack:
            index = self.menuStack.index(self.currentMenu)
            if index < len(self.menuStack) - 1:
                self.currentMenu = self.menuStack[index + 1]
                self.show()

    def navigate_back(self):
        if self.currentMenu in self.menuStack:
            index = self.menuStack.index(self.currentMenu)
            if index > 0:
                self.currentMenu = self.menuStack[index - 1]
                self.show()

    def navigate_to(self, menu):
        if self.currentMenu in self.menuStack:
            index = self.menuStack.index(self.currentMenu)
            self.menuStack = self.menuStack[:index + 1]  # truncate forward history
        self.menuStack.append(menu)
        self.currentMenu = menu
        self.show()


class Menu:
    menuSystemInstance: MenuSystem = None
    def __init__(self, strName: str, mSystem: MenuSystem = None, showHeades: bool = True):

        if mSystem is None:
            mSystem = self.__class__.menuSystemInstance

        if not isinstance(mSystem, MenuSystem):
            raise Exception("Invalid or missing MenuSystem instance.")     

        self.name: str = strName
        self.menuSystem = mSystem
        self.menuText: list[str] = list()
        self.showHeaders = showHeades

    def show_instruction(self) -> None:
        if self.menuSystem.pseudoRefresh:
            self.clear_console()
        if self.showHeaders:
            for header in self.menuSystem.headers:
                print(header)
        for str in self.menuText:
            print(str)


    def show_menu(self):
        self.show_instruction()
        self.get_input()
        self.menuSystem.navigate_back()

    def clear_console(self):
        os.system("cls")



    def get_input(self) -> str:
        inputValue = input()
        if inputValue == self.menuSystem.backKey:
            self.menuSystem.navigate_back()
        elif inputValue == self.menuSystem.forwardKey:
            self.menuSystem.navigate_forward()
        elif inputValue == self.menuSystem.mainMenuKey:
            self.menuSystem.show_main()
        else:
            return inputValue

    def wait(self, strText: str = ""):
        if len(strText) > 0:
            input(strText)
        else:
            input("Press Enter to continue...")


class TestMenu1(Menu):
    def __init__(self, strName, mSystem):
        super().__init__(strName, mSystem)
        self.menuText.append("This is test menu 1")
        self.menuText.append("Press 1 to navigate to test menu 2")


    def get_input(self):
        while True:
            inputValue= super().get_input()
            if inputValue == "1":
                self.menuSystem.navigate_to(TestMenu2("Test menu 2", self.menuSystem))
                break
            else:
                print("Invalid input.")


class TestMenu2(Menu):
    def __init__(self, strName, mSystem, showHeaders = True):
        super().__init__(strName, mSystem, showHeaders)
        self.menuText.append("This is test menu 2.")
        self.menuText.append("Write 3 to go to menu 3")

    def get_input(self):
        while True:
            inputValue = super().get_input()
            if inputValue == "3":
                self.menuSystem.navigate_to(TestMenu3("Addition", self.menuSystem))
            else:
                print("Wrong command...")

class TestMenu3(Menu):
    def __init__(self, strName, mSystem):
        super().__init__(strName, mSystem)
        self.menuText.append("This is test menu 2.")
        self.menuText.append("You can calculate sum of two digits")

    def get_input(self):
        while True:
            print("Write number a")
            intA = int(super().get_input())
            print("Write number b")
            intB = int(super().get_input())
            print("Sum of A and B = " + str(intA + intB))
            self.wait("Press any key to return to main menu")
            self.menuSystem.show_main()


class MainMenu(Menu):
    def __init__(self, strName, mSystem = None, showHeaders = True):
        super().__init__(strName, mSystem, showHeaders)
        self.menuText.append("--------Main Menu----------")
        self.menuText.append("1 - Navigate to Test Menu 1")
        self.menuText.append("2 - Navigate to Test Menu 2")
        self.menuText.append("3 - Exit")
    
    def show_instruction(self):
         super().show_instruction()

    def get_input(self):
        while True:
            inputValue = input()
            if inputValue == "1":
                self.menuSystem.navigate_to(TestMenu1("Test 1", self.menuSystem))
                break
            elif inputValue == "2":
                self.menuSystem.navigate_to(TestMenu2("Test 2", self.menuSystem))
                break
            elif inputValue == "3":
                sys.exit()
            else:
                print("No such command. Try again.")
            

if __name__ == "__main__":

   

    mSys = MenuSystem(pseudoRefresh=True)

    MainMenu.menuSystemInstance = mSys

    mainMenu = MainMenu("Main Menu")

    mSys.set_main_menu(MainMenu("Main", mSys, False))
    mSys.set_default_headers()
    mSys.show()
