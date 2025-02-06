let allData = {}

function loadImages() {
    fetch("data/data2.0.json")
        .then(response => response.json())
        .then(data => {
            allData = data
            createMenu()
            let url = new URL(window.location)
            let query = url.searchParams.get('query')
            displayImages(query)
        })
}

function createMenu() {
    let menu = document.querySelector("#tabs ul")

    Object.keys(allData).forEach(category => {
        let menu_item = document.createElement('li');
        let item = document.createElement("a");
        item.setAttribute('href', `?query=${category}`)
        item.innerText = category
        menu_item.appendChild(item);
        menu.appendChild(menu_item)
    })

    menu.className = "menu-list"

    document.querySelector('#tabs').className = "menu"
}

function displayImages(category='advoree') {
    let gallery = document.querySelector("#gallery")
    
    let items = allData[category];
    items.forEach(item => {
        let img = document.createElement('img')
        img.src = item
        gallery.appendChild(img)
    })
}

window.addEventListener("DOMContentLoaded", () => loadImages());
