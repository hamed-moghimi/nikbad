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
	basketItems = $('#basket-items');
	$('.opt-shop').click(function(e){
        var i = $(this);

        if(!i.hasClass('disabled'))
        {
            i.button('loading');
            i.addClass('disabled');
            setTimeout(function(){
                i.button('done');
                i.removeClass('disabled');
                // updating basket size
                basketItems.text(basketItems.text() * 1 + 1);
            }, 6000);
        }

        return false;
	});

    // thumbnails change
    vitrinIcon = $('.vitrin-icon')
    $('.vitrin-thumbnail').click(function(){
        var icon = $(this).children('img');
        vitrinIcon.attr('src', icon.attr('src'));
        vitrinIcon.attr('title', icon.attr('title'));
        return false;
    });

    // large icons
    $('#iconModal').on('show', function () {
        $(this).find('#iconModalLabel').text(vitrinIcon.attr('title'));
        $(this).find('.vitrin-icon-large').attr('src', vitrinIcon.attr('src'));
    })

    // feedback submit
    feedbackTable = $('#feedback-table > tbody');
    feedbackContent = $('#feedback-content');
    feedbackSubmitButton = $('#feedback-submit-button');
    $('#feedback-submit').submit(function(){
        form = $(this);
        url = form.attr('action');

        content = $('#feedback-content').val();
        if(content == '')
            return false;

        pID = $('#productID').val();
        csrf = $('[name=csrfmiddlewaretoken]').val();
        dataString = 'productID=' + pID + '&content=' + content + '&csrfmiddlewaretoken=' + csrf;
        $.ajax({
            type: "POST",
            url: url,
            data: dataString,

            success: function() {
                feedbackTable.append($('<tr><td>' + content + '</td></tr>'));
                feedbackContent.val('');
                feedbackSubmitButton.button('reset');
            },

            error: function() {
            }
        });

        feedbackSubmitButton.attr('disabled', 'disabled');
        return false;
    });
});
