$(function(){
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
});

