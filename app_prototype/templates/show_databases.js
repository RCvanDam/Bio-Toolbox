var div = document.getElementById("database_options");
var display = 0;

function hide_database_option()

{
    if(display == 0)
    {
        div.style.display = "block";
        display = 1;

    }
    else
    {
        div.style.display = "none"
        display = 0;

    }

}
