from datetime import datetime, timedelta

class Customer:
    def __init__(self, name, IDnumber):
        """
        Our constructor method which instantiates various customer objects.
        """
        self.name = name
        self.IDnumber = IDnumber
        self.Skis = 0
        self.Snowboards = 0
        self.rentalBasis = 0
        self.rentalTime = 0
        self.bill = 0

    def RequestEquipment(self, intSkisRented, intSnowboardsRented, storeName):
        """
        Takes a request from the customer for the number of skies and bikes.
        """
        self.storeName = storeName                                                      #Use a loop until user gives a valid
                                                                                        
        
        try:
            if intSkisRented < 0 or intSnowboardsRented < 0:                                          #Skis and Snowboards must be positive.
                print("Invalid input. Number of skis and/or snowboards has to be positive!")
                return -1
            else:
                self.Skis = intSkisRented                                           #Return Skis
                self.Snowboards = intSnowboardsRented                               #Return Snowboards.
            # self.Inventory_Check()   Commented by Gleb
            if self.Skis > self.storeName.CurrentSki or self.Snowboards > self.storeName.CurrentSnow:
                print("Value of Skis and/or Snowboards is greater than available amount")
                return -1
            return self.Skis, self.Snowboards
        
        except ValueError:                                                          #Else give a user error.
            print("That's not a number! Please enter a valid number.")              #Ask for a valid input.
            return -1

            
    
    def Inventory_Check(self):
        """
        Check the inventory so user can know what the current available stock of Skis and Snowboards.
        """
        self.storeName.Display_Inv()

    def returnItem(self):
        """
        Allows customers to return their items to the rental shop.
        """
        if self.rentalType and self.rentalTime and self.Skis and self.Snowboards:
            return self.rentalTime, self.rentalType, self.Skis, self.Snowboards
        else:
            return 0,0,0,0
        
class Store:
    """
    The Store the customer can access to be able to see the inventory and stores the Total Transactions.
    """
    dblTotalTransaction = 0

    def __init__(self, SkiInventory = 100, SnowboardInventory = 100):
        self.SkiInventory = SkiInventory
        self.SnowboardInventory = SnowboardInventory
        
    def Display_Inv(self):                                                          #Let the user know the available stock.
        self.CurrentSki = self.SkiInventory                     
        self.CurrentSnow = self.SnowboardInventory
##        print(f"Current Ski Inventory is {self.CurrentSki}.")
##        print(f"Current Snowboard Inventory is {self.CurrentSnow}.")

class Rental(Store):
        """
        Our constructor method which instantiates various Rental Objects.
        """
            
        def __init__(self, customerName, storeName, Skis, Snowboards):
            super().__init__()
            self.customerName = customerName
            self.storeName = storeName
            self.Skis = Skis
            self.Snowboards = Snowboards
        
        def estimateRental(self,rentalType, rentalPeriod):
            """
            Estimate the cost and how much each rental would cost whether it is hourly, daily, or weekly.
            """
            self.rentalEstimate = 0
                                                                   #Rental period is an assumption of time input by the user when calling the function

            if rentalType == 1 and rentalPeriod >= 4:              #If the hours becomes greater than 4. 
                rentalType = 2                                     #Change the rental type to Daily.
                rentalPeriod -= 4                                  #Update it to be 1 Day instead.
                rentalPeriod = int(rentalPeriod / 24) + 1          #Rounds the leftover hours to days adding one from the change
            if rentalType == 2 and rentalPeriod >= 4:              #If the Days becomes greater than 4.
                rentalType = 3                                     #Change the rental type to Weekly.
                rentalPeriod -= 4                                  #Update it to be 1 week instead.
                rentalPeriod = int(rentalPeriod / 7) + 1           #Rounds the leftover days to weeks adding one from the change

            if rentalType == 1:     #Hourly Cost.
                self.rentalEstimate = rentalPeriod * 15 * self.Skis + rentalPeriod * 10 * self.Snowboards
