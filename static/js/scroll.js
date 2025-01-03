window.addEventListener("scroll", () => {
    const title = document.getElementById("title");
    if (window.scrollY > 100) { // Adjust scroll threshold as needed
        title.style.fontSize = "1rem";
    } else {
        title.style.fontSize = "1.2rem";
    }
});