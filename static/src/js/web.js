odoo.define('web', function (require) {
    "use strict";

    $(document).ready(function () {
	var interval = setInterval(function(){
		if($('nav.o_main_navbar').length > 0 && $('.o_menu_sections').length > 0) {
			if($('#o_button_toggle').length == 0) {
				$('nav.o_main_navbar').prepend('<button type="button" class="fa fa-bars navbar-toggler" id="o_button_toggle"></button>');
				$('#o_button_toggle').click(function(){
					$('.o_menu_sections').animate({height:"toggle"});
					$('.o_menu_systray').toggle();
				});
			}
			clearInterval(interval);
		}
	}, 1000);

    });

});
