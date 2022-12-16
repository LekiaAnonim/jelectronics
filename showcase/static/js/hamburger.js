// const hamMenu = document.querySelector(`.hamburger-menu`);
// const hamburgerImage = "static/images/Menu_52px.png";
// const closeImage = "static/images/Close_100px.png";
// const navList = document.querySelector(`.nav-list`);

// hamMenu.addEventListener(`click`, function () {
    
//     if (this.getAttribute(`src`)== hamburgerImage) {
//         this.setAttribute(`src`, closeImage);
//         navList.style = `display: block`;
//         this.style = `transform: rotate(180deg)`;
//         this.style = `transition: transform linear 1s`;
//     } else {this.setAttribute(`src`, hamburgerImage);
//         navList.style = `display: none`;
//     }
// });



// ----------------------------------------------------------------------------------

const hamburger = document.querySelector(".hamburger");
const navMenu = document.querySelector(".ham-menu");

hamburger.addEventListener("click", mobileMenu);

function mobileMenu() {
    hamburger.classList.toggle("display-menu");
    navMenu.classList.toggle("display-menu");
    // navMenu.style.display = 'block';
}

// const navLink = document.querySelectorAll(".nav-link");

// navLink.forEach(n => n.addEventListener("click", closeMenu));

// function closeMenu() {
//     hamburger.classList.remove("active");
//     navMenu.classList.remove("active");
// }