##                print("The estimated cost of the rental is {}.".format(rentalEstimate))
            elif rentalType == 2:   #Daily Cost.
                self.rentalEstimate = rentalPeriod * 50 * self.Skis + rentalPeriod * 40 * self.Snowboards
##                print("The estimated cost of the rental is {}.".format(rentalEstimate))
            elif rentalType == 3:   #Weekly Cost.
                self.rentalEstimate = rentalPeriod * 200 * self.Skis + rentalPeriod * 160 * self.Snowboards
##                print("The estimated cost of the rental is {}.".format(rentalEstimate))
            


        def rentSkis(self, rentalType):
            """
            Calculate the rental for Skis based on hourly, daily, and weekly basis.
            """

            if self.Skis <= 0:                                                               #Reject invalid inputs.
                print("Number of Skis should be positive!")
                return None
            elif self.Skis > self.storeName.SkiInventory:                                    #Let the user know Skis
                print("Sorry! We have {} skis availble to rent.".format(self.storeName.SkiInventory))  #available.
                return None
            else:
                if rentalType == 1:                                                           #Calculate hourly basis.
                    self.rentalTime = datetime.now()
##                    print("You have rented {} skis on a hourly basis today at {} hours.".format(self.Skis,self.rentalTime.hour))
##                    print("You will be charged $15 an hour for each hour for each ski.")
                    self.storeName.CurrentSki -= self.Skis
                    return self.rentalTime
                elif rentalType == 2:                                                         #Calculate Daily Basis.
                    self.rentalTime = datetime.now()
##                    print("You have rented {} skis on a daily basis today at {} hours.".format(self.Skis,self.rentalTime.hour))
##                    print("You will be charged $50 an hour for each hour for each ski.")
                    self.storeName.CurrentSki -= self.Skis
                    return self.rentalTime
                elif rentalType == 3:                                                         #Calculate Weekly Basis.
                    self.rentalTime = datetime.now()
##                    print("You have rented {} skis on a weekly basis today at {} hours.".format(self.Skis,self.rentalTime.hour))
##                    print("You will be charged $200 per week for each ski.")
                    self.storeName.CurrentSki -= self.Skis
                    return self.rentalTime

        def rentSnowboards(self, rentalType):
            """
            Calculate the rental for Snowboards based on hourly, daily, Weekly basis.
            """
            
            if self.Snowboards <= 0:                                                  #Reject invalid inputs.
                print("Number of Snowboards should be positive!")
                return None
            elif self.Snowboards > self.storeName.SnowboardInventory:                 #Let the user know Snowbords available.
                print("Sorry! We have {} skis availble to rent.".format(self.storeName.SnowboardInventory))
                return None
            else:
                if rentalType == 1:                                                   #Calculate Hourly Basis.
                    self.rentalTime = datetime.now()
##                    print("You have rented {} snowboards on a hourly basis today at {} hours.".format(self.Snowboards,self.rentalTime.hour))
##                    print("You will be charged $10 an hour for each hour for each snowboards.")
                    self.storeName.CurrentSnow -= self.Snowboards
                    return self.rentalTime
                elif rentalType == 2:                                                 #Calcualte Daily Basis.
                    self.rentalTime = datetime.now()
