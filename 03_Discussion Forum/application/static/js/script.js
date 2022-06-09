function unlock_btn(id) {
    var BUTTON_ID = 'submit_btn'
    var val = document.getElementById(id).value;
    if (val.length > 0) {
        document.getElementById(BUTTON_ID).removeAttribute('disabled');
    }
    else{
        document.getElementById(BUTTON_ID).setAttribute('disabled');
    }
}

const likeBtn = document.querySelector('.like_btn');
let likeIcon = document.querySelector('#icon');
let likeCount = document.querySelector('#count');

let clicked = false;

likeBtn.addEventListener("click",()=>{
    if (!clicked) {
        clicked=true;
        likeIcon.innerHTML = `<i class="fas fa-thumbs-up"></i>`
        count.textContent++;
    }
    else{
        clicked = false;
        likeIcon.innerHTML = `<i class="far fa-thumbs-up"></i>`
        count.textContent--;
    }
})
