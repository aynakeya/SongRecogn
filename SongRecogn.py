from srModule import recognize,add_audio,add_dir
from srModule import Database,Console
import sys,getopt,os,time



description = "A song recognize application using Shazam algorithm"
console_methods = {
    "add-audio":"add a audio to the database",
    "add-dir":"add audio from a directory",
    "recognize":"recognzie a audio sample from file",
    "help":"show help",
    "quit":"Quit"
}
console_methods_usage = {
    "add-audio":"add-audio song/lingyu.mp3",
    "add-dir":"add-audio song",
    "recognize":"recognzie sample/lingyu_01.mp3"
}
console_methods_factory = {
    "add-audio":add_audio,
    "add-dir":add_dir,
    "recognize":recognize
}

if __name__ == "__main__":
    Console.log("Check connection with the database......",end="")
    status,code,msg = Database.checkDatabase()
    if not status:
        Console.log("Connect to database failed: %s" % msg)
        Console.log("Please check config or database.")
        sys.exit()
    Console.log("Success!")
    time.sleep(1)
    os.system("cls")

    Console.log("-" * 20)
    Console.log(description)
    Console.log("-" * 20)



    while True:
        command = input("Command: ")
        method = command.split(" ")[0]
        args = command[len(method)+1::]

        if not method in console_methods.keys():
            Console.log("Invalid method.")
            continue
        if method == "quit":
            Console.log("Stop console")
            sys.exit()
        if method == "help":
            for key,value in console_methods.items():
                Console.log(key, ":", value)
                if key in console_methods_usage.keys():
                    Console.log(" "*(len(key)+1),"usage :help"
                                           "",console_methods_usage[key])
            continue
        if len(args) == 0:
            Console.log("args not found.")
            continue
        console_methods_factory[method](args)