##                    print("You have rented {} snowboards on a daily basis today at {} hours.".format(self.Snowboards,self.rentalTime.hour))
##                    print("You will be charged $40 an hour for each hour for each snowboard.")
                    self.storeName.CurrentSnow -= self.Snowboards    
                    return self.rentalTime
                elif rentalType == 3:                                                 #Calculate Weekly Basis.
                    self.rentalTime = datetime.now()

                    self.storeName.CurrentSnow -= self.Snowboards
                    return self.rentalTime

                
        def calculateRentalCost(self,rentalType,return_time=None):
            """
            Calculate the Rental Cost before discounts.
            """
            actual_return_time = return_time if return_time is not None else datetime.now()
            rentalPeriod = actual_return_time - self.rentalTime

            if rentalType == 1 and (round(rentalPeriod.seconds / 3600)) >= 4:       #If the hours becomes greater than 4. 
                rentalType = 2                                                      #Change the rental type to Daily.
                rentalPeriod += timedelta(days=1)                                   #Update it to be 1 Day instead.

            if rentalType == 2 and (round(rentalPeriod.days)) >= 4:                 #If the Days becomes greater than 4.
                rentalType = 3                                                      #Change the rental type to Weekly.
                rentalPeriod += timedelta(days=7)                                  #Update it to be 1 week instead.

            if rentalType == 1:     #Hourly Cost.
                hours = max(1, rentalPeriod.seconds / 3600)
                dblSubTotal = (hours * 15 * self.Skis) + (hours * 10 * self.Snowboards)
            elif rentalType == 2:   #Daily Cost.
                days = max(1, rentalPeriod.days) 
                dblSubTotal = (days * 50 * self.Skis) + (days * 40 * self.Snowboards)
            elif rentalType == 3:   #Weekly Cost.
                weeks = max(1, rentalPeriod.days / 7) 
                dblSubTotal = (weeks * 200 * self.Skis) + (weeks * 160 * self.Snowboards)
            self.SubTotal = dblSubTotal
            
            
        
        def familyDiscount(self):
            """
            Calculate the total Rental Cost after Family Discount is applied.
            """

            if self.Skis + self.Snowboards < 3:                             #If Total number of equipment is less than 3.
                return 0                                                    #Family Discount will be 0.
            elif self.Skis + self.Snowboards > 5:                           #Else if total number of equipment greater than 5.
                return 0                                                    #Family Discount will be 0.
            else:                                                           #If equipment is 3, 4, or 5.
                print("You have recieved a 25% off the total purchase!")    
                self.SubTotal *= .75                                        #Total cost is reduced by 25%.

        def discountCode(self, strdiscountCode):                              
            """
            Checking to see if the string code entered has the ending of "BBP"
            """

            if strdiscountCode.endswith("BBP") and len(strdiscountCode) == 6:   #If Discount Code ends with BBP and is 6 characters.
                self.SubTotal *= 0.90
                print("Discount of 10% has been applied to your purchase")      #Customer recieves a 10% discount.
            # else:
            #     print("Discount Code entered is not accepted")
                
        def finalCost(self):
            """
            Final Calculations of the total cost for the purchase.
            """

            dblFinalCost = self.SubTotal                            #Total Cost for all purchases after discounts applied.
            self.storeName.dblTotalTransaction += dblFinalCost
            #print(dblFinalCost)  Commented by Gleb
            return dblFinalCost

        def returnInv(self):
            """
            Returns the inventory to reset the CurrentSki and CurrentSnow attributes in the shop
            """

            self.storeName.CurrentSki += self.Skis
            self.storeName.CurrentSnow += self.Snowboards
            self.Skis = 0
            self.Snowboards = 0

# Create Customers

#customer1 = Customer("John", 1)
#customer2 = Customer("Jimmy", 2)
#customer3 = Customer("Jane", 3)
#customer4 = Customer("Tiffany", 4)

#store1 = Store(100,100)
#store2 = Store(100,150)

#store1.Display_Inv()
#store2.Display_Inv()

#rental1 = Rental(customer1, store1, 1, 1)
#rental2 = Rental(customer1, store1, 3, 1)

#rental1.rentSkis(1)
#rental2.rentSkis(1)
#rental2.rentSnowboards(1)

#rental1.rentalTime = datetime.now() + timedelta(hours=-4)
#rental2.rentalTime = datetime.now() + timedelta(hours=-23)

#rental1.calculateRentalCost(1)
#rental2.calculateRentalCost(1)
#rental2.familyDiscount()

#rental1.discountCode("jifvis")
#rental1.discountCode("jhkBBP")




#rental1.estimateRental(2,8)
#rental1.finalCost()
#rental2.finalCost()
#print(store1.dblTotalTransaction)
