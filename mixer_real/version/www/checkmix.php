<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html;charset=utf-8"/>
<title>
PenguinMixer - an Open Source Bitcoin Mixer
</title>
</head>
<body bgcolor="#DDFFDD">
<table><tr>
<td valign="center">
<font size="+2"> PenguinMixer - an Open Source Bitcoin Mixer</font></td>
</tr></table>
<p>
<a href="index.html">Home</a> | <b>Check Mix</b>
</p>
<p>
Enter your secret mixing key below and hit Submit to view your mix status.
Mixing information is only retained for <b>7 days</b>, so if
it's been longer than that your search won't work.
</p>

<form action="checkmix.php" method="post">

Secret mixing key:
<input type="text" name="mixing_key" size="64" maxlength="64">
<br><br>
<input type="submit" value="Submit">
</form>


<?php require_once 'jsonRPCClient.php';

// Connection settings...CHANGE THESE! USE LONG RANDOM PASSWORDS!!!

// NOTE: For increased security, create an include file (for example
// you could call it setup.php) and put it outside your web root
// directory. Put the below variable settings into that include file and
// include like this:
// include '../setup.php';

$dbname = "db";
$dbhost = "localhost";
$dbusername = "vicomtech";
$dbpassword = "vicomtech";
$rpcusername = "uab";
$rpcpassword = "uabpassword";
$rpcport = "18332";

// This is used to adjust the datetime values returned from the database
// into UTC time. Set this to the number of hours you need to add or
// subtract from your server's time zone to make it equal to UTC time.
// You can use either positive or negative integers.
// EXAMPLES:
// $server_offset_hours = 4;
// $server_offset_hours = -2;
$server_offset_hours = 0;

// Connection to bitcoind service. Settings must match bitcoin.conf file.
$rpcurl = "http://" . $rpcusername . ":" . $rpcpassword .
          "@127.0.0.1:" . $rpcport . "/";
$bitcoin_rpc = new jsonRPCClient($rpcurl);

// Connection to database.
$conn = new PDO("mysql:host=$dbhost;dbname=$dbname",
                $dbusername, $dbpassword);

// This function is used to adjust a datetime by a specified number of hours.
// Note that this will change the value in the variable that is passed
// into $input_datetime, so we don't need to return a value.
function adjustTimeByOffsetHours($input_datetime, $offset_hours)
{
    $offset_string = "PT" . abs($offset_hours) . "H";
    // If the offset is postive, then we need to add the hours.
    if ($offset_hours >= 0)
    {
        $input_datetime->add(new DateInterval($offset_string));
    }
    // If the offset is negative, then we need to subtract the hours.
    else
    {
        $input_datetime->sub(new DateInterval($offset_string));
    }
}

