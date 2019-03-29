odoo.define('web', function (require) {
    "use strict";

    $(document).ready(function () {
	var interval = setInterval(function(){
		if($('.o_sub_menu').length > 0) {
			$('.o_sub_menu').append('<a href="#" class="oe_app_close_button"><i class="fa fa-arrow-right"></i></a>');

			$('.oe_app_close_button').click(function(){
				if($('.o_sub_menu').css("left") == '-250px'){
						$('.o_sub_menu').css("left", '0');
				} else {
						$('.o_sub_menu').css("left", '-250px');
				}
			});

			clearInterval(interval);
		}
	}, 1000);

    });

});
