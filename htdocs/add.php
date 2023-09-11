<html>
<body>
      <?php
      if(isset($_POST['num1']) && isset($_POST['num2']))
      {
            $num1 = $_POST['num1'];
            $num2 = $_POST['num2'];
            $sum = $num1+$num2;
            echo "The sum of $num1 and $num2 is $sum";
      }
      else
      {
            echo "Please enter two numbers";

      }
      ?>
</body>
</html>
