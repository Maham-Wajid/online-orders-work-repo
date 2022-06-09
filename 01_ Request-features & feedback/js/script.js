function actionToggle(){
    var action = document.querySelector('.action');
    action.classList.toggle('active');
}

$(document).ready(function() {
    $('.trending').show();
    $('.top').hide();
    $('.new').hide();
});
function select_filter(id){
    var selected_value = document.getElementById('list').value;
    if(selected_value == 'trending')
    {
        $('.trending').show();
        $('.top').hide();
        $('.new').hide();
    }
    else if(selected_value == 'top')
    {
        $('.trending').hide();
        $('.top').show();
        $('.new').hide();
    }
    else{
        $('.top').hide();
        $('.trending').hide();
        $('.new').show();
    }
}

function search_posts() {
    var filter = $('#post-search').val().toLowerCase();
    var posts = document.getElementsByClassName('single-post');
    for (i = 0; i < posts.length; i++) {
    var inner_text = posts[i].children[1].children[0].children[0].children[0].innerText.toLowerCase();
      if (inner_text.includes(filter)) {
          console.log(posts[i]);
        posts[i].style.display = "flex";
      } else {
        posts[i].style.display = "none";
      }
    }
  }