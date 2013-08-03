$(document).ready(function(){
	
	/* -------- event handlers --------- */
	// info-box
	infoBox = $('.info-box');
	$('.opt-info').click(function(e){
		infoBox.css({'left': e.pageX, 'top': e.pageY});
		infoBox.fadeIn('fast');
		return false;
	});
	$('.info-box').click(function(){
		return false;
	});
	$('body').click(function(){
		infoBox.hide();
	})
	
	// add to market basket
	basketItems = $("#basket-items");
	$('.opt-shop').click(function(e){
		// i = $(this).children('i');
		// i.removeClass('icon-plus').addClass('icon-spin icon-refresh');
		var i = $(this);
		i.button('loading');
		setTimeout(function(){
		i.button('don');
		// p = i.parent();
		// i.removeClass('icon-refresh').removeClass('icon-spin').addClass('icon-ok');		
		// updating basket size
		basketItems.text(basketItems.text() * 1 + 1);
		}, 3000);
	});
	
	// test
	$('#enter').click(function(){
		$('.alert').alert('close');
		return false;
	});
});
