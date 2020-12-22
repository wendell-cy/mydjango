$(function(){
    // 从cookie中获取csrf_token
    let csrftoken= getCookie('csrftoken')
    //这个设置让所有ajax post/delete请求在其请求头中都携带x-csrftoken 信息
    $.ajaxSetup( {
        beforeSend: function (xhr,settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken",csrftoken);
                }
        }
    });

    $('#newsFormModal').on('shown.bs.modal',function(){
        $('#newsInput').trigger('focus')
    });

    $("#postNews").click(function () {
        if (currentUser === "") {
            alert("请登录后再发布");
            return;
        }
        if ($('#newsInput').val() ==="") {
            alert("请输入更新的动态信息")
        } else {
            // alert("发布ok")
            $.ajax( {
                url: '/news/post-news/',
                data: $("#postNewsFrom").serialize(),
                type: 'POST',
                cache: false,
                success: function (data) {
                    $('ul.stream').prepend(data);
                    $('#newsInput').val("");
                    $('#newsFormModal').modal("hide");
                },
                error: function (data) {
                    alert(data.responseText);
                },
            });
    }
    });

    $("ul.stream").on("click", ".like", function () {
        // alert("hello");
        let li = $(this).closest('li')
        let newsId = $(li).attr("news-id")
        // alert(newsId)
        let payload = {
            'newsId': newsId,
            'csrf_token': csrftoken,
        }
        // alert(payload)
        $.ajax({
            url: '/news/like/',
            data: payload,
            type: 'POST',
            cache:false,
            success: function (data) {
                $(".like .like-count", li).text(data.liker_count);
                if ($(".like .heart" ,li).hasClass("fa fa-heart")) {
                    ($(".like .heart", li).removeClass("fa fa-heart"));
                    ($(".like .heart", li).addClass("fa fa-heart-o"));
                } else {
                    ($(".like .heart", li).removeClass("fa fa-heart-o"));
                    ($(".like .heart", li).addClass("fa fa-heart"));
                }
            }
        });
    });

    $('#replyFormModal').on('show.bs.modal', function (event) {
        let button = $(event.relatedTarget);
        let recipient = button.data('who');
        let newsid = button.data('newsid');
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
        let modal = $(this);
        modal.find('.modal-title').text('新的回复 到： ' + recipient)
        modal.find('.modal-body input.recipient').val(recipient)
        modal.find('.modal-body input.newsid').val(newsid)
    });

    $("#postReply").click(function () {
        if (currentUser === "") {
            alert("请登录后再发布评论");
            return;
        }
        if ($('#reply-content').val() ==="") {
            alert("请输入评论内容")
        } else {
            // alert("发布ok")
            $.ajax( {
                url: '/news/post-reply/',
                data: $("#postReplyForm").serialize(),
                type: 'POST',
                cache: false,
                success: function (data) {
                    let li = $('[news-id='+data.newsid+']');
                    $(".reply .reply-count", li).text(data.replies_count);
                    $("reply-content").val("");
                    $('#replyFormModal').modal("hide");
                    // $('ul.stream').prepend(data);
                    // $('#reply-content').val("");
                    // $('#replyFormModal').modal("hide");
                },
                error: function (data) {
                    alert(data.responseText);
                },
            });
    }

    });

    $("ul.stream").on("click", ".reply", function () {
        // alert('hahahah')
        let li = $(this).closest('li');
        let newsId = $(li).attr("news-id");
        // alert(newsId)
        $.ajax({
            url: '/news/get-replies/',
            data: {'newsId': newsId},
            cache: false,
            success: function (data) {
                $("#replyListModal .modal-body").html(data.replies_html);
            }
        });
    });
});







