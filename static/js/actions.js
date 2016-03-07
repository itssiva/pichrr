$(document).on('click', '.like_button , .dislike_button ', function () {
        var obj = $(this);

        var class_name = this.className;
        obj.addClass('disabled');
        var url = obj.attr('href');
        console.log("Loc", "1");
        console.log("class", class_name);
        console.log("url", url);

        $.ajax({
            url: url.concat("/"),


            success: function (html) {
                console.log("loc", "success");
                ret = html;
                console.log('json', ret);

                var o = jQuery.parseJSON(ret);

                console.log("loc", "success1");

                var points = o[0].rep_count;

                if (class_name == 'like_button') {
                    console.log("Loc", "2");
                    var points_obj = obj.siblings('.points');
                    var dislike_obj = obj.siblings('.dislike_button');

                    console.log("In like other obj is", points_obj);
                    console.log("In like lik status is", dislike_obj);


                    if (o[0].liked_flag == -1) {
                        obj.html('<i class="fa fa-thumbs-up fa-lg" title="like"></i>');
                        points_obj.html(''+points);
                    } else {
                        obj.html('<i title="dislike" class="fa fa-thumbs-up fa-lg color_it"></i>');
                        dislike_obj.html('<i  class="fa fa-thumbs-down fa-lg"></i>');
                        points_obj.html(''+points);

                    }
                }
                else{
                    console.log("Loc", "3");
                    var points_obj = obj.siblings('.points');
                    var like_obj = obj.siblings('.like_button');
                    if(class_name == 'dislike_button'){

                        if (o[0].disliked_flag == -1) {
                        obj.html('<i class="fa fa-thumbs-down fa-lg" title="like"></i>');
                            points_obj.html(''+points);
                    } else {
                        obj.html('<i title="dislike" class="fa fa-thumbs-down fa-lg color_it"></i>');
                        like_obj.html('<i  class="fa fa-thumbs-up fa-lg"></i>');
                            points_obj.html(''+points);
                    }
                    }
                }
                obj.removeClass('disabled');

            }
        });
        return false;
    });



    $(document).on('click', '.favorite_button', function () {
        var obj = $(this);
        obj.addClass('disabled');
        var favorite_url = obj.attr('href');
        $.ajax({
            url: favorite_url.concat("/"),
            success: function (html) {
                ret = html;
                var o = jQuery.parseJSON(ret)
                if (o[0].favorite_flag == -1) {
                    obj.html('<i class="fa fa-heart fa-lg" title="Add to Faorites"></i>');
                }
                else {
                    obj.html('<i title="Remove from Favorites" class="fa fa-heart fa-lg color_it"></i>');
                }
                obj.removeClass('disabled');
            }
        });
        return false;
    });/**
 * Created by sponugot on 2/27/16.
 */
