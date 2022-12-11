// Script for Slider
const shows = document.querySelectorAll('.showcase-image');
const slide_control = document.querySelector('.slider-control');
const sliderImg = document.querySelectorAll('.img1');

Array.from(sliderImg).forEach(function (img) {
    img.style.width = `${screen.width}px`;
})
const showsArray = Array.from(shows);
let z_index = 100;
// Create a span element for slider control
const creatControl = new Promise(function (resolve) {
    for (let i = 0; i < shows.length; i++) {
        const span = document.createElement('div');
        span.style.zIndex = 500;
        span.classList.add(`span`);
        slide_control.appendChild(span);
        resolve(span.classList[0]);
    }
})
// console.log(screen.width);
let n = 0;
let timeId = setInterval(() => {
    n += 1;
    showsArray.forEach(function (show) {
        show.style.zIndex = z_index--;
        // console.log(n);
        if (n < shows.length) {
            // console.log(show);
            show.style.transform = `translateX(-${n * screen.width}px)`;
        } else {
            n -= shows.length+1;
            show.style.transform = `translateX(${0}px)`;
            // span.classList.add('active');

        }
    })
}, 4000);



creatControl.then(response => {
    // console.log(response);
    const spans = document.querySelectorAll(`.${response}`);
    showsArray.forEach(function (show) {
        show.style.zIndex = z_index;
        Array.from(spans).forEach(function (sp) {
            sp.addEventListener('click', function () {
            show.style.transform = 'translateX(1300px)';
        })
        })
    })
})
// 
