
function orders() {
	$(".WRH-panel2").fadeOut("slow");
	setTimeout(function() {
		$(".WRH-panel2").load('NewOrdersBack');
	}, 500);
	$(".WRH-panel2").fadeIn("slow");
}

function tiny_orders(tmp) {
	$(".WRH-panel2").fadeOut("slow");
	setTimeout(function() {
		$(".WRH-panel2").load(tmp);
	}, 500);
	$(".WRH-panel2").fadeIn("slow");
}

function load_select_page(tmp) {
    $(".WRH-panel2").fadeOut(700);
    $(".WRH-panel2").html("<div class='loading'><div class='load-float'></div> <img src='images/loading.gif' /></div>");
    setTimeout(function() {
        $(".WRH-panel2").load(tmp);
    }, 700);
    $(".WRH-panel2").fadeIn("slow");
}

function load_first_page() {
    $(".WRH-panel2").fadeOut(700);
    $(".WRH-panel2").html("<div class='loading'><div class='load-float'></div> <img src='images/loading.gif' /></div>");
    setTimeout(function() {
        $(".WRH-panel2").load('WRHDelivery2');
    }, 700);
    $(".WRH-panel2").fadeIn("slow");
}

//function load_last_page() {
//    $(".WRH-panel2").fadeOut(700);
//    $(".WRH-panel2").html("<div class='loading'><div class='load-float'></div> <img src='images/loading.gif' /></div>");
//    setTimeout(function() {
//        $(".WRH-panel2").load('WRH-ConfirmationWRHDelivery.html');
//    }, 700);
//    $(".WRH-panel2").fadeIn("slow");
//}
