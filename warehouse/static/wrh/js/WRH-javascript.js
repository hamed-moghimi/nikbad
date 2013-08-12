
function orders() {
	$(".WRH-panel2").fadeOut("slow");
	setTimeout(function() {
		$(".WRH-panel2").load('NewOrdersBack');
	}, 500);
	$(".WRH-panel2").fadeIn("slow");
}

function ready_orders() {
    $(".WRH-panel2").fadeOut("slow");
    setTimeout(function() {
        $(".WRH-panel2").load('ReadyOrder2');
    }, 500);
    $(".WRH-panel2").fadeIn("slow");
}

function ready_tiny_orders(tmp) {
    $(".WRH-panel2").fadeOut("slow");
    setTimeout(function() {
        $(".WRH-panel2").load(tmp);
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

function confirm_order(tmp) {
    var st = "ConfirmOrder/";
    var st2 = st.concat(tmp.toString())
    $(".WRH-panel2").fadeOut("slow");
    setTimeout(function() {
        $(".WRH-panel2").load(st2);
    }, 500);
    $(".WRH-panel2").fadeIn("slow");
}

function confirm_ready_order(tmp) {
    var st = "ConfirmReadyOrder/";
    var st2 = st.concat(tmp.toString())
    $(".WRH-panel2").fadeOut("slow");
    setTimeout(function() {
        $(".WRH-panel2").load(st2);
    }, 500);
    $(".WRH-panel2").fadeIn("slow");
}


function load_select_page(tmp) {
    $(".WRH-panel2").fadeOut("slow");
//    $(".WRH-panel2").html("<div class='loading'><div class='load-float'></div> <img src='{{}}images/loading.gif' /></div>");
    setTimeout(function() {
        $(".WRH-panel2").load(tmp);
    }, 700);
    $(".WRH-panel2").fadeIn("slow");
}

function load_first_page() {
    $(".WRH-panel2").fadeOut("slow");
//    $(".WRH-panel2").html("<div class='loading'><div class='load-float'></div> <img src='images/loading.gif' /></div>");
    setTimeout(function() {
        $(".WRH-panel2").load('WRHDelivery2');
    }, 700);
    $(".WRH-panel2").fadeIn("slow");
}

function confirm_clear(){
    var bill = document.getElementById('bill');
    var a = bill.value;
    if (/^[\d]+$/.test(a))
    {
        $(".WRH-panel2").fadeOut("slow");
        var str = "ConfirmClearance/";
        var st2 = str.concat(a);
        setTimeout(function() {
            $(".WRH-panel2").load(st2.toString());
        }, 500);
        $(".WRH-panel2").fadeIn("slow");
    }else
    {
        alert("لطفا یک عدد برای شماره فیش وارد کنید.")
    }
}

function clear_end(tmp) {
    $(".WRH-panel2").fadeOut("slow");
    var str = "ConfirmClearance-end/";
    var st2 = str.concat(tmp.toString())
    setTimeout(function() {
        $(".WRH-panel2").load(st2);
    }, 500);
    $(".WRH-panel2").fadeIn("slow");
}

function clearance() {
    $(".WRH-panel2").fadeOut("slow");
    setTimeout(function() {
        $(".WRH-panel2").load('Clearance2');
    }, 500);
    $(".WRH-panel2").fadeIn("slow");
}
function confirm_product_return() {
    var code = document.getElementById('code');
    var pcode = document.getElementById('pcode');
    var b = pcode.value;
    var a = code.value;
    if (! /^[\d]+$/.test(a))
    {
        alert("لطفا یک عدد برای شماره حواله وارد کنید.");
    }else
    {
        if (! /^[\d]+$/.test(b))
        {
            alert("لطفا یک عدد برای کد کالا وارد کنید.");
        }
        else
        {
            $(".WRH-panel2").fadeOut("slow");
            var str = "CustomerReturn-next/";
            var st2 = str.concat(a);
            var st3 = st2.concat("/")
            var st4 = st3.concat(b);
            setTimeout(function() {
                $(".WRH-panel2").load(st4.toString());
            }, 500);
            $(".WRH-panel2").fadeIn("slow");
        }
    }
}

function confirm_product_return2(pid, kid) {
    $(".WRH-panel2").fadeOut("slow");
    var str = "CustomerReturn-next/";
    var st2 = str.concat(pid);
    var st3 = st2.concat("/")
    var st4 = st3.concat(kid);
    setTimeout(function() {
        $(".WRH-panel2").load(st4.toString());
    }, 500);
    $(".WRH-panel2").fadeIn("slow");
}

function customer_return() {
    $(".WRH-panel2").fadeOut("slow");
    setTimeout(function() {
        $(".WRH-panel2").load('CustomerReturn2');
    }, 500);
    $(".WRH-panel2").fadeIn("slow");
}

function receipt_return() {
    $(".WRH-panel2").fadeOut("slow");
    setTimeout(function() {
        $(".WRH-panel2").load('ReceiptDelivery2');
    }, 500);
    $(".WRH-panel2").fadeIn("slow");
}


function confirm_return(pid, kid) {
    var qnt = document.getElementById('qnt');
    var a = qnt.value;
    $(".WRH-panel2").fadeOut("slow");
    var str = "ConfirmReturn/";
    var st2 = str.concat(pid);
    var st3 = st2.concat("/")
    var st4 = st3.concat(kid);
    var st5 = st4.concat("/");
    var st6 = st5.concat(a);
    setTimeout(function() {
        $(".WRH-panel2").load(st6);
    }, 500);
    $(".WRH-panel2").fadeIn("slow");
}

function confirm_receipt(pid) {
    $(".WRH-panel2").fadeOut("slow");
    var str = "ConfirmReceipt/";
    var st2 = str.concat(pid);
    setTimeout(function() {
        $(".WRH-panel2").load(st2);
    }, 500);
    $(".WRH-panel2").fadeIn("slow");
}


function confirm_delivery() {
    var qnt = document.getElementById('code');
    var a = qnt.value;
    $(".WRH-panel2").fadeOut("slow");
    var str = "ReceiptDetail/";
    var st6 = str.concat(a);
    setTimeout(function() {
        $(".WRH-panel2").load(st6);
    }, 500);
    $(".WRH-panel2").fadeIn("slow");
}

function customer_delivery() {
    $(".WRH-panel2").fadeOut("slow");
    setTimeout(function() {
        $(".WRH-panel2").load('WRH-CustomerDelivery2.html');
    }, 500);
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
