#!/usr/bin/python
# -*- coding: utf-8 -*-

# This python script should be running whenever the mixer web site is live.
# If you stop it for a long period and then start it up, it will have a lot
# of transactions to catch up on at once, which might look weird.

# License: Do whatever you want with this code.

# Needed to call bitcoin functions
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
# Needed to connect to MySQL database
import MySQLdb
# Needed for getting current time, implementing waiting, comparing dates
# and times, adding dates/times, etc.
import time
from datetime import datetime, timedelta
# Needed so we can do random mixing fees, random payment splitting, and
# random time delays.
from random import SystemRandom
random = SystemRandom()

# Constants
# !!! CHANGE THESE! USE LONG RANDOM PASSWORDS !!!

DATABASE_NAME = "db"
DATABASE_HOST = "localhost"
DATABASE_USERNAME = "vicomtech"
DATABASE_PASSWORD = "vicomtech"
SERVICE_USERNAME = "uab"
SERVICE_PASSWORD = "uabpassword"
SERVICE_PORT_NUMBER = "18332"

LOG_FILE_PREFIX = "mixer-log-"

# !!! YOU MAY CHANGE THESE IF YOU WANT DIFFERENT SETTINGS FOR YOUR MIXER !!!

# How many seconds to wait between each loop iteration
LOOP_ITERATION_WAIT_SECONDS = 60

# A user must send in at least this amount * the number of output addresses
# he specifies. So if he specifies 3 output addresses he must send in at
# least MIN_USER_PAYMENT_PER_OUTPUT_ADDRESS * 3. If he sends in less than
# this, no money will be returned.
MIN_USER_PAYMENT_PER_OUTPUT_ADDRESS = 0.02
# Maximum amount to mix per user. If a user sends in more than this amount,
# the mixer will keep the amount over this limit. The number of output
# addresses does not affect this maximum).
# NOTE: This is also the amount you must "seed" the mixer wallet with
# (utilizing the master account row (account_id =1) in the accounts table)
# before opening it for business.
MAX_USER_PAYMENT = 4.0

# When we mix money we take a fee that is randomized between these numbers.
MIN_MIX_FEE = 0.005
MAX_MIX_FEE = 0.01

# This controls how long a user has to send in his payments before his account
# goes inactive (meaning no more payments into the account are allowed).
DAYS_UNTIL_ACCOUNT_INACTIVE = 3
# This controls how long after an account is created should all information
# for that account be wiped.
# You should also delete old log files at the same interval.
DAYS_UNTIL_ACCOUNT_DELETED = 7

# This function write to the log file.
def log(text):
    with open(LOG_FILE_NAME, "a") as logfile:
        logfile.write(text + "\n")

