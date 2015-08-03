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
        KindEditor.create('textarea[name="comments"]', {
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
        KindEditor.html('textarea[name="comments"]', $(this).attr('data-comments'));
    })

    $('#comments-modal').on('hidden.bs.modal', function () {
        KindEditor.remove('textarea[name="comments"]');
    })

    $(".comments").dblclick(function(){
        var primary_key = $(this).parent().find('td').first().text();
        var comments = $(this).parent().find('td').last().text();
        $('#comments-modal').attr('data-comments', comments);
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

});
