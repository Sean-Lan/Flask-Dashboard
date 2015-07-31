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
    
});

