
import hashlib
import binascii
from time import time

#open file words.txt
words = [line.strip().lower() for line in open('words.txt')]
words.reverse()
wordset = {word for word in words}
passwords1 = [line.strip() for line in open('passwords1.txt')]
passwords2 = {line.strip() for line in open('passwords2.txt')}
passwords3 = [line.strip() for line in open('passwords3.txt')]

#print("set?", type(wordset))
#print("aa" in wordset)

class User:
    def __init__(self, username, password_H, salt=""):
        self.username = username
        self.password_H = password_H
        self.salt = salt
        self.password_U = ""


def calculateHash(word):
    #steps he includes in short sample program
    encoded_word = word.encode('utf-8') # type=bytes
    hasher = hashlib.sha256(encoded_word)
    digest = hasher.digest() # type=bytes
    digest_as_hex = binascii.hexlify(digest)
    digest_as_hex_string = digest_as_hex.decode('utf-8')
    return digest_as_hex_string


def part1():
    peopleList = []
    for line in passwords1:
        contents = line.split(":")
        newPerson = User(contents[0], contents[1])
        peopleList.append(newPerson)

    f = open("cracked1.txt", "a")

    hashcount = 0
    hashtimes = []
    crackcount = 0
    cracktimes = []

    total_start = time()

    for word in words:
        start = time()
        hash = calculateHash(word) #this is a string
        hashcount+=1
        hash_end = time()
        hash_elapsed = hash_end - start
        hashtimes.append(hash_elapsed)
        for person in peopleList:
            if hash == person.password_H:
                crack_end = time()
                crack_elapsed = crack_end - start
                cracktimes.append(crack_elapsed)
                crackcount+=1
                person.password_U = word
                f.write(person.username+":"+person.password_U+"\n")

    total_end = time()
    total_elapsed = total_end - total_start
    average_hash_time = sum(hashtimes) / len(hashtimes)
    average_crack_time = sum(cracktimes) / len(cracktimes)
    crack_per_hash = crackcount / hashcount

    print("Part 1")
    print("Total time:", total_elapsed, "s")
    print("Number of hashes computed:", hashcount)
    print("Passwords cracked:", crackcount)
    print("Time per hash computed:", average_hash_time)
    print("Time per password cracked:", average_crack_time)
    print("Passwords cracked per number of hashes computed:", crack_per_hash)


def part2():
    #peopleList = []
    peopleDictionary = {}

    for line in passwords2:
        contents = line.split(":")
        #newPerson = User(contents[0], contents[1])
        #peopleList.append(newPerson)
        peopleDictionary[contents[0]] = contents[1]

    f = open("cracked2.txt", "a")

    hashcount = 0
    hashtimes = []
    crackcount = 0
    cracktimes = []
    currword = ""

    #f.write("jondich:moose\n") #because moose >:)
    total_start = time()

    for word in words:
        for secondword in words:
            #start = time()
            #secondword = words[i+1505]
            guessword = word+secondword
            hash = calculateHash(guessword) #this is a string
            hashcount+=1
            #hash_end = time()
            #hash_elapsed = hash_end - start
            #hashtimes.append(hash_elapsed)
            for person in peopleDictionary:
                if hash == peopleDictionary[person]:
                    #crack_end = time()
                    #crack_elapsed = crack_end - start
                    #cracktimes.append(crack_elapsed)
                    crackcount+=1
                    #person.password_U = guessword
                    #f.write(person.username+":"+person.password_U+"\n")
                    f.write(person+":"+guessword+"\n")
                    break

        curr_time = time()
        if curr_time - total_start >= 60:
            currword = word
            break

    total_end = time()
    total_elapsed = total_end - total_start
    #average_hash_time = sum(hashtimes) / len(hashtimes)
    if len(cracktimes) != 0:
        average_crack_time = sum(cracktimes) / len(cracktimes)
    else:
        average_crack_time = 0
    crack_per_hash = crackcount / hashcount

    print("Part 2 (sets)")
    print("I made it to:", currword)
    print("Total time:", total_elapsed, "s")
    print("Number of hashes computed:", hashcount)
    print("Passwords cracked:", crackcount)
    #print("Time per hash computed:", average_hash_time)
    #print("Time per password cracked:", average_crack_time)
    print("Passwords cracked per number of hashes computed:", crack_per_hash)

    print("\a" * 5)


def part3():
    peopleList = []
    for line in passwords3:
        contents = line.split(":")
        username = contents[0]
        passwordlist = contents[1].split("$")
        salt = passwordlist[2]
        password = passwordlist[3]
        newPerson = User(username, password, salt)
        peopleList.append(newPerson)

    f = open("cracked3.txt", "a")

    hashcount = 0
    hashtimes = []
    crackcount = 0
    cracktimes = []

    #f.write("jondich:moose\n") #because moose >:)
    total_start = time()

    for person in peopleList:
        #print("current person:", person.username)
        for word in words:
            start = time()
            guessword = person.salt + word
            #print(guessword)
            hash = calculateHash(guessword) #this is a string
            hashcount+=1
            hash_end = time()
            hash_elapsed = hash_end - start
            hashtimes.append(hash_elapsed)

            if hash == person.password_H:
                crack_end = time()
                crack_elapsed = crack_end - start
                cracktimes.append(crack_elapsed)
                crackcount+=1
                person.password_U = word
                f.write(person.username+":"+person.password_U+"\n")
                break

        #curr_time = time()
        #if curr_time - total_start >= 28800:
            #break

    total_end = time()
    total_elapsed = total_end - total_start
    average_hash_time = sum(hashtimes) / len(hashtimes)
    if len(cracktimes) != 0:
        average_crack_time = sum(cracktimes) / len(cracktimes)
    else:
        average_crack_time = 0
    crack_per_hash = crackcount / hashcount

    print("Part 3")
    print("Total time:", total_elapsed, "s")
    print("Number of hashes computed:", hashcount)
    print("Passwords cracked:", crackcount)
    print("Time per hash computed:", average_hash_time)
    print("Time per password cracked:", average_crack_time)
    print("Passwords cracked per number of hashes computed:", crack_per_hash)

    #print("\a" * 5)

#part1()
#part2()
#part3()
