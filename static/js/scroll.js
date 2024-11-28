window.addEventListener("scroll", () => {
    const title = document.getElementById("title");
    if (window.scrollY > 100) { // Adjust scroll threshold as needed
        title.style.fontSize = "1.5rem";
    } else {
        title.style.fontSize = "2rem";
    }
});