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
<td><img src="pics/pengmix.gif" height="50"></td>
<td valign="center">
<font size="+2"> PenguinMixer - an Open Source Bitcoin Mixer</font></td>
</tr></table>
<p>
<a href="index.html">Home</a> | <a href="checkmix.php">Check Mix</a> 
</p>

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

// Connection to bitcoind service. Settings must match bitcoin.conf file.
$rpcurl = "http://" . $rpcusername . ":" . $rpcpassword .
          "@127.0.0.1:" . $rpcport . "/";
$bitcoin_rpc = new jsonRPCClient($rpcurl);

// Connection to database. 
$conn = new PDO("mysql:host=$dbhost;dbname=$dbname",
                $dbusername, $dbpassword);


// This function is used to validate a bitcoin address.
function validateBitcoinAddress($bitcoin_rpc, $conn, $address, $address_name)
{
    // Make sure length is <= maximum allowed bitcoin address length of 35
    if (strlen($address) > 35)
    {
        echo "Error! Your bitcoin $address_name is too long. ";
        echo "Please go back and fix it. ";
        return false;
    }
    // Make sure the address contains only allowable BASE58 characters.
    $matchpattern = "@^[1-9A-HJ-NP-Za-km-z]+$@";
    if (!preg_match($matchpattern, $address))
    {
        echo "Error! Your bitcoin $address_name has invalid characters. ";
        echo "Please go back and fix it. ";
        return false;
    }

    // Check that address format is valid.
    $is_address_valid = $bitcoin_rpc->validateaddress($address);
    if (!$is_address_valid['isvalid'])
    {
        echo "Error! You entered an invalid bitcoin $address_name. ";
        echo "Please go back and fix it. ";
        return false;
    }

    // Check that the address is not already in the mixer database as
    // an input addresss.
    $query = "SELECT * FROM accounts " .
             "WHERE input_address =:address";
    $statement = $conn->prepare($query);
    $statement->bindParam(':address', $address);
    $statement->execute();
    $rowcount = $statement->rowCount();
    if ($rowcount <> 0)
    {
        echo "Error! Bitcoin $address_name already exists in the mixer. ";
        echo "Please go back and enter a different address. ";
        return false;
    }

    // If all checks pass, return true.
    return true;
}

// This function inserts an output address into the mixer database.
// We made a function for this since we need to do this up to 5 times.
function insertOutputAddress($conn, $input_address, $output_address)
{
    $query = "insert into output_addresses " .
             "(account_id, output_address) " .
             "values ((select account_id from accounts where " .
             "input_address = :input_address), :output_address)";
    $statement = $conn->prepare($query);
    $statement->bindParam(':input_address', $input_address);
    $statement->bindParam(':output_address', $output_address);
    $statement->execute();
    $rowcount = $statement->rowCount();
    if ($rowcount <> 1)
    {
       echo "Error! The server had a problem. Please report error code 3.";
       return false;
    }
    return true;
}


// Validate the form input.


// Validate the bitcoin addresses the user entered.
// Address 1 is required, but addresses 2-5 are optional.


// Address 1: //////////////////////////////////////////////

// First, make sure the post variable exists.
if (!isset($_POST['output_address_1']))
{
    echo "Error! You didn't enter anything for bitcoin address 1. ";
    echo "Please go back and fix it.";
    exit(1);
}

// Then, make sure it is a valid bitcoin address.
$output_address_1 = $_POST['output_address_1'];
if (!validateBitcoinAddress($bitcoin_rpc, $conn, $output_address_1,
    "output address 1"))
{
    exit(1);
}


// Addresses 2-5: Can be missing/blank, but if not missing/blank
// they must be valid.
// Also, the user can't put the same address into two or more of the
// text boxes.

// Address 2: //////////////////////////////////////////////

if (isset($_POST['output_address_2']))
{
    if ($_POST['output_address_2'] != "")
    {
        $output_address_2 = $_POST['output_address_2'];
        if ($output_address_2 == $output_address_1)
        {
            echo "Error! You entered one or more duplicate addresses. ";
            echo "Please go back and fix this.";
            exit(1);
        }
        if (!validateBitcoinAddress($bitcoin_rpc, $conn, $output_address_2,
            "output address 2"))
        {
            exit(1);
        }
    }
}

