from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import way2sms
from easygui import passwordbox



#The bms varialbe should have the link for for the movie in BookMyShow.
bms = "https://in.bookmyshow.com/buytickets/avengers-infinity-war-3d-hyderabad/movie-hyd-ET00073463-MT/20180428"
#malls = ['PVR ICON: Hitech, Madhapur, Hyderabad', 'Prasads: Hyderabad','Asian M Cube Mall: Attapur','Mukta A2 Cinemas: Abids']

#You can enter the names of the halls present in your city. You can get the names of the halls, by going through BookMyShow
malls = ['PVR ICON: Hitech, Madhapur, Hyderabad', 'Prasads: Hyderabad','Asian M Cube Mall: Attapur']

def checkConnectionToWay2SMS():
    queue = way2sms.sms(username, password)
    if queue.loggedIn == True:
        print("Way2SMS Password Correct")
        queue.logout()
        return True
    else:
        return False

def sendMessageToMobile(text,number):
    mobile_number_to_send = number
    message = text
    queue = way2sms.sms(username, password)
    queue.send(mobile_number_to_send, message)
    n = queue.msgSentToday()
    queue.logout()
    #print("Going into Sleep for Response.")


username = input("Enter Username: ")
password = passwordbox("Enter Password: ")


checkForLogin = checkConnectionToWay2SMS()
numberOfRuns = 1
if checkForLogin == True:
    ticketNotAvailable = True
    while ticketNotAvailable:
        print("Running Script Iteration: ", numberOfRuns)
        page = urlopen(bms)
        soup = BeautifulSoup(page, "lxml")

        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.decompose()    # rip it out

        # get text
        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)


        for mall in malls:
            if mall in text:
                sendMessageToMobile("Avengers Ticket Available at " + mall + ". Hurry!",<Enter the Number you want to send Message to!>)
                print("Ticket Available in: ", mall)
                ticketNotAvailable = False
                time.sleep(300)

        if ticketNotAvailable == True:
            print("Ticket still not available. Pausing Web Scrapping.\n")
            time.sleep(45)
            numberOfRuns += 1

else:
    print("Invalid Username Password")
