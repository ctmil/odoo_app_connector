//console.log("Odoo App");
//this.$('.oe_searchview_input:last').focus();
/*
odoo.define('web', function (require) {
    "use strict";
*/
    $(document).ready(function () {
	var interval = setInterval(function(){
		if($('.oe_app_close_button').length == 0 && $('.oe_leftbar').length > 0) {
				console.log("Create Button SubMenu");
				$('body').append('<a href="#" class="oe_app_close_button"><i class="fa fa-th"></i></a>');

				$('.oe_app_close_button').click(function () {
					if($('.oe_leftbar').css('display') == 'table-cell') {
						$('.oe_leftbar').css('display', 'none');
					} else {
						$('.oe_leftbar').css('display', 'table-cell');
					}
				});
		}
		if($('.oe_app_close_search').length == 0 && $('.oe_leftbar').length > 0) {
                                console.log("Create Button Search");
                                $('body').append('<a href="#" class="oe_app_close_search"><i class="fa fa-search"></i></a>');

                                $('.oe_app_close_search').click(function () {
					console.log($('.oe_searchview').css('display'));
                                        if($('.oe_searchview').css('display') == 'none') {
						$('.oe_searchview').removeClass('importantHide');
                                                $('.oe_searchview').addClass('importantShow');
                                        } else {
						$('.oe_searchview').removeClass('importantShow');
                                                $('.oe_searchview').addClass('importantHide');
                                        }
                                });
                }
		/*if($('.o_sub_menu').length > 0) {
			$('.o_sub_menu').append('<a href="#" class="oe_app_close_button"><i class="fa fa-arrow-right"></i></a>');

			$('.oe_app_close_button').click(function(){
				if($('.o_sub_menu').css("left") == '-220px'){
						$('.o_sub_menu').css("left", '0');
				} else {
						$('.o_sub_menu').css("left", '-220px');
				}
			});

			clearInterval(interval);
		}*/
		//$('.oe_searchview_input:last').blur();
	}, 1000);


    });
/*
});
*/
