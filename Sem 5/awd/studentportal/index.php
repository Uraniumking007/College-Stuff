<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home</title>
</head>
<style>
    body {
        background-color: #f1f1f1;
        height: 100vh;
        width: 100vw;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        gap: 20px;
    }
    table,
    td,
    th {
        border: 1px solid black;
    }

</style>
<body>
    List Of Students
    <?php
    include 'db.php';
    $sql = "SELECT * FROM students";
    $result = mysqli_query($connect, $sql);
    echo $result->num_rows;
    if ($result) {

    ?>
        <table>
            <tr>
            <td>
                Name
            </td>
            <td>
                Department
            </td>
            <td>
                Gender
            </td>
            </tr>
            <tr>
                    <?php
                    while ($row = mysqli_fetch_assoc($result)) {?>
                    
                <td><?php echo $row['name'] . "<br>";?></td>
                <td>
                    <?php
                        echo $row['department'] . "<br>";
                    ?>
                </td>
                <td>
                    <?php
                        echo $row["gender"] . "<br>";
                    ?>
                </td>
            </tr>
    <?php
    } ?>
        </table>
    <?php
    }?>
    <a href="./registration">
        <button>Register New Student</button>
    </a>
</body>

</html>