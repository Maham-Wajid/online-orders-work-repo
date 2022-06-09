$(document).ready(function() {
    $(".comment-reply").hide();
    $(".post-comment").hide();
});

function filterStyle(id){
    if(id=='new')
    {
        $( "#old" ).removeClass( 'active');
        $( "#new" ).addClass( 'active');
    }
    else{
        $( "#new" ).removeClass( 'active');
        $( "#old" ).addClass( 'active');
    }
}

function actionToggle(){
    var action = document.querySelector('.action');
    action.classList.toggle('active');
}