// If the user has entered a mixing key and clicked submit, then this
// form variable will be defined and we should search for the mixing key.
if (isset($_POST['mixing_key']))
{
    $mixing_key = $_POST['mixing_key'];

    // If the mixing key is not 64 characters, give an error and stop.
    if (strlen($mixing_key) <> 64)
    {
        echo "Error! Your secret mixing key is the wrong length. ";
        echo "It should be 64 characters.";
        exit(1);
    }

    // If the mixing key contains invalid characters, give an error and stop.
    $matchpattern = "@^[0-9a-fA-F]+$@";
    if (!preg_match($matchpattern, $mixing_key))
    {
        echo "Error! Your secret mixing key has invalid characters. ";
        echo "Valid characters are 0-9 and a-f.";
        exit(1);
    }

    // Look up the mixing key in the account table.
    $query = "SELECT account_id, input_address, " .
             "required_confirmations, created_datetime " .
             "FROM accounts " .
             "WHERE secret_mixing_key =:mixing_key";
    $statement = $conn->prepare($query);
    $statement->bindParam(':mixing_key', $mixing_key);
    $statement->execute();
    $account_rowcount = $statement->rowCount();

    // If the mixing key isn't found, show an error.
    if ($account_rowcount == 0)
    {
        echo "Error! That secret mixing key was not found. ";
        echo "Please try again. ";
        exit(1);
    }

    // If we reach here, then we have found the mixing key in the database.

    // Set variables to hold values from account table.
    $account_result = $statement->fetch();
    $account_id = $account_result['account_id'];
    $input_address = $account_result['input_address'];
    $confirmations = $account_result['required_confirmations'];
    $created_datetime = new DateTime($account_result['created_datetime']);

    // Adjust created datetime into UTC based on server time zone.
    adjustTimeByOffsetHours($created_datetime, $server_offset_hours);
    $created_datetime_string = $created_datetime->format('Y-m-d H:i:s');

    // The deadline time for sending in an input payment is one day after
    // the mix was created.
    $deadline_datetime = $created_datetime->add(new DateInterval('P1D'));
    $deadline_datetime_string = $deadline_datetime->format('Y-m-d H:i:s');

    // This section shows information about the mix settings
    echo "<h3>Mix Information</h3>";
    echo "<table cellpadding=6>";
    echo "<tr><td><b>Secret Mixing Key</b></td>";
    echo "<td>$mixing_key</td></tr>";
    echo "<tr><td><b>Account Created *</b></td>";
    echo "<td>$created_datetime_string</td></tr>";
    echo "<tr><td><b>Input Payment Deadline *</b></td>";
    echo "<td>$deadline_datetime_string</td></tr>";
    echo "<tr><td><b>Required Confirmations **</b></td>";
    echo "<td>$confirmations</td></tr>";
    echo "<tr><td><b>Mixer Input Address</b></td>";
    echo "<td>$input_address</td></tr>";

    // Users can have up to 5 output addresses. We need to query the
    // output_addresses table to get the list of output addresses
    // for the user's account.
    $query = "SELECT output_address " .
             "FROM output_addresses " .
             "WHERE account_id =:account_id";
    $statement = $conn->prepare($query);
    $statement->bindParam(':account_id', $account_id);
    $statement->execute();
    $output_address_rowcount = $statement->rowCount();

    // If no output addresses are found for this account, show an error.
    // This should never happen, as at least one output address should be
    // created whenever a user creates a mix.
    if ($output_address_rowcount == 0)
    {
        echo "Error! No output addresses found! ";
        echo "This error should never happen. Please report it.";
        exit(1);
    }

    // If we found at least one output address...

    // Set the minimum payment to 0.02 multiplied by the number of
    // output addresses.
    $minimum_payment = 0.02 * $output_address_rowcount;

    // Get all rows of data from result set.
    $output_address_result = $statement->fetchAll();

    // Loop through all the output addresses for this account and show
    // them in the table.
    // Note that if we are on the first output address, we should show
    // a label in the first column.
    $is_first_row = true;
    foreach($output_address_result as $row)
    {
        $output_address = $row['output_address'];
        echo "<tr><td>";
        if ($is_first_row)
        {
            echo "<b>Output Address(es)</b>";
        }
        echo "</td><td>$output_address</td></tr>";
        // We are no longer on the first row, so set variable to false.
        $is_first_row = false;
    }

    // Information about min and max payments.
    echo "<tr><td><b>Minimum Payment</b></td>";
    echo "<td>$minimum_payment btc ";
    echo "(0.02 * number of output addresses you specified)</td></tr>";
    echo "<tr><td><b>Maximum Payment</b></td>";
    echo "<td>4.0 btc</td></tr>";
    echo "</table>";

    // Notes about data displayed in above table.
    echo "<br><i>* This is displayed in 24-hour UTC time.";
    echo "<br><br>** The required confirmations value was set randomly ";
    echo " when you created your mix. If you selected a fast payback, a ";
    echo " number from 2-5 was chosen. If you selected a slow payback, a ";
    echo " number from 6-24 was chosen. When your input payment has this ";
    echo " many confirmations the mixer will schedule your output ";
    echo " payment(s).</i>";

    // Input payment information

    // Go through all the addresses in the mixer's wallet looking for
    // the one that matches to the account's input address.
    // The parameters (0, true) mean to list wallet addresses that have
    // a minimum of 0 confirmations (in other words, any number of
    // confirmations) and true means to list wallet addresses even if
    // there have been no payments into them yet.
    $wallet_addresses = $bitcoin_rpc->listreceivedbyaddress(0, true);
    foreach($wallet_addresses as $wallet_address)
    {
        // When we find the account's input address...
        if ($wallet_address['address'] == $input_address)
        {
            $input_payment_amount = number_format($wallet_address['amount'],8);
            $input_payment_confirmations = $wallet_address['confirmations'];
            $input_payment_txids = $wallet_address['txids'];
        }
    }

    echo "<h3>Input Payment Information</h3>";

    // If the user has not sent in any input payments yet...
    if ($input_payment_amount == 0)
    {
        echo "No input payments found.";
    }
    else
    {
        echo "<table cellspacing=6>";
        echo "<tr><td><b>Amount</b></td>";
        echo "<td><b>Confirmations</b></td>";
        echo "<td><b>Transaction IDs</b></td></tr>";
        echo "<tr><td>$input_payment_amount</td>";
        echo "<td>$input_payment_confirmations</td>";
        echo "<td>";
        // It is possible that the user sent in more than one input
        // payment to the mixer input address. So there could be more
        // than one txid for an input address. So we need to loop through
        // and output all the txids for this input address.
        foreach ($input_payment_txids as $input_payment_txid)
        {
            echo $input_payment_txid;
            echo "<br>";
        }
        echo "</td></tr></table>";
        if ($input_payment_amount < Round($minimum_payment,8))
        {
            echo "<font color='red'>Warning! You have sent in less ";
            echo "than the required minimum of $minimum_payment btc ";
            echo "(0.02 * number of output addresses you specified). ";
            echo "You must send in enough to bring your total input ";
            echo "payment up to $minimum_payment if you want a ";
            echo "return payment.</font>";
        }
        if ($input_payment_amount > 4.0)
        {
            echo "<font color='red'>Warning! You have sent in over ";
            echo "the maximum allowed by the mixer! The mixer will ";
            echo "only return up to 4.0 btc. You need to ";
            echo "<a href='contact.html'>contact support</a> to get ";
            echo "your extra bitcoins back.</font>";
        }
    }

    // Information about payments sent or scheduled to be sent from mixer

    echo "<h3>Output Payment Information</h3>";

    // Look up the account id of the user and find payments for that
    // account (payments might not exist yet).
    $query = "SELECT o.output_address, p.amount_net, " .
             "p.transaction_id, p.payment_datetime " .
             "FROM accounts a inner join output_addresses o " .
             "ON a.account_id = o.account_id " .
             "INNER JOIN payments p " .
             "ON o.output_address_id = p.output_address_id " .
             "WHERE a.account_id =:account_id " .
             "ORDER BY p.payment_id";
    $statement = $conn->prepare($query);
    $statement->bindParam(':account_id', $account_id);
    $statement->execute();
    $payment_rowcount = $statement->rowCount();

    // If no records are returned, tell user there are no output payments yet.
    if ($payment_rowcount == 0)
    {
        echo "No output payments are scheduled yet.<br><br>";
    }
    // If there is at least one output payment scheduled...
    else
    {
        $payment_result = $statement->fetchAll();

        // Table header row
        echo "<table cellspacing=6>";
        echo "<tr><td><b>Output Address</b></td>";
        echo "<td><b>Amount</b></td>";
        echo "<td><b>Scheduled Datetime *</b></td>";
        echo "<td><b>Transaction ID</b></td></tr>";

        // Loop through all payments and add them to table.
        $payment_total = 0;
        foreach($payment_result as $row)
        {
            $output_address = $row['output_address'];
            $amount = $row['amount_net'];
            // Keep a running total of output payment.
            $payment_total = $payment_total + $amount;
            // Adjust payment datetime into UTC based on server time zone.
            $payment_datetime = new DateTime($row['payment_datetime']);
            adjustTimeByOffsetHours($payment_datetime, $server_offset_hours);
            $payment_datetime_string=$payment_datetime->format('Y-m-d H:i:s');

            // If the transaction id is blank, show "Not sent yet".
            if ($row['transaction_id'] == "")
            {
                $transaction_id = "Not sent yet";
            }
            else
            {
                $transaction_id = $row['transaction_id'];
            }

            // Output information to table.
            echo "<tr><td>$output_address</td>";
            echo "<td>$amount</td>";
            echo "<td>$payment_datetime_string</td>";
            echo "<td>$transaction_id</td></tr>";
        }

        // Calculate the mixing fee as:
        // input payment - total output payment
        $mix_fee = Round($input_payment_amount - $payment_total,8);
        // Calculate the mixing fee percentage as:
        // (mix fee / input payment) * 100
        $mix_fee_percent = Round(($mix_fee / $input_payment_amount) * 100,2);

        // Final summary information
        echo "<tr><td><b>Total</b></td>";
        echo "<td colspan=3><b>$payment_total</b></td></tr>";
        echo "<tr><td><b>Mixing Fee</b></td>";
        echo "<td colspan=3><b>$mix_fee</b></td></tr>";
        echo "<tr><td><b>Mixing Fee Percentage</b></td>";
        echo "<td colspan=3><b>$mix_fee_percent %</b></td></tr>";
        echo "</table>";
        echo "<br><i>* This is displayed in 24-hour UTC time.</i><br><br>";

    }// End of what to do if payments are found.

    echo "<b>Use your browser's refresh button to update this screen.</b>";
}
?>

</body>
</html>

