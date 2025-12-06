<!DOCTYPE html>
<html data-theme="synthwave">
<head>
    <title>@yield("title") - XMachines·</title>


    <!-- <link rel="stylesheet" href="/assets/jquery-ui/jquery-ui.min.css"> -->
    <!-- <link rel="stylesheet" href="/assets/jquery-ui/jquery-ui.structure.min.css"> -->
    <!-- <link rel="stylesheet" href="/assets/jquery-ui/jquery-ui.theme.min.css"> -->

    <script src="/assets/jquery/jquery-3.7.1.min.js"></script>
    <!-- <script src="/assets/jquery-ui/jquery-ui.min.js"></script> -->
    <script src="/assets/app.js"></script>


    <!-- UIkit CSS -->
    <!-- <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/uikit@3.25.1/dist/css/uikit.min.css" /> -->

    <!-- UIkit JS -->
    <!-- <script src="https://cdn.jsdelivr.net/npm/uikit@3.25.1/dist/js/uikit.min.js"></script> -->
    <!-- <script src="https://cdn.jsdelivr.net/npm/uikit@3.25.1/dist/js/uikit-icons.min.js"></script> -->


    <link href="https://cdn.jsdelivr.net/npm/flowbite@4.0.1/dist/flowbite.min.css" rel="stylesheet" />
    <script src="https://cdn.jsdelivr.net/npm/flowbite@4.0.1/dist/flowbite.min.js"></script>



    <link rel="stylesheet" href="/assets/app.css">

</head>
<body>
    @yield('content')


    <script>
        $(document).ready(function() {
            // Your jQuery code here
            // $("body").css("color", "blue");
            $("a").addClass("underline");
        });
    </script>

</body>
</html>
