function set_hours() {
    console.log( "ready!" );
    $(".hour_rent").on('click', function(){
        alert("I am an alert box!");
        var price_changes = document.getElementsByClassName("change_text");
        var i;
        for (i = 0; i < x.length; i++) {
            x[i].innerHTML = "bajs";
        }
        console.log(result);
    });
};

//$(function() {
//console.log( "ready!" );
//$(".news_box").on('click', function(){
//var entry = this;
//var post_id = $(this).find('h2').attr('id');
//$.ajax({
//type:'GET',
//url: '/delete' + '/' + post_id,
//context: entry,
//success:function(result){
//if(result['status'] === 1){
//$(this).remove();
//console.log(result);
//}
//}
//});
//});
//});