# This is the infinite loop inside which the program runs. It will not stop
# unless it is killed or exits with an unhandled error.
while True:

    # Write each day's log to a separate file so that we can easily delete
    # old log files for user privacy.
    LOG_FILE_NAME = LOG_FILE_PREFIX + time.strftime('%Y-%m-%d')

    log ("Loop time: " + str(datetime.today()))

    # Connection to bitcoind service. Settings must match bitcoin.conf file.
    rpc = AuthServiceProxy("http://%s:%s@127.0.0.1:%s" %
                       (SERVICE_USERNAME, SERVICE_PASSWORD,
                        SERVICE_PORT_NUMBER))

    # Connection to database.
    db = MySQLdb.connect(host=DATABASE_HOST, db=DATABASE_NAME,
                         user=DATABASE_USERNAME, passwd=DATABASE_PASSWORD)

    # Get a list of all active accounts except the master account (the master
    # account is a special account used to put the initial seed money into
    # the mixer). The account_id of the master is always 1.
    account_list = db.cursor()
    account_list.execute("SELECT account_id, input_address, " +
                         "       required_confirmations, " +
                         "       active_flag, created_datetime " +
                         "FROM accounts " +
                         "WHERE account_id <> 1 " +
                         "ORDER BY account_id")


    # Get list of all wallet addresses that have received payments from users.
    # Even though we are showing all payments, even unconfirmed ones, we
    # won't actually pay out to a user until all payments he has made to his
    # input address have the required number of confirmations set for his
    # account in the account table.
    
    inputs = rpc.listreceivedbyaddress(0)

    # Go through all accounts in database (EXCEPT master account).
    for account_row in account_list.fetchall():

        # account unique identifier
        current_account_id = account_row[0]
        ## The address the user sends his money into
        current_input_address = account_row[1]
        # How many confirmations are needed on input money before output
        # money is sent.
        current_required_confirmations = account_row[2]
        # If the account is active (able to send payments out).
        current_active_flag = account_row[3]

        # When was the account created?
        current_account_created_datetime = account_row[4]
        # The user's account will be switched to inactive a certain number
        # of days after he creates it (assuming no payments are pending).
        # Users are warned on web page they only have a certain time limit
        # to send in their payments.
        current_account_inactive_datetime = (
            current_account_created_datetime +
            timedelta(days=DAYS_UNTIL_ACCOUNT_INACTIVE))
        # All records for the user's account will be deleted a certain number
        # of days after he creates it.
        current_account_delete_datetime =(
            current_account_created_datetime +
            timedelta(days=DAYS_UNTIL_ACCOUNT_DELETED))

        # If current account is old enough to delete, then do so.
        # We do this to protect user privacy
        if (current_account_delete_datetime < datetime.today()):
            log ("Account " + str(current_account_id) +
                 " is old enough to delete.")
            # Due to foreign keys in database we need to delete information
            # in a specific order.
            args = (current_account_id,)
            delete = db.cursor()
            query = ("DELETE p "
                     "FROM payments p " +
                     "INNER JOIN output_addresses o " +
                     "ON p.output_address_id = " +
                     "   o.output_address_id " +
                     "WHERE o.account_id = %s ")
            delete.execute(query, args)
            query = ("DELETE FROM output_addresses " +
                     "WHERE account_id = %s")
            delete.execute(query, args)
            query = ("DELETE FROM accounts " +
                     "WHERE account_id = %s")
            delete.execute(query, args)
            db.commit()
            log ("Account deleted.")

            # Do not perform any more actions for this account since it's
            # now deleted. Continue to next account in the loop.
            continue

        # If the current account is ALREADY inactive (but was not old
        # enough to delete), also do not perform any more actions for
        # this account. Continue to next account in the loop.
        if (current_active_flag == "N"):
            continue

        # Check if account is old enough to switch to inactive status.
        if (current_account_inactive_datetime < datetime.today()):
            log ("Account " + str(current_account_id) +
                 " is old enough to make inactive.")
            update_to_inactive = db.cursor()
            query = ("UPDATE accounts " +
                     "set active_flag = 'N' " +
                     "WHERE account_id = %s")
            args = (current_account_id,)
            update_to_inactive.execute(query, args)
            db.commit()
            log ("Account set to inactive.")
            # Since we've just made this account inactive, we don't need
            # to do anything else with it, so continue to next account
            # in the loop
            continue

        # If we reached here, then we have an active account and we can
        # do the normal stuff.

        log ("account id: " + str(current_account_id))
        log ("input address: " + current_input_address)
        log ("required confirmations for this account: " +
               str(current_required_confirmations))
        log ("account created: " + str(current_account_created_datetime))
        log ("account goes inactive after: " +
               str(current_account_inactive_datetime))
        log ("account will be deleted after: " +
               str(current_account_delete_datetime))

        # Loop through all the input addresses in the wallet looking for the
        # one that matches the current account's input address.
        for current_input in inputs:
            ## If match and we have enough confirmations of the money
            ## sent in...
            if (current_input_address == current_input['address'] and
                current_input['confirmations'] >=
                current_required_confirmations):

                current_input_amount = current_input['amount']
                log ("total user has sent in: " + str(current_input_amount))

                # We will only pay a maximum of X btc to each user, so
                # cap total payment at X btc, even if the user sent in
                # more (which the web site tells them NOT to do).
                if current_input_amount > MAX_USER_PAYMENT:
                    current_input_amount = MAX_USER_PAYMENT
                    log ("Max payment per user is " + str(MAX_USER_PAYMENT))

                # Check the total amount we've scheduled to pay out but have
                # not paid out yet.
                payments_scheduled = db.cursor()
                query = ("SELECT IfNull(SUM(p.amount_gross),0) " +
                         "FROM output_addresses o " +
                         "INNER JOIN payments p " +
                         "ON o.output_address_id = " +
                         "   p.output_address_id " +
                         "WHERE o.account_id = %s " +
                         "AND p.transaction_id IS NULL")
                args = (current_account_id,)
                payments_scheduled.execute(query, args)
                payments_scheduled_row = payments_scheduled.fetchone()
                current_scheduled_payments = float(payments_scheduled_row[0])
                log ("total payments scheduled but not sent: " +
                       str(current_scheduled_payments))

                # Check the total amount we've paid out so far.
                payments_sent = db.cursor()
                query = ("SELECT IfNull(SUM(p.amount_gross),0) "
                         "FROM output_addresses o " +
                         "INNER JOIN payments p " +
                         "ON o.output_address_id = " +
                         "   p.output_address_id " +
                         "WHERE o.account_id = %s " +
                         "AND p.transaction_id IS NOT NULL")
                args = (current_account_id,)
                payments_sent.execute(query, args)
                payments_sent_row = payments_sent.fetchone()
                current_sent_payments = float(payments_sent_row[0])
                log ("total payments sent: " +
                       str(current_sent_payments))

                current_total_payments = round((current_scheduled_payments +
                                                current_sent_payments),8)
                log ("grand total payments: " + str(current_total_payments))

                # Amount due is the total amount the user has sent in minus
                # the total amount we've scheduled payments for or sent
                # payments for.
                current_amount_due = (float(current_input_amount) -
                                      current_total_payments)
                log ("amount due: " + str(current_amount_due))

                # Now we need to loop through all the output addresses the
                # user has and split his amount due up to those different
                # addresses.
                output_addresses = db.cursor()
                query = ("SELECT output_address_id, output_address " +
                         "FROM output_addresses "
                         "WHERE account_id = %s " +
                         "ORDER BY output_address_id")
                args = (current_account_id,)
                output_addresses.execute(query, args)
                number_of_output_addresses = output_addresses.rowcount
                log ("this account has " + str(number_of_output_addresses) +
                       " output addresses")

                # Figure out the minimum payment amount for this account.
                # This is calculated by multiplying the minimum payment
                # amount per output address by the number of output addresses
                # this account has.
                current_minimum_payment = (
                    (MIN_USER_PAYMENT_PER_OUTPUT_ADDRESS *
                     number_of_output_addresses))
                log ("Minimum payment for this account is " +
                       str(current_minimum_payment))

                # If the amount due is greater than or equal to the minimum
                # payment for this account, then schedule payment(s).
                if (current_amount_due >= round(current_minimum_payment,8)):

                    # These variables will be modified as we go through
                    # the loop of all output addresses.
                    current_address_number = 1
                    current_payment_datetime = datetime.today()
                    created_datetime = current_payment_datetime

                    total_new_payments_remaining = current_amount_due

                    # Loop through all of this account's output addresses.
                    for output_address_row in output_addresses.fetchall():

                        log ("current output address number: " +
                               str(current_address_number))
                        current_output_address_id = output_address_row[0]
                        log ("current output address id: " +
                               str(current_output_address_id))
                        current_output_address = output_address_row[1]
                        log ("current output address: " +
                               current_output_address)

                        # Calculate a payment for the current output address.

                        # Complicated stuff:
                        # If we are not on the last output address, choose
                        # a random payment amount for the current address
                        # between the min payment amount and (the amount left
                        # to be paid minus the (min payment * the number of
                        # addresses left to be paid)).
                        # So for example if the minimum to pay is 0.01 and we
                        # need to pay 0.5 btc total and we are on address
                        # 1 of 3, then we pick a random payment amount between
                        # 0.01 and 0.48 btc.
                        # Let's say we choose 0.17 for address 1.
                        # Now, when we're on address 2, we choose an amount
                        # between 0.01 and 0.32.
                        # Let's say we choose 0.05 for address 2.
                        # Then, on the last output address, we just pay
                        # the remaining balance (which would be 0.28 in
                        # this example).
                        if (current_address_number <
                          number_of_output_addresses):
                            current_gross_amount = (
                             round(random.uniform(
                                 MIN_USER_PAYMENT_PER_OUTPUT_ADDRESS,
                                 (total_new_payments_remaining -
                                  (MIN_USER_PAYMENT_PER_OUTPUT_ADDRESS *
                                   (number_of_output_addresses -
                                    current_address_number)))),8))

                        # If we are on the last output address, set payment to
                        # however much remains to be paid after setting the
                        # payments for the prior output addresses.
                        else:
                            current_gross_amount = (
                                round(total_new_payments_remaining,8))

                        # Now we need to select a random fee between our min
                        # and max and subract this fee from the payment to
                        # the user.
                        current_mix_fee = round(random.uniform(MIN_MIX_FEE,
                                                               MAX_MIX_FEE),8)

                        # Set the pay amount to the amount due minus the fee.
                        current_net_amount = (round(current_gross_amount *
                                                    (1.0 - current_mix_fee),8))

                        # Calculate payment datetime for this output address

                        # If we are not on the first output address, add a
                        # random number of seconds to delay payment to this
                        # address.
                        if (current_address_number > 1):

                            # Base the delay time range on the account's
                            # number of required confirmations

                            min_delay = current_required_confirmations * 300
                            max_delay = 2 * min_delay
                            current_payment_delay = random.randint(min_delay,
                                                                   max_delay)
                            current_payment_datetime = (
                                created_datetime +
                                timedelta(seconds=current_payment_delay))

                        # Insert this scheduled payment into the database
                        query = ("INSERT INTO payments " +
                                 "(output_address_id, amount_gross, " +
                                 "amount_net, created_datetime,payment_datetime) " +
                                 "VALUES(%s,%s,%s,%s,%s)")
                        args = (current_output_address_id,
                                current_gross_amount, current_net_amount,
                                created_datetime,
                                current_payment_datetime)
                        insert = db.cursor()
                        insert.execute(query, args)
                        db.commit()

                        log ("Payment amount of " + str(current_gross_amount) +
                               " gross, " + str(current_net_amount) +
                               " net scheduled to this output address on " +
                               str(current_payment_datetime))

                        # Keep track of which address number we are on for next
                        # loop iteration.
                        current_address_number = current_address_number + 1

                        # Keep track of how much we've scheduled and remains to
                        # be scheduled thus far
                        total_new_payments_remaining = (
                            total_new_payments_remaining-current_gross_amount)


        # Now check if it's time to process any scheduled payments for this
        # account. Get a list of all unsent payments for this account.
        payments_to_execute = db.cursor()
        query = ("SELECT o.output_address, p.payment_id, p.amount_gross, " +
                 "       p.amount_net, p.payment_datetime " +
                 "FROM output_addresses o " +
                 "INNER JOIN payments p " +
                  "ON o.output_address_id = " +
                  "   p.output_address_id " +
                  "WHERE o.account_id = %s " +
                  "AND p.transaction_id IS NULL")
        args = (current_account_id,)
        payments_to_execute.execute(query, args)

        # Loop through all unsent payments.
        for payment_row in payments_to_execute.fetchall():

            # The address this payment should be sent to
            current_output_address = payment_row[0]
            # payment unique identifier
            current_payment_id = payment_row[1]
            # Gross amount (without mixing fee subracted)
            current_gross_amount = float(payment_row[2])
            # Net amount (actual payment amount)
            current_net_amount = float(payment_row[3])
            # When the payment should be processed
            current_payment_datetime = payment_row[4]

            # If the payment processing datetime is less than or equal
            # to the current datetime, then send payment.
            if (current_payment_datetime <= datetime.today()):

                log ("Payment " + str(current_payment_id) + " needs sending.")

                # Lock the funds this user sent in, so that we don't
                # use the unspent money in his input address to send
                # back to him (that would defeat the idea of mixing).

                # This array holds the unspent payments to lock.
                unspent_output_ids = []

                # Get list of all unspent outputs. Unspent outputs are funds
                # that have been sent into the mixer's wallet but have not been
                # paid out yet. We keep track of this so we can lock a user's
                # input money when paying out that user, so that users are
                # guaranteed to get different bitcoins than the ones they put
                # in. Min confirmations is set to 0 because we want to lock all
                # payments a particular user has put in, even unconfirmed ones.
                unspent_outputs = rpc.listunspent(0)

                # Get a list of wallet address groupings. If the user's input
                # payment has already been used to pay a different user then
                # the change from that transaction will be in a change
                # address. We need to find any wallet addresses in the same
                # group as user's input address so that we can lock not only
                # unspent outputs in the user's input address, but also
                # unspent outputs in change addresses that came from
                # transactions that used the original unspent outputs in the
                # user's input address.
                address_groups = rpc.listaddressgroupings()

                # Go through all the address groups, looking for the one that
                # contains the user's input address.
                for current_address_group in address_groups:
                    # Go through all the addresses in the current group and add
                    # them to a list.
                    current_address_list = []
                    for current_address in current_address_group:
                        current_address_list.append(current_address[0])
                    # Check if the current address list contains the user's
                    # input addresss. If it does...
                    if (current_input_address in current_address_list):
                        # Go through all unspent outputs in wallet
                        for unspent_output in unspent_outputs:
                            unspent_output_address = unspent_output['address']
                            # If this output is in the current address list...
                            if (unspent_output_address in current_address_list):
                                # Append this output to array of outputs to lock.
                                current_trans_id = unspent_output['txid']
                                current_vout = unspent_output['vout']
                                current_unspent_id  = [{'txid': current_trans_id,
                                                        'vout': current_vout}]
                                unspent_output_ids = (unspent_output_ids +
                                                      current_unspent_id)
                # Now that we've found all the unspent outputs in the user's
                # input address and any related change addresses, lock them.
                rpc.lockunspent(False, unspent_output_ids)
                log ("locked unspent outputs:")
                log (str(unspent_output_ids))

                # Try to make the payment and record it in the database.
                try:

                    txid = rpc.sendtoaddress(current_output_address,
                                             current_net_amount)

                    query = ("UPDATE payments " +
                             "SET transaction_id = %s " +
                             "WHERE payment_id = %s")
                    args = (txid, current_payment_id)
                    insert = db.cursor()
                    insert.execute(query, args)
                    db.commit()
                    log("Sent payment id " + str(current_payment_id) +
                        " for " + str(current_gross_amount) +
                        " gross, " + str(current_net_amount) +
                        " net to output address " + current_output_address +
                        " at " + str(current_payment_datetime) +
                        " txid: " + txid)
                except JSONRPCException, e:
                    log (repr(e.error))

                # Unlock this user's money so it can be sent
                # to another user.
                rpc.lockunspent(True, unspent_output_ids)
                log ("unlocked unspent outputs:")
                log (str(unspent_output_ids))

    log("**********************************************************************")
    log("**********************************************************************")
    ## Wait specified interval and then run through the loop again
    time.sleep(LOOP_ITERATION_WAIT_SECONDS)

