
var display_img = document.querySelector(".photo-display img");

var select_img = document.querySelectorAll(".product-instance-photos img");

console.log(select_img);

// Array.from(select_img).forEach(function (image) {
//     image.removeAttribute('style');
// });


Array.from(select_img).forEach(function (image) {

    var select_img_link = image.getAttribute("src");
    

    image.addEventListener('click', function (e) {
        
        e.preventDefault();
        display_img.setAttribute('src', select_img_link);
        image.setAttribute('style', 'border: solid green');
        
    }, false);
    
});

var save = document.querySelectorAll('.save p');

var previous = document.querySelectorAll('.previous-price p strike');
var current = document.querySelectorAll('.price p');


// converting html collections to array

var savelist = Array.from(save);
var previouslist = Array.from(previous);
var currentlist = Array.from(current);

var percent_save = (previouslist.innerHTML - currentlist.innerHTML) * 100 / previouslist.innerHTML;

// savelist.forEach(function (item) {

    
for (let i = 0; i < previouslist.length; i++) {

    savelist[i].innerHTML = Math.round((previouslist[i].innerHTML - currentlist[i].innerHTML) * 100 / previouslist[i].innerHTML);
    
};
const addCartForm = document.querySelector('form');
const addToCart = document.querySelector('form #amount');
const price = document.querySelector('.disc-price').innerHTML;

addCartForm.addEventListener('submit', function (e) {
    
    e.preventDefault();

    const quantity = addToCart.value;
    var new_price = quantity*price;
    document.querySelector('.disc-price').innerHTML = new_price;
});