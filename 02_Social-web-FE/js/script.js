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

