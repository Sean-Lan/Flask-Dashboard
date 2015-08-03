$(document).ready(function() {
    var client = new ZeroClipboard($('.copy-span'), { 
        moviePath: '/static/js/ZeroClipboard.swf' 
    });
    // bind the zeroclipboard event
    client.on( "ready", function( readyEvent ) {
        client.on( "beforecopy", function( event ) {
            event.target.style.color = 'green' 
        } );
        client.on( "copy", function(event) {
            event.clipboardData.setData('text/plain', $(event.target).parent().find('.copy-content').text());
        } );
        client.on( "aftercopy", function( event ) {
            event.target.style.color = 'black' 
        } );
        client.on( "aftercopy", function( event ) {
            event.target.style.color = 'black' 
        } );
    });

    $('.copy-span').tooltip({title: "copy full path to clipboard", placement: 'right'});
    // Here is an issue, sometimes tooltip won't disappear when
    // mouse out, so I add a timeout function to force it disappear after
    // 2 seconds.
    $('.copy-span').mouseenter(function(){
        var that = $(this)
        that.tooltip('show');
    setTimeout(function(){
        that.tooltip('hide');
    }, 2000);
    });

    $('#comments-modal').on('shown.bs.modal', function () {
        $(document).off('focusin.modal');
        editor = KindEditor.create('textarea[name="comments"]', {
            resizeType : 1,
            allowPreviewEmoticons : false,
            allowImageUpload : false,
            items : [
            'fontname', 'fontsize', '|', 'forecolor', 'hilitecolor', 'bold', 'italic', 'underline',
            'removeformat', '|', 'justifyleft', 'justifycenter', 'justifyright', 'insertorderedlist',
            'insertunorderedlist', '|', 'link'],
            width: '100%',
            autoHeightMode : true,
            afterCreate : function() {
                this.loadPlugin('autoheight');
            }
        });
        KindEditor.html('textarea[name="comments"]', $('.CurrentComment').html());
    })

    $('#comments-modal').on('hidden.bs.modal', function () {
        KindEditor.remove('textarea[name="comments"]');
        $('.CurrentComment').parent().removeClass('success')
        $('.CurrentComment').removeClass('CurrentComment')
    })

    $(".comments").dblclick(function(){
        var primary_key = $(this).parent().find('td span.primary-key').text();
        var comments = $(this).parent().find('td').last().text();
        $(this).addClass('CurrentComment')
        $(this).parent().addClass('success')
        $('#comments-modal').attr('data-primary_key', primary_key);
        $('#comments-modal').modal('show');
    });

    $('.comments').tooltip({title: "double click to edit comments", placement: 'top'});
    // Here is an issue, sometimes tooltip won't disappear when
    // mouse out, so I add a timeout function to force it disappear after
    // 2 seconds.
    $('.comments').mouseenter(function(){
        var that = $(this)
        that.tooltip('show');
    setTimeout(function(){
        that.tooltip('hide');
    }, 2000);
    });

    $("#btn-submit").click(function(){
        var comments = editor.html()
        var primary_key = $('#comments-modal').attr('data-primary_key')
        var table_name = $('.main-table').attr('table_name')
        var key_name = $('.main-table').attr('key_name')
        $.post($SCRIPT_ROOT + "/_update_table",
            {
                comments: comments,
                primary_key: primary_key,
                table_name: table_name,
                key_name: key_name
            },
            function(data,status){
                if (data.status == 'success') {
                    // console.log("Data: " + data + "\nStatus: " + status);
                    $('.CurrentComment').html(comments)
                    $('#comments-modal').modal('hide');
                }
            });
    });

});
