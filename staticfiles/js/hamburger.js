const hamMenu = document.querySelector(`.hamburger-menu`);
const hamburgerImage = "static/images/Menu_52px.png";
const closeImage = "static/images/Close_100px.png";
const navList = document.querySelector(`.nav-list`);

hamMenu.addEventListener(`click`, function () {
    
    if (this.getAttribute(`src`)== hamburgerImage) {
        this.setAttribute(`src`, closeImage);
        navList.style = `display: block`;
        this.style = `transform: rotate(180deg)`;
        this.style = `transition: transform linear 1s`;
    } else {this.setAttribute(`src`, hamburgerImage);
        navList.style = `display: none`;
    }
});