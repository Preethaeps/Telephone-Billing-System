import mysql.connector as mq
from tabulate import tabulate
import random


def menu():
    print("\n--------------------------------------------------------------------\n")
    print("\t\t\t =======================")
    print("\t\t\t TELEPHONE BILLING SYSTEM")
    print("\t\t\t =======================\n")
    print("--------------------------------------------------------------------\n")

    print("\t\t\t\t =========")
    print("\t\t\t\t MAIN MENU")
    print("\t\t\t\t =========\n\n")

    print("\t\t 1. Register User  \t\t 2. Search Customer \n")
    print("\t\t 3. Update Customer \t 4. Generate Bill\n")
    print("\t\t 5. Delete Customer \t 6. Help \n\n\t\t 7. Exit\n")
    print("--------------------------------------------------------------------")


def register():
    print("\n\t\t\t =========================")
    print("\t\t\t NEW CUSTOMER REGISTRATION")
    print("\t\t\t =========================\n\n")
    ph = input("Enter Your PHONE NO. :  ")
    nam = input("Enter Your NAME :  ")
    add = input("Enter Your ADDRESS :  ")
    aadhar = input("Enter Your AADHAR NO. :  ")
    acc_id = random.randint(1000, 9999)
    con = mq.connect(host="localhost", user="root", passwd="123456", database="preetha")
    cur = con.cursor()
    query1 = "insert into cust(phno, name, addr, aadhar) values ({},'{}','{}','{}')".format(ph, nam, add, aadhar)
    cur.execute(query1)
    query2 = "insert into accounts(phno, accid) values ({}, {})".format(ph, acc_id)
    cur.execute(query2)
    query3 = "insert into billing(phno, accid) values ({}, {})".format(ph, acc_id)
    con.commit()
    print("\n\t\t--------------------------------------------------------------------")
    print("\t\t\t\t !!! SUCCESSFULLY REGISTERED THE USER !!!")
    print("\t\t--------------------------------------------------------------------\n")
    con.close()


def search():
    print("\n\t\t\t\t ===============")
    print("\t\t\t\t SEARCH CUSTOMER")
    print("\t\t\t\t ===============\n\n")
    ph = input("Enter your PHONE NO. :  ")
    con = mq.connect(host="localhost", user="root", passwd="123456", database="preetha")
    cur = con.cursor()
    print("\n 1.Customer details \n 2.Billing details")
    ch=int(input("\n Enter the choice for the details required: "))
    query1 = "select phno, name, addr, aadhar, accid, regdate from cust natural join accounts where phno={}".format(ph)
    query2 = "select phno,accid,amt_payed,date_paid,calls from accounts natural join billing natural join payment where phno={}".format(ph)
    if ch == 1:
        cur.execute(query1)
        res1 = cur.fetchall()
        if res1 == [] :
            print("\n Customer doesn't Exist...")
        else:
            print("\n  Phone No.   Acc_id    Name     Address      Aadhar Register_date   ")
            print(tabulate(res1, tablefmt="grid"))
    elif ch == 2:
        cur.execute(query2)
        res2 = cur.fetchall()
        if res2 == [] :
            print("\n Customer doesn't Exist...")
        else:
            print("\n  Phone No.   Acc_id Amt_paid Date_paid Calls")
            print(tabulate(res2, tablefmt="grid"))
    else:
        print("your selection is invalid")
    con.close()


def modify():
    print("\n\t\t\t\t ====================")
    print("\t\t\t\t UPDATE CUSTOMER DATA")
    print("\t\t\t\t =====================\n\n")
    ph = input("Enter Your PHONE NO. :  ")
    con = mq.connect(host="localhost", user="root", passwd="123456", database="preetha")
    cur = con.cursor()
    query = "select * from cust where phno={}".format(ph)
    cur.execute(query)
    res = cur.fetchall()
    if res == []:
            print("\n Customer doesn't Exist...")
    else:
            print("\n 1. Change Name\n 2. Change Address\n 3. Change Aadhar No.")
            ch = int(input("\nEnter Which You Would Like to Change :  "))
    if ch == 1:
                nam = input("Enter New NAME :  ")
                query = "update cust set name= '{}' where phno={}".format(nam, ph)
                cur.execute(query)
                con.commit()
                print("\n\t\t----------------------------------------------------------")
                print("\t\t\t\t !!! SUCCESSFULLY UPDATED YOUR NAME !!!")
                print("\t\t----------------------------------------------------------\n")
    elif ch == 2:
                add = input("Enter New ADDRESS :  ")
                query = "update cust set addr = '{}' where phno={}".format(add, ph)
                cur.execute(query)
                con.commit()
                print("\n\t\t----------------------------------------------------------")
                print("\t\t\t\t !!! SUCCESSFULLY UPDATED YOUR ADDRESS !!!")
                print("\t\t----------------------------------------------------------\n")
    elif ch == 3:
                aadhar = input("Enter New AADHAR NO. :  ")
                query = "update cust set aadhar= '{}' where phno={}".format(aadhar, ph)
                cur.execute(query)
                con.commit()
                print("\n\t\t----------------------------------------------------------")
                print("\t\t\t\t !!! SUCCESSFULLY UPDATED YOUR AADHAR NO. !!!")
                print("\t\t----------------------------------------------------------\n")
    else:
                print("Please Enter the Correct Choice :  ")

    con.close()


