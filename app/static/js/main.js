// app\static\js\main.js

document.addEventListener("DOMContentLoaded", () => {
    const sortSelect = document.getElementById("sort");
    const ideaList = document.getElementById("idea-list");

    if (!sortSelect) return;

    sortSelect.addEventListener("change", () => {
        const cards = Array.from(document.querySelectorAll(".idea-card"));

        let sorted;

        if (sortSelect.value === "likes") {
            sorted = cards.sort((a, b) =>
                b.dataset.likes - a.dataset.likes
            );
        } else {
            sorted = cards.sort((a, b) =>
                b.dataset.date - a.dataset.date
            );
        }

        sorted.forEach(card => ideaList.appendChild(card));
    });
});


document.addEventListener("DOMContentLoaded", () => {
    const inputs = document.querySelectorAll("input");

    inputs.forEach(input => {
        input.addEventListener("focus", () => {
            input.parentElement.classList.add("active");
        });

        input.addEventListener("blur", () => {
            if (input.value === "") {
                input.parentElement.classList.remove("active");
            }
        });
    });
});