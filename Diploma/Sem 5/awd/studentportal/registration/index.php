<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registration</title>
</head>

<body>
    <form method="post" action="./register.php  ">
        <table>
            <tr>
                <td>Name:</td>
                <td>
                    <input type="text" name="name">
                </td>
            </tr>
            <tr>
                <td>
                    Department:
                </td>
                <td>
                    <input type="text" name="department">
                </td>
            </tr>
            <tr>
                <td>
                    Gender
                </td>
                <td>
                    <input type="radio" name="gender" value="male">Male
                    <input type="radio" name="gender" value="female">Female
                </td>
            </tr>
            <tr>
                <td>
                    <button type="submit">Save</button>
                </td>
                <td>
                    <button type="reset">Reset</button>
                </td>
            </tr>
        </table>
    </form>
</body>

</html>