// Gets Data from API
fetch("https://api.api-onepiece.com/v2/fruits/en")
    .then(response => {
    return response.json();
    })
    .then(data => {
    console.log(data);
    })
    .catch(error => console.log(error));




// Turns Radio Buttons Unclickable (Devil Fruit Type Filter)
document.querySelectorAll(".df-type-filter input").forEach(radio => {
    radio.addEventListener("click", (event) => {
        const target = event.target;

        if (target.dataset.wasChecked === "true") {
            target.checked = false;
            target.dataset.wasChecked = "false";
        } else {
            document.querySelectorAll(".df-type-filter input").forEach(all => {
                all.dataset.wasChecked = "false";
            });

            target.dataset.wasChecked = "true";
        }
    });
});