def billing():
    print("\n\t\t\tBilling")
    print(" "
          "\t\t\t--------\n")
    ph = input("\nEnter your phone number:")
    con = mq.connect(host="localhost", user="root", passwd="123456", database="preetha")
    cur = con.cursor()
    bill_id = random.randint(1000, 9999)
    query = "select accid from accounts where phno={}".format(ph)
    cur.execute(query)
    res1 = cur.fetchall()
    query1 = "select phno from billing where phno={}".format(ph)
    cur.execute(query1)
    res = cur.fetchall()
    if res == []:
        query2 = "insert into billing(phno, accid, billno) values({}, {}, {})".format(ph, res1[0][0], bill_id);
        cur.execute(query2)
    query4 = "select phno from payment where phno={}".format(ph)
    cur.execute(query4)
    res = cur.fetchall()
    if res == []:
        query4 = "insert into payment(phno, accid) values({}, {})".format(ph, res1[0][0]);
        cur.execute(query4)
    query3 = "select phno, accid, amt_generated, status from billing where phno={}".format(ph)
    cur.execute(query3)
    res = cur.fetchall()
    if res==[]:
        print("\nCustomer doesn't Exist....")
    else:
        calls = int (input("Enter no. of calls: "))
        bill = 0
        if calls>150:
            bill = bill + (calls-150)*3 + 50*1.5
        elif 100<calls<=150:
            bill = bill + (calls-100)*2.5 + 50*1.5
        elif 50<calls<=100:
            bill = bill + (calls-50)*1.5

        if res[0][3]!="Paid":
            old_bill = res[0][2]
        else:
            old_bill=0
        print("\n\t\t\tBilling")
        print("\t\t\t--------\n")
        print("\n\t\tPending Bill Amount", old_bill)
        print("\n\t\tNew Bill Amount", bill)
        print("\t\t--------------------")
        print("\t\tTotal Bill Amount ", bill+old_bill)
        print("\t\t--------------------")
        ch = input("Press Y to Pay Bill Now or Any other key to Pay later: ")
        if ch in ['Y', 'y']:
            query = "update billing set calls={}, amt_generated={}, status='Paid' where phno={};". format(calls, bill+old_bill, ph)
            cur.execute(query)
            con.commit()
            print("\nSuccessfully Paid the Bill!")
            query1 = "update payment set amt_payed = {} where phno={}".format(bill+old_bill, ph)
            cur.execute(query1)
            con.commit()
        else:
            query = "update billing set calls={}, amt_generated= {}, Status ='Un-Paid' where phno={}".format(calls, bill + old_bill, ph)
            cur.execute(query)
            con.commit()
            print("\nPlease make payment as soon as possible")
        con.close()


def remove():
    ph = input("Enter your phone number :  ")
    con = mq.connect(host="localhost", user="root", passwd="123456", database="preetha")
    cur = con.cursor()
    query = "select * from cust where phno={}".format(ph)
    cur.execute(query)
    res = cur.fetchall()
    if res == []:
        print("\n Customer doesn't Exist...\n")
        print("--------------------------------------------------------------------")
    else:
        ch = input("Are you sure to delete customer...Y/N :")
    if ch in ['y', 'Y']:
        query4 = "delete from payment where phno={}".format(ph)
        cur.execute(query4)
        query3 = "delete from billing where phno={}".format(ph)
        cur.execute(query3)
        query2 = "delete from accounts where phno={}".format(ph)
        cur.execute(query2)
        query1 = "delete from cust where phno={}".format (ph)
        cur.execute(query1)
        con.commit()
        print("\n\t\t----------------------------------------------------------")
        print("\t\t\t\t !!! SUCCESSFULLY DELETED CUSTOMER DATA !!!")
        print("\t\t----------------------------------------------------------\n")
    else:
        print("No changes made in your database\n")
        print("----------------------------------------------------------------")
        con.close()


def helping():
    print ("\n\t\t\t\t\t =====")
    print ("\t\t\t\t\t Help")
    print ("\t\t\t\t\t =====\n\n")
    print ("This is how our billing system works :")
    print ("1. Your First call is FREE!")
    print ("2. 50-100 calls costs 1.5 Rs per call")
    print ("3. 101-150 calls costs 2.5 Rs per call")
    print ("4. Above 10 calls are 3 Rs per call")
    print ("\nHave a nice day!")


while True:
    menu()
    ch = int(input("\nEnter your choice :  "))
    if ch == 1:
        register()
    elif ch == 2:
        search()
    elif ch == 3:
        modify()
    elif ch == 4:
        billing()
    elif ch == 5:
        remove()
    elif ch == 6:
        helping()
    elif ch == 7:
        exit()
    else:
        print("Please choose correct choice and try again...")

    ch = int(input("\n\n Please type '0' to continue.... Any other key to exit : "))
    if ch != 0:
        break