// Address 3: //////////////////////////////////////////////

if (isset($_POST['output_address_3']))
{
    if ($_POST['output_address_3'] != "")
    {
        $output_address_3 = $_POST['output_address_3'];
        if ($output_address_3 == $output_address_2 ||
            $output_address_3 == $output_address_1)
        {
            echo "Error! You entered one or more duplicate addresses. ";
            echo "Please go back and fix this.";
            exit(1);
        }
        if (!validateBitcoinAddress($bitcoin_rpc, $conn, $output_address_3,
            "output address 3"))
        {
            exit(1);
        }
    }
}

// Address 4: //////////////////////////////////////////////

if (isset($_POST['output_address_4']))
{
    if ($_POST['output_address_4'] != "")
    {
        $output_address_4 = $_POST['output_address_4'];
        if ($output_address_4 == $output_address_3 ||
            $output_address_4 == $output_address_2 ||
            $output_address_4 == $output_address_1)
        {
            echo "Error! You entered one or more duplicate addresses. ";
            echo "Please go back and fix this.";
            exit(1);
        }
        if (!validateBitcoinAddress($bitcoin_rpc, $conn, $output_address_4,
            "output address 4"))
        {
            exit(1);
        }
    }
}

// Address 5: //////////////////////////////////////////////

if (isset($_POST['output_address_5']))
{
    if ($_POST['output_address_5'] != "")
    {
        $output_address_5 = $_POST['output_address_5'];
        if ($output_address_5 == $output_address_4 ||
            $output_address_5 == $output_address_3 ||
            $output_address_5 == $output_address_2 ||
            $output_address_5 == $output_address_1)
        {
            echo "Error! You entered one or more duplicate addresses. ";
            echo "Please go back and fix this.";
            exit(1);
        }
        if (!validateBitcoinAddress($bitcoin_rpc, $conn, $output_address_5,
            "output address 5"))
        {
            exit(1);
        }
    }
}

// If we reach here, then we've successfully validated the user-entered
// output addresses.


// Validate a valid delay option was enetered.

// First, make sure the post variable exists.
if (!isset($_POST['delay']))
{
    echo "Error! You did not enter a delay option. ";
    echo "Please go back and fix it.";
    exit(1);
}

// Then make sure a valid option was enetered.
$delay = $_POST['delay'];
if ($delay <> "fast" && $delay <> "slow")
{
    echo "You entered an invalid delay option. ";
    echo "Please go back and fix it.";
    exit(1);
}


// Generate a new input address for user to send his bitcoins to.
$input_address = $bitcoin_rpc->getnewaddress();
// Make sure the generated input address is valid.
// This should always be the case except if we have a weird bug.
if (!validateBitcoinAddress($bitcoin_rpc, $conn, $input_address,
    "generated input address"))
{
    echo "Please report error code 1.";
    exit(1);
}

// Generate a random number of confirmations that are required for the
// user's input payment before he is sent payment back.
// Each confirmation takes about 10 minutes.
if ($delay == "fast")
{
    $confirmations = random_int(2,5);
}
else
{
    $confirmations = random_int(6,24);
}

// Generate a secret mixing key, which is a random string displayed
// to the user when setting up a mix. The user would need to supply
// this when contacting the support e-mail address if he has a question
// or problem with his mix.
$secret_mixing_key = bin2hex(random_bytes(32));

// Insert a new account into the account table.
$query = "insert into accounts " .
         "  (input_address, required_confirmations, secret_mixing_key) " .
         "   values (:input_address, :confirmations, :secret_mixing_key)";
$statement = $conn->prepare($query);
$statement->bindParam(':input_address', $input_address);
$statement->bindParam(':confirmations', $confirmations);
$statement->bindParam(':secret_mixing_key', $secret_mixing_key);
$statement->execute();
$rowcount = $statement->rowCount();
if ($rowcount <> 1)
{
    echo "Error! The server had a problem. Please report error code 2.";
    exit(1);
}

