<html>
    <head>
        <title>CIS 322 REST-api example calls</title>
    </head>

    <body>
        <h1>Example API Calls</h1>
        <sub><em>App must be ran at least once to generate data from database</em></sub>
        
        
        <h2>List of Open Times</h2>
        <!--
        <ul>
            <?php
            /*
            //$csvfile = file_get_contents('http://laptop-service/listOpenOnly/csv');
            if (($handle = file_get_contents('http://laptop-service/listOpenOnly/csv')) !== FALSE) {
                while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
                    $num = count($data);
                    echo "<p> $num fields in line $row: <br /></p>\n";
                    $row++;
                    for ($c=0; $c < $num; $c++) {
                        echo $data[$c] . "<br />\n";
                    }
                }
            //fclose($handle);
            }*/
            ?>
        </ul>-->

        <?php
          //Create user
          $apiurl = "localhost:5001/api/register";
          $ch = curl_init();
          $username = "root";
          $password = "toor";

          // set options
          curl_setopt($ch, CURLOPT_URL, $url);
          curl_setopt($ch, CURLOPT_POST, true);
          curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
          curl_setopt($ch, CURLOPT_USERPWD, "$username:$password");
          curl_setopt($ch, CURLOPT_HTTPAUTH, CURLAUTH_BASIC);
          // grab URL and pass it to the browser
          $result = curl_exec($ch);
          $status_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);

          echo "<p>$result</p>";
          echo "<p>$status_code</p>";

          // close cURL resource, and free up system resources
          curl_close($ch);
          ?>
    </body>
</html>