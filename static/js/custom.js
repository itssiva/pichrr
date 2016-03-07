$(function(){
$(".dropdown").hover(
        function() {
            $('.dropdown-menu', this).stop( true, true ).fadeIn("fast");
            $(this).toggleClass('open');
            $('b', this).toggleClass("caret caret-up");
        },
        function() {
            $('.dropdown-menu', this).stop( true, true ).fadeOut("fast");
            $(this).toggleClass('open');
            $('b', this).toggleClass("caret caret-up");
        });
});

//var loadingobj ;
var start_loading = 0;
var a_url = a_url || "";
var extend_query = extend_query || "";
var feedobj = $('.feed');

jQuery(document).ready(function() {
var offset = 250;
var duration = 300;
jQuery(window).scroll(function() {
    if (jQuery(this).scrollTop() > offset) {
        jQuery('.back-to-top').fadeIn(duration);
    } else {
        jQuery('.back-to-top').fadeOut(duration);
    }
});

    jQuery('.back-to-top').click(function(event) {
        event.defaultPrevented();
        jQuery('html, body').animate({scrollTop: 0}, duration);
        return false;
    })
});


$(document).ready(function(){
    $("nav [href]").each(function () {
        if (this.href == window.location.href) {
            var this_value = this;
            $(this).addClass("currentLink");
        }
    });

});


function load_posts(page) {
    console.log("page is", ""+page);
    $.get(a_url+'?older=' + page + '&'+extend_query,
        function(response) {
        	if(response==0){
				//loadingobj.hide();
                feedobj.append('<div class="no_more"> <h1>No more posts to show</h1></div>');
                start_loading = 1;

        	}else{
				var $boxes = $(response);
                feedobj.append( $boxes);
                //loadingobj.hide();
				start_loading=0;
			}
        }
    );
}


var getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName, i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
};
var prev_page = 1;

$(window).scroll(function() {
	//loadingobj = $(".loading");
    if (($(window).height() + $(window).scrollTop()+ 200) >= $(document).height()) {
    	var next_page = parseInt($('.feed span:last').attr('data-next'));
        if (next_page && start_loading==0&&next_page>prev_page) {
            prev_page = next_page;
            start_loading=1;
            if(document.location.search.length) {
                var q = getUrlParameter('q');
                extend_query = 'q='+q;

            }
            //loadingobj.show();
            load_posts(next_page);
        }
    }
});

