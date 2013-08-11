$(document).ready(function()
{
    // menu navbar affix
    $('#menu-navbar').affix({
        offset: { top: 200 }
    });

    // login menu toggle
    loginMenu = $('#login-menu');
    $('#login-menu-button').click(function(){
       loginMenu.slideToggle('fast');
    });
});

// if you did not use jQuery and wrote your codes in basic javascript(extremely not recommended!!!), write your codes here. Please port your codes to jQuery as soon as possible, for compatibility with other codes and all web browsers.