// This keeps track of how many output addresses were added so we can
// tell the user what their minimum input amount is
// (0.02 * number of output addresses).
$number_of_output_addresses_inserted = 0;

// First, insert the user's first (required) output addresses into
// the output address table.
if (!insertOutputAddress($conn, $input_address, $output_address_1))
{
    exit(1);
}
$number_of_output_addresses_inserted = $number_of_output_addresses_inserted + 1;

// Then insert any additional output addresses if the user has entered valid
// values.
// Note that if $output_address_X is set, then it means that we have already
// attempted to validate the value in that variable. If the validation failed,
// then the PHP code would have exited before now, which prevents us from
// entering an invalid address into the database.

if(isset($output_address_2))
{
    if (!insertOutputAddress($conn, $input_address, $output_address_2))
    {
        exit(1);
    }
    $number_of_output_addresses_inserted =
        $number_of_output_addresses_inserted + 1;
}
if(isset($output_address_3))
{
    if (!insertOutputAddress($conn, $input_address, $output_address_3))
    {
        exit(1);
    }
    $number_of_output_addresses_inserted =
        $number_of_output_addresses_inserted + 1;
}
if(isset($output_address_4))
{
    if (!insertOutputAddress($conn, $input_address, $output_address_4))
    {
        exit(1);
    }
    $number_of_output_addresses_inserted =
        $number_of_output_addresses_inserted + 1;
}
if(isset($output_address_5))
{
    if (!insertOutputAddress($conn, $input_address, $output_address_5))
    {
        exit(1);
    }
    $number_of_output_addresses_inserted =
        $number_of_output_addresses_inserted + 1;
}

// Calculate minimum payment based on number of output addresses specified.
$minimum_payment = 0.02 * $number_of_output_addresses_inserted;

// If everything worked, show the user a confirmation screen.

echo "<p><i><b>Warning</b>: Hitting the Refresh button on this page is ";
echo "<b>not</b> how to check your mix status. If you hit Refresh you ";
echo "will create a new mix. If you want to check your mix status, copy ";
echo "the secret mixing key below into your clipboard, then go to the ";
echo "<a href='checkmix.php'>Check Mix</a> screen and enter your secret ";
echo "mixing key there.</i></p>";

echo "<h3>Now You're Ready to Mix!</h3>";
echo "Your output address and payment delay preferences have been stored ";
echo " in the mixer.<br><br>";

echo "Send your funds into this address: <br><br>";
echo "<font style='BACKGROUND-COLOR: white'>$input_address</font>";
echo "<br><br>";

echo "When your input payment has ";
echo "<b>$confirmations</b> confirmations the mixer will schedule ";
echo "your output payments. *<br><br>";

echo "<i> * This value was set randomly when you created your mix. If ";
echo "you selected a fast payback, a number from 2-5 was chosen. If you ";
echo "selected a slow payback, a number from 6-24 was chosen.</i><br><br>";

echo "This is your secret mixing key: <br><br>";
echo "<font style='BACKGROUND-COLOR: white'>$secret_mixing_key</font>";
echo "<br><br>";
echo "Make a note of this string because if you want to ";
echo "<a href='checkmix.php'>check your mix status</a> or ";
echo "<a href='contact.html'>contact</a> support with a question about your ";
echo "mix you will need to provide it.";

echo "<h3>Mixing Rules:</h3>";
echo "<ol><li>Since you specified $number_of_output_addresses_inserted ";
echo "output address(es) your minimum payment is <b>$minimum_payment</b>";
echo " btc.</li>";
echo "<li>Maximum payment: <b>4.0 btc</b> (do not send in more than this).";
echo "</li>";
echo "<li>You have up to <b>24 hours</b> to send in your payment.</li></ol>";
echo "<font color='red'>Failure to follow these rules will result in ";
echo "lost bitcoins!</font>";

echo "<br><br><b>Important Note:</b><br><br>";
echo "If you specified more than one output address, your payment will be ";
echo "sent to you in <b>separate</b> transactions for each output address, ";
echo "<b>with a delay</b> between each payment.";

?>



</body>
</html>


