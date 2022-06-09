function unlock_btn(id) {
    var BUTTON_ID = 'submit_btn'
    // let crsor = document.getElementById('submit_btn');
    // crsor.addEventListener(onkeyup,()=>{
    //     crsor.style="cursor: pointer;"
    // })
    var val = document.getElementById(id).value;
    if (val.length > 0) {
        document.getElementById(BUTTON_ID).removeAttribute('disabled');
    }
    else{
        document.getElementById(BUTTON_ID).setAttribute('disabled');
    }
}


function update_like(topic_id) {
    if ($('#'+topic_id).hasClass('fas')) {
        $('#'+topic_id).removeClass('fas');
        $('#'+topic_id).addClass('far');
        $.ajax({
            url: "/remove_like",
            type: 'POST',
            data: { topic_id:topic_id},
        }).done(function (data) {
            if(data == 0){
                alert('please login to like posts');
            }
        });
    }
    else {
        $('#'+topic_id).removeClass('far');
        $('#'+topic_id).addClass('fas');
        $.ajax({
            url: "/add_like",
            type: 'POST',
            data: { topic_id:topic_id},
        }).done(function (data) {
            if(data == 0){
                alert('please login to like posts');
            }
        });
    }
}